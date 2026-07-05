import os

from flask import Flask
from flask_jwt_extended import JWTManager
from werkzeug.security import generate_password_hash

from config import Config
from models import User, db

app = Flask(__name__)

app.config.from_object(Config)

app.config["CACHE_TYPE"] = "RedisCache"
app.config["CACHE_REDIS_HOST"] = "localhost"
app.config["CACHE_REDIS_PORT"] = 6379
app.config["CACHE_DEFAULT_TIMEOUT"] = 300

db.init_app(app)

jwt = JWTManager(app)

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


if __name__ == "__main__":

    app.run(debug=True)