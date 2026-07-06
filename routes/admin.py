from flask import Blueprint, jsonify, request, render_template
from flask_jwt_extended import jwt_required
from models import db, Trek, User, Booking
from werkzeug.security import generate_password_hash, check_password_hash
from extensions import cache
from tasks import daily_trek_reminder, generate_monthly_report
from celery_worker import celery


admin_bp = Blueprint(
    "admin",
    __name__,
    url_prefix="/admin"
)

@admin_bp.route("/create-trek", methods=["POST"])
@jwt_required()
def create_trek():

    data = request.get_json()

    from datetime import datetime

    start_date = datetime.strptime(
        data["start_date"],
        "%Y-%m-%d"
    ).date()

    end_date = datetime.strptime(
        data["end_date"],
        "%Y-%m-%d"
    ).date()

    trek = Trek(

        name=data["name"],
        location=data["location"],
        difficulty=data["difficulty"],
        duration=data["duration"],
        available_slots=data["available_slots"],
        description=data["description"],

        start_date=start_date,
        end_date=end_date,

        staff_id=data.get("staff_id"),

        status="Pending"
    )

    db.session.add(trek)
    db.session.commit()

    cache.clear()

    return jsonify({
        "success": True,
        "message": "Trek Created Successfully"
    }), 201

@admin_bp.route("/treks", methods=["GET"])
@jwt_required()
def get_treks():

    treks = Trek.query.all()

    return jsonify([
        {
            "id": trek.id,
            "name": trek.name,
            "location": trek.location,
            "difficulty": trek.difficulty,
            "duration": trek.duration,
            "available_slots": trek.available_slots,
            "status": trek.status,
            "staff_name":
                User.query.get(trek.staff_id).name
                if trek.staff_id
                else "Not Assigned"
        }
        for trek in treks
    ])


@admin_bp.route("/delete-trek/<int:id>", methods=["DELETE"])
@jwt_required()
def delete_trek(id):

    trek = Trek.query.get(id)

    if not trek:
        return jsonify({"message": "Trek not found"}), 404

    db.session.delete(trek)
    db.session.commit()

    cache.clear()

    return jsonify({
        "message": "Trek deleted successfully"
    })


@admin_bp.route("/trek/<int:id>", methods=["GET"])
@jwt_required()
def get_trek_by_id(id):

    trek = Trek.query.get_or_404(id)

    return jsonify({

        "id": trek.id,
        "name": trek.name,
        "location": trek.location,
        "difficulty": trek.difficulty,
        "duration": trek.duration,
        "available_slots": trek.available_slots,
        "description": trek.description,
        "staff_id": trek.staff_id

    })


@admin_bp.route("/update-trek/<int:id>", methods=["PUT"])
@jwt_required()
def update_trek(id):

    trek = Trek.query.get(id)

    if not trek:
        return jsonify({"message": "Trek not found"}), 404

    data = request.get_json()

    trek.name = data["name"]
    trek.location = data["location"]
    trek.difficulty = data["difficulty"]
    trek.duration = data["duration"]
    trek.available_slots = data["available_slots"]
    trek.description = data["description"]
    trek.staff_id = data["staff_id"]
    db.session.commit()

    cache.clear()

    return jsonify({
        "message": "Trek updated successfully"
    })

@admin_bp.route("/add-staff", methods=["POST"])
def add_staff():

    data = request.get_json()

    existing_staff = User.query.filter_by(
        email=data["email"]
    ).first()

    if existing_staff:
        return jsonify({
            "message": "Email already exists"
        }), 400

    staff = User(
        name=data["name"],
        email=data["email"],
        password=generate_password_hash(
            data["password"]
        ),
        phone=data["phone"],
        role="staff",
        active=True
    )

    db.session.add(staff)
    db.session.commit()

    return jsonify({
        "message": "Staff Added Successfully"
    })

@admin_bp.route("/staff", methods=["GET"])
def get_staff():

    search = request.args.get("search", "")

    query = User.query.filter_by(
        role="staff"
    )

    if search:

        query = query.filter(
            db.or_(
                User.name.ilike(f"%{search}%"),
                User.email.ilike(f"%{search}%"),
                User.id.like(f"%{search}%")
            )
        )

    staffs = query.all()

    return jsonify([
        {
            "id": staff.id,
            "name": staff.name,
            "email": staff.email,
            "phone": staff.phone,
            "active": staff.active
        }
        for staff in staffs
    ])

@admin_bp.route(
    "/deactivate-staff/<int:id>",
    methods=["PUT"]
)
def deactivate_staff(id):

    staff = User.query.get_or_404(id)

    staff.active = False

    db.session.commit()

    return jsonify({
        "message":
        "Staff Deactivated Successfully"
    })

@admin_bp.route(
    "/activate-staff/<int:id>",
    methods=["PUT"]
)
def activate_staff(id):

    staff = User.query.get_or_404(id)

    staff.active = True

    db.session.commit()

    return jsonify({
        "message": "Staff Activated Successfully"
    })

@admin_bp.route("/users", methods=["GET"])
def get_users():

    search = request.args.get("search", "")

    query = User.query.filter_by(
        role="user"
    )

    if search:

        query = query.filter(
            db.or_(
                User.name.ilike(f"%{search}%"),
                User.email.ilike(f"%{search}%")
            )
        )

    users = query.all()

    return jsonify([
        {
            "id": user.id,
            "name": user.name,
            "email": user.email,
            "phone": user.phone,
            "active": user.active
        }
        for user in users
    ])

@admin_bp.route(
    "/deactivate-user/<int:id>",
    methods=["PUT"]
)
def deactivate_user(id):

    user = User.query.get_or_404(id)

    user.active = False

    db.session.commit()

    return jsonify({
        "message": "User Deactivated Successfully"
    })

@admin_bp.route(
    "/activate-user/<int:id>",
    methods=["PUT"]
)
def activate_user(id):

    user = User.query.get_or_404(id)

    user.active = True

    db.session.commit()

    return jsonify({
        "message": "User Activated Successfully"
    })

@admin_bp.route("/staff-list", methods=["GET"])
def staff_list():

    staffs = User.query.filter_by(
        role="staff",
        active=True
    ).all()

    return jsonify([
        {
            "id": staff.id,
            "name": staff.name
        }
        for staff in staffs
    ])

@admin_bp.route("/bookings", methods=["GET"])
def get_bookings():

    bookings = Booking.query.all()

    data = []

    for booking in bookings:

        user = User.query.get(
            booking.user_id
        )

        trek = Trek.query.get(
            booking.trek_id
        )

        data.append({

            "id": booking.id,

            "user_name":
                user.name,

            "trek_name":
                trek.name,

            "booking_date":
                booking.booking_date.strftime(
                    "%d-%m-%Y"
                ),

            "status":
                booking.status,

            "payment_status":
                booking.payment_status
        })

    return jsonify(data)

from tasks import daily_trek_reminder

@admin_bp.route("/run-reminder")
def run_reminder():

    daily_trek_reminder.delay()

    return {
        "message": "Reminder Job Started"
    }

@admin_bp.route(
    "/send-reminders",
    methods=["GET", "POST"]
)
@jwt_required()
def send_reminders():

    task = daily_trek_reminder.delay()

    return jsonify({

        "message": "Daily reminder started",

        "task_id": task.id

    })

from celery.result import AsyncResult

@admin_bp.route(
    "/monthly-report",
    methods=["POST"]
)
def monthly_report():

    task = generate_monthly_report.delay()

    return jsonify({

        "message": "Report Generation Started",

        "task_id": task.id

    })

@admin_bp.route(
    "/report-status/<task_id>"
)
def report_status(task_id):

    task = celery.AsyncResult(task_id)

    if task.ready():

        return jsonify({

            "status": "Completed",

            "report": task.result

        })

    return jsonify({

        "status": "Processing"

    })

@admin_bp.route("/monthly-report-page")
def monthly_report_page():

    return render_template(
        "monthly_report.html"
    )

from flask_mail import Message
from extensions import mail

