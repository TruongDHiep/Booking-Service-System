# -*- coding: utf-8 -*-
from datetime import datetime, timedelta
from odoo import _
from odoo.exceptions import ValidationError


class AppointmentService:
    def __init__(self, env):
        self.env = env
        self.Appointment = env["service.appointment"]

    def check_availability(self, service, booking_date, end_date, exclude_id=None):
        domain = [
            ("service_id", "=", service.id),
            ("state", "not in", ["cancel"]),
            "|",
            "&",
            ("booking_date", "<", end_date),
            ("end_date", ">", booking_date),
            "&",
            ("booking_date", "=", booking_date),
            ("end_date", "=", end_date),
        ]

        if exclude_id:
            domain.append(("id", "!=", exclude_id))

        overlapping = self.Appointment.search(domain)
        overlap_count = len(overlapping)

        max_capacity = service.max_concurrent_bookings

        if max_capacity == 0:
            return (False, None, None)

        if overlap_count >= max_capacity:
            if overlap_count == 1:
                error_msg = _(
                    "Time slot unavailable!\n\n"
                    "Conflicting appointment: %s\n"
                    'Service "%s" allows only %d booking at this time.'
                ) % (overlapping[0].reference, service.name, max_capacity)
            else:
                error_msg = _(
                    "Time slot fully booked!\n\n"
                    'Service "%s" capacity: %d/%d bookings\n'
                    "This slot is full. Please select another time."
                ) % (service.name, overlap_count, max_capacity)

            return (True, overlapping[0] if overlapping else None, error_msg)

        return (False, None, None)

    def get_upcoming_appointments(self, hours_ahead=24):
        now = datetime.now()
        future_time = now + timedelta(hours=hours_ahead)

        domain = [
            ("booking_date", ">=", now),
            ("booking_date", "<=", future_time),
            ("state", "in", ["confirmed"]),
        ]

        return self.Appointment.search(domain, order="booking_date asc")

    def get_recently_completed(self, hours_ago=24):
        now = datetime.now()
        past_time = now - timedelta(hours=hours_ago)

        domain = [
            ("end_date", ">=", past_time),
            ("end_date", "<=", now),
            ("state", "=", "done"),
        ]

        return self.Appointment.search(domain, order="end_date desc")

    def format_appointment_for_email(self, appointment):
        return {
            "reference": appointment.reference,
            "customer_name": appointment.customer_id.name,
            "customer_email": appointment.customer_id.email,
            "service_name": appointment.service_id.name,
            "booking_date": appointment.booking_date.strftime("%B %d, %Y at %I:%M %p")
            if appointment.booking_date
            else "",
            "duration": appointment.service_id.duration,
            "price": appointment.service_id.price,
            "currency": appointment.service_id.currency_id.symbol,
            "notes": appointment.notes or "",
            "portal_url": f"/my/appointments/{appointment.id}",
        }

    def validate_booking_time(self, booking_date):
        if booking_date < datetime.now():
            raise ValidationError(
                _(
                    "Cannot book appointments in the past. Please select a future date and time."
                )
            )
