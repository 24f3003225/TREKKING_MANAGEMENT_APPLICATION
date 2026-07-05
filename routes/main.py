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
