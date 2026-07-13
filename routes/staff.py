from flask import Blueprint, jsonify, request
from flask_jwt_extended import jwt_required, get_jwt_identity
from models import Trek, Booking, User, db
from extensions import cache

staff_bp = Blueprint(
    "staff",
    __name__,
    url_prefix="/staff"
)


@staff_bp.route("/dashboard-data")
@jwt_required()
@cache.cached(timeout=120)
def dashboard_data():

    staff_id = int(get_jwt_identity())

    total_treks = Trek.query.filter_by(
        staff_id=staff_id
    ).count()

    total_bookings = Booking.query.join(
        Trek
    ).filter(
        Trek.staff_id == staff_id,
        Booking.status != "Cancelled"
    ).count()

    return jsonify({
        "total_treks": total_treks,
        "total_bookings": total_bookings
    })


@staff_bp.route("/my-treks")
@jwt_required()
def my_treks():

    staff_id = int(get_jwt_identity())

    treks = Trek.query.filter_by(
        staff_id=staff_id
    ).all()

    return jsonify([
        {
            "id": trek.id,
            "name": trek.name,
            "location": trek.location,
            "difficulty": trek.difficulty,
            "duration": trek.duration,
            "available_slots": trek.available_slots,
            "status": trek.status
        }
        for trek in treks
    ])


@staff_bp.route("/participants/<int:trek_id>")
@jwt_required()
def participants(trek_id):

    staff_id = int(get_jwt_identity())

    trek = Trek.query.filter_by(
        id=trek_id,
        staff_id=staff_id
    ).first()

    if not trek:
        return jsonify({
            "message": "Unauthorized Access"
        }), 403

    bookings = Booking.query.filter(
        Booking.trek_id == trek_id,
        Booking.status != "Cancelled"
    ).all()

    result = []

    for booking in bookings:

        user = User.query.get(
            booking.user_id
        )

        result.append({
            "user_id": user.id,
            "name": user.name,
            "email": user.email,
            "phone": user.phone,
            "booking_status": booking.status
        })

    return jsonify(result)


@staff_bp.route("/trek/<int:trek_id>")
@jwt_required()
def get_trek(trek_id):

    staff_id = int(get_jwt_identity())

    trek = Trek.query.filter_by(
        id=trek_id,
        staff_id=staff_id
    ).first()

    if not trek:
        return jsonify({
            "message": "Unauthorized Access"
        }), 403

    return jsonify({
        "id": trek.id,
        "name": trek.name,
        "location": trek.location,
        "status": trek.status,
        "available_slots": trek.available_slots
    })


@staff_bp.route(
    "/update-status/<int:trek_id>",
    methods=["PUT"]
)
@jwt_required()
def update_status(trek_id):

    staff_id = int(
        get_jwt_identity()
    )

    trek = Trek.query.filter_by(
        id=trek_id,
        staff_id=staff_id
    ).first()

    if not trek:

        return jsonify({
            "message":
            "Unauthorized Access"
        }), 403

    data = request.get_json()

    allowed_statuses = [

        "Pending",

        "Approved",

        "Open",

        "Closed",

        "Started",

        "Ongoing",

        "Completed"
    ]

    if data["status"] not in allowed_statuses:

        return jsonify({
            "message":
            "Invalid Status"
        }), 400

    trek.status = data["status"]


    if trek.status == "Completed":

        bookings = Booking.query.filter_by(
            trek_id=trek.id,
            status="Booked"
        ).all()

        for booking in bookings:

            booking.status = "Completed"

    db.session.commit()

    cache.clear()

    return jsonify({
        "message":
        "Status Updated Successfully"
    })

@staff_bp.route(
    "/update-slots/<int:trek_id>",
    methods=["PUT"]
)
@jwt_required()
def update_slots(trek_id):

    staff_id = int(
        get_jwt_identity()
    )

    trek = Trek.query.filter_by(
        id=trek_id,
        staff_id=staff_id
    ).first()

    if not trek:

        return jsonify({
            "message":
            "Unauthorized Access"
        }), 403

    data = request.get_json()

    trek.available_slots = int(
        data["available_slots"]
    )

    db.session.commit()
    cache.clear()

    return jsonify({
        "message":
        "Slots Updated Successfully"
    })