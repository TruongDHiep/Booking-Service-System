# -*- coding: utf-8 -*-
from odoo import http, _
from odoo.http import request
from datetime import datetime


class WebsiteBookingController(http.Controller):
    @http.route("/booking", type="http", auth="public", website=True, sitemap=True)
    def booking_service_list(self, **kwargs):
        services = (
            request.env["booking.service"]
            .sudo()
            .search([("active", "=", True)], order="name")
        )

        values = {
            "services": services,
            "page_name": "service_booking",
        }

        return request.render("om_website_booking.service_catalog", values)

    @http.route(
        "/booking/service/<string:slug>",
        type="http",
        auth="public",
        website=True,
        sitemap=True,
    )
    def service_detail(self, slug, **kwargs):
        service = (
            request.env["booking.service"]
            .sudo()
            .search([("slug", "=", slug), ("active", "=", True)], limit=1)
        )

        if not service:
            return request.render("website.404")

        related_services = (
            request.env["booking.service"]
            .sudo()
            .search(
                [("id", "!=", service.id), ("active", "=", True)], limit=3, order="name"
            )
        )

        values = {
            "service": service,
            "related_services": related_services,
            "page_name": "service_detail",
            "breadcrumbs": [
                {"name": "Home", "url": "/"},
                {"name": "Services", "url": "/booking"},
                {"name": service.name, "url": f"/booking/service/{slug}"},
            ],
        }

        return request.render("om_website_booking.service_detail", values)

    @http.route(
        "/booking/service/<int:service_id>", type="http", auth="public", website=True
    )
    def booking_service_detail(self, service_id, **kwargs):
        service = request.env["booking.service"].sudo().browse(service_id)

        if not service.exists() or not service.active:
            return request.redirect("/booking")

        values = {
            "service": service,
            "page_name": "service_booking_form",
        }

        return request.render("om_website_booking.booking_form", values)

    @http.route(
        "/booking/create",
        type="http",
        auth="public",
        methods=["POST"],
        website=True,
        csrf=True,
    )
    def booking_create(self, **post):
        try:
            required_fields = [
                "service_id",
                "customer_name",
                "customer_email",
                "customer_phone",
                "booking_date",
            ]

            errors = []
            for field in required_fields:
                if not post.get(field):
                    errors.append(_("Missing required field: %s") % field)

            if errors:
                return request.render(
                    "om_website_booking.booking_error",
                    {
                        "errors": errors,
                        "page_name": "booking_error",
                    },
                )

            try:
                import logging
                import pytz

                _logger = logging.getLogger(__name__)

                raw_date_string = post.get("booking_date")

                if _logger.isEnabledFor(logging.DEBUG):
                    _logger.debug("Timezone conversion - Input: %s", raw_date_string)

                user_tz = request.env.user.tz or "Asia/Ho_Chi_Minh"
                timezone = pytz.timezone(user_tz)

                booking_date_local_naive = datetime.strptime(
                    raw_date_string, "%Y-%m-%dT%H:%M"
                )

                booking_date_local = timezone.localize(booking_date_local_naive)

                booking_date_utc = booking_date_local.astimezone(pytz.UTC)

                booking_date = booking_date_utc.replace(tzinfo=None)

                if _logger.isEnabledFor(logging.DEBUG):
                    _logger.debug(
                        "Timezone conversion - Local: %s (%s), UTC: %s",
                        booking_date_local_naive,
                        user_tz,
                        booking_date,
                    )

            except ValueError:
                return request.render(
                    "om_website_booking.booking_error",
                    {
                        "errors": [_("Invalid date format")],
                        "page_name": "booking_error",
                    },
                )

            if booking_date < datetime.now():
                return request.render(
                    "om_website_booking.booking_error",
                    {
                        "errors": [
                            _(
                                "Cannot book appointments in the past. Please select a future date and time."
                            )
                        ],
                        "page_name": "booking_error",
                    },
                )

            import re

            phone = post.get("customer_phone", "").strip()
            phone_number = phone.split()[-1] if " " in phone else phone

            if not re.match(r"^\+?\d{1,4}\s?\d{7,15}$", phone) and not re.match(
                r"^\d{7,15}$", phone_number
            ):
                return request.render(
                    "om_website_booking.booking_error",
                    {
                        "errors": [
                            _(
                                "Invalid phone number format. Please enter a valid phone number with digits only."
                            )
                        ],
                        "page_name": "booking_error",
                    },
                )

            Partner = request.env["res.partner"].sudo()
            customer = Partner.search(
                [("email", "=", post.get("customer_email"))], limit=1
            )

            if not customer:
                customer = Partner.create(
                    {
                        "name": post.get("customer_name"),
                        "email": post.get("customer_email"),
                        "phone": post.get("customer_phone"),
                    }
                )
            else:
                if customer.phone != post.get("customer_phone"):
                    customer.write(
                        {
                            "phone": post.get("customer_phone"),
                            "name": post.get("customer_name"),
                        }
                    )

            Appointment = request.env["service.appointment"].sudo()

            from datetime import timedelta

            service = (
                request.env["booking.service"]
                .sudo()
                .browse(int(post.get("service_id")))
            )
            end_date = booking_date + timedelta(hours=service.duration)

            has_overlap, overlapping, error_msg = Appointment.check_overlap(
                booking_date=booking_date, end_date=end_date, service_id=service.id
            )

            if has_overlap:
                return request.render(
                    "om_website_booking.booking_error",
                    {
                        "errors": [error_msg],
                        "page_name": "booking_error",
                    },
                )

            try:
                appointment = Appointment.create(
                    {
                        "customer_id": customer.id,
                        "service_id": int(post.get("service_id")),
                        "booking_date": booking_date,
                        "notes": post.get("notes", ""),
                        "state": "draft",
                    }
                )

                if _logger.isEnabledFor(logging.DEBUG):
                    _logger.debug(
                        "Sending confirmation email for appointment %s",
                        appointment.reference,
                    )
                try:
                    from odoo.addons.om_service_operation.services.email_service import (
                        EmailService,
                    )

                    email_service = EmailService(request.env)
                    result = email_service.send_confirmation_email(appointment)

                    if _logger.isEnabledFor(logging.DEBUG):
                        _logger.debug(
                            "Confirmation email sent successfully: %s", result
                        )

                except Exception as email_error:
                    import traceback

                    _logger.error(
                        "Failed to send confirmation email for appointment %s: %s",
                        appointment.reference,
                        str(email_error),
                    )
                    if _logger.isEnabledFor(logging.DEBUG):
                        _logger.debug(
                            "Email error traceback:\n%s", traceback.format_exc()
                        )

                return request.redirect("/booking/success/%s" % appointment.id)

            except Exception as e:
                from odoo.exceptions import ValidationError

                error_message = str(e)

                if (
                    isinstance(e, ValidationError)
                    or "conflicts" in error_message.lower()
                    or "ValidationError" in str(type(e))
                ):
                    errors = [
                        _(
                            "The selected time slot is not available. Please choose a different time."
                        )
                    ]

                    if "conflicts" in error_message.lower():
                        errors = [
                            error_message.split("\n")[0]
                        ]  # Get first line of error
                else:
                    errors = [
                        _(
                            "An error occurred while creating your booking. Please try again."
                        )
                    ]

                return request.render(
                    "om_website_booking.booking_error",
                    {
                        "errors": errors,
                        "page_name": "booking_error",
                    },
                )

        except Exception as e:
            error_message = str(e)
            errors = [_("An unexpected error occurred: %s") % error_message]

            return request.render(
                "om_website_booking.booking_error",
                {
                    "errors": errors,
                    "page_name": "booking_error",
                },
            )

    @http.route(
        "/booking/success/<int:appointment_id>",
        type="http",
        auth="public",
        website=True,
    )
    def booking_success(self, appointment_id, **kwargs):
        appointment = request.env["service.appointment"].sudo().browse(appointment_id)

        if not appointment.exists():
            return request.redirect("/booking")

        values = {
            "appointment": appointment,
            "page_name": "booking_success",
        }

        return request.render("om_website_booking.booking_success", values)
