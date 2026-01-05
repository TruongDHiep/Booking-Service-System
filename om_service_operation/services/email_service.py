# -*- coding: utf-8 -*-
from odoo import _
from odoo.exceptions import UserError
import logging

_logger = logging.getLogger(__name__)


class EmailService:
    def __init__(self, env):
        self.env = env
        from .appointment_service import AppointmentService

        self.appointment_service = AppointmentService(env)

    def send_confirmation_email(self, appointment):
        try:
            if not appointment.customer_id.email:
                _logger.warning(
                    f"Cannot send confirmation: No email for customer {appointment.customer_id.name}"
                )
                return False

            template = self.env.ref(
                "om_service_operation.email_booking_confirmation",
                raise_if_not_found=False,
            )

            if not template:
                _logger.error(
                    "Booking confirmation email template not found via XML ID"
                )
                return False

            template = template.sudo()
            template.send_mail(appointment.id, force_send=True)

            _logger.info(
                f"Confirmation email sent for appointment {appointment.reference} "
                f"to {appointment.customer_id.email}"
            )

            return True

        except Exception as e:
            _logger.error(f"Error sending confirmation email: {str(e)}")
            return False

    def send_reminder_emails(self):
        try:
            appointments = self.appointment_service.get_upcoming_appointments(
                hours_ahead=24
            )

            template = self.env.sudo().ref(
                "om_service_operation.email_appointment_reminder",
                raise_if_not_found=False,
            )

            if not template:
                _logger.error("Appointment reminder email template not found")
                return 0

            sent_count = 0

            for appointment in appointments:
                if appointment.reminder_sent:
                    continue

                if not appointment.customer_id.email:
                    _logger.warning(
                        f"Cannot send reminder for {appointment.reference}: "
                        f"No email for customer {appointment.customer_id.name}"
                    )
                    continue

                try:
                    template.send_mail(appointment.id, force_send=True)
                    appointment.write({"reminder_sent": True})

                    sent_count += 1

                    _logger.info(
                        f"Reminder email sent for appointment {appointment.reference} "
                        f"to {appointment.customer_id.email}"
                    )

                except Exception as e:
                    _logger.error(
                        f"Error sending reminder for {appointment.reference}: {str(e)}"
                    )
                    continue

            _logger.info(f"Reminder emails sent: {sent_count}/{len(appointments)}")
            return sent_count

        except Exception as e:
            _logger.error(f"Error in send_reminder_emails: {str(e)}")
            return 0

    def send_completion_notification(self, appointment):
        try:
            appointment.ensure_one()

            if appointment.completion_email_sent:
                _logger.info(
                    f"Completion email already sent for {appointment.reference}"
                )
                return False

            template = self.env.sudo().ref(
                "om_service_operation.email_completion_notification",
                raise_if_not_found=False,
            )

            if not template:
                _logger.error("Completion notification email template not found")
                return False

            if not appointment.customer_id.email:
                _logger.warning(
                    f"Cannot send completion email: No email for customer {appointment.customer_id.name}"
                )
                return False

            template.send_mail(appointment.id, force_send=True)
            appointment.write({"completion_email_sent": True})

            _logger.info(
                f"Completion email sent for appointment {appointment.reference} "
                f"to {appointment.customer_id.email}"
            )

            return True

        except Exception as e:
            _logger.error(f"Error sending completion email: {str(e)}")
            return False

    def send_completion_notifications_batch(self):
        try:
            appointments = self.appointment_service.get_recently_completed(hours_ago=24)

            template = self.env.sudo().ref(
                "om_service_operation.email_completion_notification",
                raise_if_not_found=False,
            )

            if not template:
                _logger.error("Completion notification email template not found")
                return 0

            sent_count = 0

            for appointment in appointments:
                if appointment.completion_email_sent:
                    continue

                if not appointment.customer_id.email:
                    _logger.warning(
                        f"Cannot send completion email for {appointment.reference}: "
                        f"No email for customer {appointment.customer_id.name}"
                    )
                    continue

                try:
                    template.send_mail(appointment.id, force_send=True)
                    appointment.write({"completion_email_sent": True})
                    sent_count += 1

                    _logger.info(
                        f"Completion email sent for appointment {appointment.reference} "
                        f"to {appointment.customer_id.email}"
                    )

                except Exception as e:
                    _logger.error(
                        f"Error sending completion email for {appointment.reference}: {str(e)}"
                    )
                    continue

            _logger.info(f"Completion emails sent: {sent_count}/{len(appointments)}")
            return sent_count

        except Exception as e:
            _logger.error(f"Error in send_completion_notifications_batch: {str(e)}")
            return 0
