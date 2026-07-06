from flask import Blueprint, render_template
from models import User, Trek, Booking

main_bp = Blueprint("main", __name__)

@main_bp.route("/")
def home():
        return render_template("home.html")

@main_bp.route("/register")
def register_page():
    return render_template("register.html")

@main_bp.route("/login")
def login_page():
    return render_template("login.html")

@main_bp.route("/admin/dashboard")
def admin_dashboard():

    total_users = User.query.filter_by(role="user").count()

    total_treks = Trek.query.count()

    total_bookings = Booking.query.count()

    return render_template(
        "admin_dash.html",
        total_users=total_users,
        total_treks=total_treks,
        total_bookings=total_bookings
)

@main_bp.route("/admin/create-trek")
def create_trek_page():
    return render_template("create_trek.html")

@main_bp.route("/admin/treks-page")
def treks_page():
    return render_template("treks.html")

@main_bp.route("/admin/edit-trek/<int:id>")
def edit_trek_page(id):
    return render_template("edit_trek.html")

@main_bp.route("/admin/add-staff")
def add_staff_page():
    return render_template("add_staff.html")

@main_bp.route("/admin/staff-page")
def staff_page():
    return render_template("staff.html")

@main_bp.route("/admin/users-page")
def users_page():
    return render_template("users.html")

@main_bp.route("/admin/bookings-page")
def admin_bookings_page():
    return render_template("bookings.html")