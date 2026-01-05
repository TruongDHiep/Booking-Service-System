# -*- coding: utf-8 -*-
from odoo import http, fields, _
from odoo.http import request
from odoo.exceptions import AccessError
from werkzeug.exceptions import Forbidden
from datetime import timedelta
from odoo.addons.portal.controllers.portal import CustomerPortal, pager as portal_pager


class CustomerPortalAppointments(CustomerPortal):
    def _prepare_home_portal_values(self, counters):
        """Add appointment count to portal home."""
        values = super()._prepare_home_portal_values(counters)

        if "appointment_count" in counters:
            partner = request.env.user.partner_id
            appointment_count = request.env["service.appointment"].search_count(
                [("customer_id", "=", partner.id)]
            )
            values["appointment_count"] = appointment_count

        return values

    @http.route(
        ["/my/appointments", "/my/appointments/page/<int:page>"],
        type="http",
        auth="user",
        website=True,
    )
    def portal_my_appointments(self, page=1, sortby=None, filterby=None, **kw):
        partner = request.env.user.partner_id
        Appointment = request.env["service.appointment"]

        domain = [("customer_id", "=", partner.id)]

        filter_options = {
            "all": {"label": _("All"), "domain": []},
            "upcoming": {
                "label": _("Upcoming"),
                "domain": [
                    ("booking_date", ">=", fields.Datetime.now()),
                    ("state", "!=", "cancel"),
                ],
            },
            "past": {
                "label": _("Past"),
                "domain": [("booking_date", "<", fields.Datetime.now())],
            },
            "confirmed": {
                "label": _("Confirmed"),
                "domain": [("state", "=", "confirmed")],
            },
        }

        if not filterby:
            filterby = "all"
        domain += filter_options.get(filterby, filter_options["all"])["domain"]

        sort_options = {
            "date_desc": {"label": _("Newest First"), "order": "booking_date desc"},
            "date_asc": {"label": _("Oldest First"), "order": "booking_date asc"},
            "name": {"label": _("Reference"), "order": "reference"},
        }

        if not sortby:
            sortby = "date_desc"
        order = sort_options.get(sortby, sort_options["date_desc"])["order"]

        appointment_count = Appointment.search_count(domain)

        pager = portal_pager(
            url="/my/appointments",
            total=appointment_count,
            page=page,
            step=10,
            url_args={"sortby": sortby, "filterby": filterby},
        )

        appointments = Appointment.search(
            domain, order=order, limit=10, offset=pager["offset"]
        )

        values = {
            "appointments": appointments,
            "page_name": "my_appointments",
            "default_url": "/my/appointments",
            "pager": pager,
            "sortby": sortby,
            "filterby": filterby,
            "sort_options": sort_options,
            "filter_options": filter_options,
        }

        return request.render("om_website_booking.portal_my_appointments", values)

    @http.route(
        ["/my/appointments/<int:appointment_id>"],
        type="http",
        auth="user",
        website=True,
    )
    def portal_appointment_detail(self, appointment_id, access_token=None, **kw):
        try:
            appointment_sudo = self._document_check_access(
                "service.appointment", appointment_id, access_token=access_token
            )
        except (AccessError, Forbidden):
            return request.redirect("/my")

        can_cancel = False
        time_until_appointment = None

        if appointment_sudo.state in ["draft", "confirmed"]:
            time_until_appointment = (
                appointment_sudo.booking_date - fields.Datetime.now()
            )
            can_cancel = time_until_appointment >= timedelta(days=1)

        values = {
            "appointment": appointment_sudo,
            "page_name": "appointment_detail",
            "can_cancel": can_cancel,
            "time_until_appointment": time_until_appointment,
            "error": kw.get("error"),
            "message": kw.get("message"),
        }

        return request.render("om_website_booking.portal_appointment_detail", values)

    @http.route(
        ["/my/appointments/<int:appointment_id>/cancel"],
        type="http",
        auth="user",
        methods=["POST"],
        website=True,
        csrf=True,
    )
    def portal_appointment_cancel(self, appointment_id, access_token=None, **kw):
        try:
            appointment_sudo = self._document_check_access(
                "service.appointment", appointment_id, access_token=access_token
            )
        except (AccessError, Forbidden):
            return request.redirect("/my")

        if appointment_sudo.state not in ["draft", "confirmed"]:
            return request.redirect(
                "/my/appointments/%s?error=invalid_state" % appointment_id
            )

        time_until_appointment = appointment_sudo.booking_date - fields.Datetime.now()

        if time_until_appointment < timedelta(days=1):
            return request.redirect(
                "/my/appointments/%s?error=too_late" % appointment_id
            )

        appointment_sudo.action_cancel()

        appointment_sudo.message_post(
            body=_("Cancelled by customer via portal."),
            subject=_("Appointment Cancelled"),
        )

        return request.redirect("/my/appointments?message=cancelled")
