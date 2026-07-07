import os

from flask import Flask, send_from_directory
from flask_cors import CORS
from flask_jwt_extended import JWTManager
from werkzeug.security import generate_password_hash

from config import Config
from extensions import cache, mail
from models import User, db

from routes.admin import admin_bp
from routes.auth import auth_bp
from routes.main import main_bp
from routes.staff import staff_bp
from routes.user import user_bp


app = Flask(__name__)

# Configuration
app.config.from_object(Config)

# Redis Cache Configuration
app.config["CACHE_TYPE"] = "RedisCache"
app.config["CACHE_REDIS_HOST"] = "localhost"
app.config["CACHE_REDIS_PORT"] = 6379
app.config["CACHE_DEFAULT_TIMEOUT"] = 300

# Initialize Extensions
CORS(app)

db.init_app(app)

jwt = JWTManager(app)

cache.init_app(app)
mail.init_app(app)

# Register Blueprints
app.register_blueprint(main_bp)
app.register_blueprint(auth_bp)
app.register_blueprint(admin_bp)
app.register_blueprint(user_bp)
app.register_blueprint(staff_bp)


def create_admin():

    admin = User.query.filter_by(
        role="admin"
    ).first()

    if not admin:

        admin = User(

            name="Admin",

            email="admin@gmail.com",

            password=generate_password_hash(
                "admin123"
            ),

            role="admin",

            active=True
        )

        db.session.add(admin)

        db.session.commit()

        print("Admin Created Successfully")

    else:

        print("Admin Already Exists")


with app.app_context():

    db.create_all()

    create_admin()


@app.route("/exports/<filename>")
def download_export(filename):

    return send_from_directory(
        os.path.join(
            app.root_path,
            "exports"
        ),
        filename,
        as_attachment=True
    )


if __name__ == "__main__":

    app.run(debug=True)