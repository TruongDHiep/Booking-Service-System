# -*- coding: utf-8 -*-
from odoo import models, fields, api, _
from odoo.exceptions import ValidationError
from datetime import timedelta
import logging

_logger = logging.getLogger(__name__)


class ServiceAppointment(models.Model):
    _name = "service.appointment"
    _description = "Service Appointment"
    _inherit = ["mail.thread", "mail.activity.mixin", "portal.mixin"]
    _order = "booking_date desc, id desc"
    _rec_name = "reference"

    reference = fields.Char(
        string="Appointment Reference",
        required=True,
        readonly=True,
        copy=False,
        default="New",
        help="Unique identifier for this appointment",
    )

    # Customer Information
    customer_id = fields.Many2one(
        "res.partner",
        string="Customer",
        required=True,
        tracking=True,
        help="Customer who booked this appointment",
    )

    customer_phone = fields.Char(
        related="customer_id.phone", string="Phone", readonly=True, store=False
    )

    customer_email = fields.Char(
        related="customer_id.email", string="Email", readonly=True, store=False
    )

    service_id = fields.Many2one(
        "booking.service",
        string="Service",
        required=True,
        tracking=True,
        help="Service to be performed",
    )

    booking_date = fields.Datetime(
        string="Start Date & Time",
        required=True,
        tracking=True,
        help="When the service appointment starts",
    )

    duration = fields.Float(
        related="service_id.duration",
        string="Duration (Hours)",
        readonly=True,
        store=True,
        help="Duration of the service in hours",
    )

    end_date = fields.Datetime(
        string="End Date & Time",
        compute="_compute_end_date",
        store=True,
        help="Calculated end time based on start time and duration",
    )

    price = fields.Monetary(
        related="service_id.price", string="Service Price", readonly=True, store=True
    )

    currency_id = fields.Many2one(
        related="service_id.currency_id", string="Currency", readonly=True, store=True
    )

    state = fields.Selection(
        [
            ("draft", "Draft"),
            ("confirmed", "Confirmed"),
            ("done", "Done"),
            ("cancel", "Cancelled"),
        ],
        string="Status",
        default="draft",
        required=True,
        tracking=True,
        help="Current status of the appointment",
    )

    notes = fields.Text(string="Notes", help="Additional notes or special requirements")

    reminder_sent = fields.Boolean(
        string="Reminder Sent",
        default=False,
        help="Indicates if 24-hour reminder email was sent",
        copy=False,
    )

    completion_email_sent = fields.Boolean(
        string="Completion Email Sent",
        default=False,
        help="Indicates if completion notification email was sent",
        copy=False,
    )

    is_past = fields.Boolean(
        string="Is Past Appointment", compute="_compute_is_past", store=False
    )

    @api.depends("booking_date", "duration")
    def _compute_end_date(self):
        """Calculate end date based on booking date and duration."""
        for record in self:
            if record.booking_date and record.duration:
                record.end_date = record.booking_date + timedelta(hours=record.duration)
            else:
                record.end_date = False

    @api.depends("booking_date")
    def _compute_is_past(self):
        """Check if appointment is in the past."""
        now = fields.Datetime.now()
        for record in self:
            record.is_past = record.booking_date < now if record.booking_date else False

    def check_overlap(self, booking_date, end_date, service_id, exclude_id=None):
        if not booking_date or not end_date:
            return (False, None, None)

        from odoo.addons.om_service_operation.services.appointment_service import (
            AppointmentService,
        )

        service = self.env["booking.service"].browse(service_id)

        appointment_service = AppointmentService(self.env)
        return appointment_service.check_availability(
            service=service,
            booking_date=booking_date,
            end_date=end_date,
            exclude_id=exclude_id,
        )

    @api.constrains("booking_date")
    def _check_past_date(self):
        for record in self:
            if record.booking_date and record.booking_date < fields.Datetime.now():
                raise ValidationError(
                    _(
                        "Cannot create appointments in the past.\n"
                        "Please select a future date and time."
                    )
                )

    # CRUD Overrides
    @api.model_create_multi
    def create(self, vals_list):
        """Override create to generate sequence number."""
        for vals in vals_list:
            if vals.get("reference", "New") == "New":
                vals["reference"] = (
                    self.env["ir.sequence"].next_by_code("service.appointment") or "New"
                )

        records = super(ServiceAppointment, self).create(vals_list)

        for record in records:
            record.message_post(
                body=_("Appointment created for %s") % record.service_id.name,
                subject=_("New Appointment"),
            )

        return records

    def action_confirm(self):
        """Confirm the appointment."""
        for record in self:
            if record.state != "draft":
                continue

            record.write({"state": "confirmed"})
            record.message_post(
                body=_("Appointment confirmed"), subject=_("Appointment Confirmed")
            )

    def action_done(self):
        """Mark appointment as done and send completion email."""
        for record in self:
            if record.state != "confirmed":
                continue

            record.write({"state": "done"})
            record.message_post(
                body=_("Appointment completed"), subject=_("Appointment Completed")
            )

            try:
                from odoo.addons.om_service_operation.services.email_service import (
                    EmailService,
                )

                email_service = EmailService(self.env)
                email_service.send_completion_notification(record)
            except Exception as e:
                import logging

                _logger = logging.getLogger(__name__)
                _logger.error(
                    f"Failed to send completion email for {record.reference}: {str(e)}"
                )

    def action_cancel(self):
        """Cancel the appointment."""
        for record in self:
            if record.state in ["done", "cancel"]:
                continue

            record.write({"state": "cancel"})
            record.message_post(
                body=_("Appointment cancelled"), subject=_("Appointment Cancelled")
            )

    def _cron_send_reminders(self):
        """Cron job to send appointment reminder emails."""
        from odoo.addons.om_service_operation.services.email_service import EmailService

        email_service = EmailService(self.env)
        count = email_service.send_reminder_emails()
        _logger.info(f"Cron: Sent {count} reminder emails")

    def _cron_send_completions(self):
        """Cron job to send completion notification emails."""
        from odoo.addons.om_service_operation.services.email_service import EmailService

        email_service = EmailService(self.env)
        count = email_service.send_completion_notifications_batch()
        _logger.info(f"Cron: Sent {count} completion emails")

    def action_set_to_draft(self):
        """Reset appointment to draft."""
        for record in self:
            record.write({"state": "draft"})
            record.message_post(
                body=_("Appointment reset to draft"), subject=_("Appointment Reset")
            )

    def _compute_access_url(self):
        """Compute portal access URL."""
        super()._compute_access_url()
        for appointment in self:
            appointment.access_url = "/my/appointments/%s" % appointment.id

    def _get_portal_return_action(self):
        """Return action after portal operations."""
        self.ensure_one()
        return {
            "type": "ir.actions.act_url",
            "url": "/my/appointments",
            "target": "self",
        }

    def name_get(self):
        """Custom name display."""
        result = []
        for record in self:
            name = f"{record.reference} - {record.customer_id.name} - {record.service_id.name}"
            result.append((record.id, name))
        return result
