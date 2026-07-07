import os
from datetime import datetime, timedelta

import pandas as pd
from flask import Flask
from flask_mail import Message
from sqlalchemy import func

from celery_worker import celery
from config import Config
from extensions import mail
from models import Booking, Trek, User, db


def create_app():

    app = Flask(__name__)

    app.config.from_object(Config)

    db.init_app(app)

    mail.init_app(app)

    return app


@celery.task
def export_booking_history(user_id):

    app = create_app()

    with app.app_context():

        bookings = Booking.query.filter_by(
            user_id=user_id
        ).all()

        data = []

        for booking in bookings:

            trek = Trek.query.get(
                booking.trek_id
            )

            data.append({

                "Booking ID": booking.id,
                "Trek": trek.name,
                "Location": trek.location,
                "Difficulty": trek.difficulty,
                "Status": booking.status,
                "Payment": booking.payment_status,
                "Booking Date": booking.booking_date

            })

        os.makedirs(
            "exports",
            exist_ok=True
        )

        filename = f"exports/history_{user_id}.csv"

        df = pd.DataFrame(data)

        df.to_csv(
            filename,
            index=False
        )

        return filename


@celery.task
def daily_trek_reminder():

    app = create_app()

    with app.app_context():

        tomorrow = datetime.utcnow().date() + timedelta(days=1)

        bookings = Booking.query.filter_by(
            status="Booked"
        ).all()

        for booking in bookings:

            trek = Trek.query.get(
                booking.trek_id
            )

            if trek and trek.start_date == tomorrow:

                user = User.query.get(
                    booking.user_id
                )

                msg = Message(

                    subject="Trek Reminder",

                    recipients=[user.email]

                )

                msg.body = f"""
Hello {user.name},

Your trek starts tomorrow.

Trek: {trek.name}
Location: {trek.location}
Start Date: {trek.start_date}

Happy Trekking!

Regards,
Trekking Management System
"""

                mail.send(msg)

        return "Daily Reminder Sent"


@celery.task
def generate_monthly_report():

    app = create_app()

    with app.app_context():

        total_treks = Trek.query.count()

        total_participants = Booking.query.filter(
            Booking.status != "Cancelled"
        ).count()

        completed_treks = Booking.query.filter_by(
            status="Completed"
        ).count()

        cancelled_bookings = Booking.query.filter_by(
            status="Cancelled"
        ).count()

        popular_trek = db.session.query(

            Trek.name,

            func.count(
                Booking.id
            ).label("count")

        ).join(

            Booking,

            Trek.id == Booking.trek_id

        ).group_by(

            Trek.id

        ).order_by(

            func.count(
                Booking.id
            ).desc()

        ).first()

        report = {

            "total_treks": total_treks,

            "total_participants": total_participants,

            "completed_treks": completed_treks,

            "cancelled_bookings": cancelled_bookings,

            "popular_trek": (
                popular_trek[0]
                if popular_trek
                else "None"
            )

        }

        return report