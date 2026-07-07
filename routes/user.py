from flask import Blueprint, jsonify, request
from flask_jwt_extended import jwt_required, get_jwt_identity 
from models import db, Trek, User, Booking
from werkzeug.security import generate_password_hash, check_password_hash
from extensions import cache
from tasks import export_booking_history
from flask import send_file
import os

user_bp = Blueprint(
    "user",
    __name__,
    url_prefix="/user"
)

@user_bp.route("/dashboard-data")
@jwt_required()
def dashboard_data():

    total_treks = Trek.query.count()

    total_bookings = Booking.query.count()

    active_treks = Trek.query.filter_by(
        status="Approved"
    ).count()

    return jsonify({

        "total_treks": total_treks,

        "total_bookings": total_bookings,

        "active_treks": active_treks

    })

@user_bp.route("/treks")
@jwt_required()
@cache.cached(timeout=300)
def available_treks():

    difficulty = request.args.get(
        "difficulty"
    )

    location = request.args.get(
        "location"
    )

    duration = request.args.get(
        "duration"
    )

    query = Trek.query.filter(
        Trek.available_slots > 0,
        Trek.status == "Approved"
    )

    if difficulty:

        query = query.filter(
            Trek.difficulty == difficulty
        )

    if location:

        query = query.filter(
            Trek.location.ilike(
                f"%{location}%"
            )
        )

    if duration:

        query = query.filter(
            Trek.duration <= int(duration)
        )

    treks = query.all()

    return jsonify([
        {
            "id": trek.id,
            "name": trek.name,
            "location": trek.location,
            "difficulty": trek.difficulty,
            "duration": trek.duration,
            "available_slots": trek.available_slots,
            "description": trek.description
        }

        for trek in treks
    ])

@user_bp.route(
    "/book-trek/<int:trek_id>",
    methods=["POST"]
)
@jwt_required()
def book_trek(trek_id):

    data = request.get_json()

    trek = Trek.query.get_or_404(
        trek_id
    )

    if trek.available_slots <= 0:

        return jsonify({
            "message":
            "Trek is Full"
        }), 400

    if trek.status != "Approved":

        return jsonify({
            "message":
            "Trek is not available for booking"
        }), 400

    booking = Booking(

        user_id=data["user_id"],

        trek_id=trek_id,

        status="Booked",

        payment_status="Pending"
    )

    trek.available_slots -= 1

    db.session.add(
        booking
    )

    db.session.commit()

    cache.clear()    
    return jsonify({
        "message":
        "Trek Booked Successfully"
    })

@user_bp.route(
    "/my-bookings/<int:user_id>"
)
@jwt_required()
def my_bookings(user_id):

    bookings = Booking.query.filter_by(
        user_id=user_id
    ).all()

    result = []

    for booking in bookings:

        trek = Trek.query.get(
            booking.trek_id
        )

        result.append({

            "booking_id":
                booking.id,

            "trek_name":
                trek.name,

            "location":
                trek.location,

            "difficulty":
                trek.difficulty,

            "status":
                booking.status,

            "payment_status":
                booking.payment_status
        })

    return jsonify(result)

@user_bp.route(
    "/cancel-booking/<int:id>",
    methods=["PUT"]
)
@jwt_required()
def cancel_booking(id):

    booking = Booking.query.get_or_404(id)

    print("Before:", booking.status, booking.payment_status)

    booking.status = "Cancelled"
    booking.payment_status = "-"

    print("After:", booking.status, booking.payment_status)

    trek = Trek.query.get(booking.trek_id)
    trek.available_slots += 1

    db.session.commit()

    updated = Booking.query.get(id)
    print("Database:", updated.status, updated.payment_status)

    cache.clear()

    return jsonify({
        "message": "Booking Cancelled"
    })

@user_bp.route(
    "/profile"
)
@jwt_required()
def get_profile():

    user_id = int(
        get_jwt_identity()
    )

    user = User.query.get_or_404(
        user_id
    )

    return jsonify({

        "id": user.id,

        "name": user.name,

        "email": user.email,

        "phone": user.phone

    })

@user_bp.route(
    "/profile",
    methods=["PUT"]
)
@jwt_required()
def update_profile():

    user_id = int(
        get_jwt_identity()
    )

    user = User.query.get_or_404(
        user_id
    )

    data = request.get_json()

    user.name = data["name"]

    user.phone = data["phone"]

    db.session.commit()

    return jsonify({

        "message":
        "Profile Updated Successfully"

    })

@user_bp.route(
    "/export-history"
)
@jwt_required()
def export_history():

    user_id = int(
        get_jwt_identity()
    )

    task = export_booking_history.delay(
        user_id
    )

    return jsonify({

        "message": "Export Started",

        "task_id": task.id

    })
from celery_worker import celery

@user_bp.route(
    "/export-status/<task_id>"
)
@jwt_required()
def export_status(task_id):

    task = celery.AsyncResult(task_id)

    if task.state == "SUCCESS":

        return jsonify({

            "status": "Completed",

            "file":
                f"exports/{os.path.basename(task.result)}"

        })

    elif task.state == "FAILURE":

        return jsonify({

            "status": "Failed",

            "error": str(task.result)

        }), 500

    return jsonify({

        "status": "Processing"

    })