from flask import Blueprint, request, jsonify, render_template
from werkzeug.security import generate_password_hash, check_password_hash
from flask_jwt_extended import create_access_token
from models import db, User

auth_bp = Blueprint("auth",__name__,url_prefix="/auth")

@auth_bp.route("/register", methods=["POST"])
def register():

    data = request.get_json()

    name = data.get("name")
    email = data.get("email")
    password = data.get("password")
    phone = data.get("phone")

    if not name or not email or not password:
        return jsonify({
            "success": False,
            "message": "All fields are required"
        }), 400

    existing_user = User.query.filter_by(
        email=email
    ).first()

    if existing_user:
        return jsonify({
            "success": False,
            "message": "Email already registered"
        }), 400

    user = User(
        name=name,
        email=email,
        password=generate_password_hash(password),
        phone=phone,
        role="user",
        active=True
    )

    db.session.add(user)
    db.session.commit()

    return jsonify({
        "success": True,
        "message": "Registration successful"
    }), 201

@auth_bp.route("/login", methods=["POST"])
def login():

    data = request.get_json()

    email = data.get("email")
    password = data.get("password")

    if not email or not password:
        return jsonify({
            "success": False,
            "message": "Email and Password are required"
        }), 400

    user = User.query.filter_by(
        email=email
    ).first()

    if not user:
        return jsonify({
            "success": False,
            "message": "Invalid Email or Password"
        }), 401

    if not check_password_hash(
        user.password,
        password
    ):
        return jsonify({
            "success": False,
            "message": "Invalid Email or Password"
        }), 401

    if not user.active:
        return jsonify({
            "success": False,
            "message": "Account is deactivated"
        }), 403

    access_token = create_access_token(
        identity=str(user.id)
    )

    return jsonify({
        "success": True,
        "message": "Login Successful",
        "token": access_token,
        "user": {
            "id": user.id,
            "name": user.name,
            "email": user.email,
            "role": user.role
        }
    }), 200