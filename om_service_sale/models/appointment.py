# -*- coding: utf-8 -*-
from odoo import models, fields, api, _
from odoo.exceptions import UserError, ValidationError


class ServiceAppointment(models.Model):
    _inherit = "service.appointment"

    sale_order_id = fields.Many2one(
        "sale.order",
        string="Sale Order",
        readonly=True,
        copy=False,
        help="Generated sale order for this appointment",
    )

    sale_order_count = fields.Integer(
        string="Sale Order Count",
        compute="_compute_sale_order_count",
        help="Number of sale orders linked to this appointment",
    )

    @api.depends("sale_order_id")
    def _compute_sale_order_count(self):
        """Compute the number of linked sale orders."""
        for record in self:
            record.sale_order_count = 1 if record.sale_order_id else 0

    def action_create_sale_order(self):
        self.ensure_one()

        if self.state != "confirmed":
            raise UserError(
                _(
                    "Only confirmed appointments can generate quotations.\n"
                    "Please confirm this appointment first."
                )
            )

        if self.sale_order_id:
            raise UserError(
                _(
                    "A quotation already exists for this appointment!\n"
                    "Sale Order: %s\n\n"
                    "Use the smart button to view it."
                )
                % self.sale_order_id.name
            )

        if not self.service_id.product_id:
            raise ValidationError(
                _(
                    'Cannot create quotation: Service "%s" is not linked to a product.\n\n'
                    "Please configure the Related Product in Service master data."
                )
                % self.service_id.name
            )

        SaleOrder = self.env["sale.order"]

        order_vals = {
            "partner_id": self.customer_id.id,
            "date_order": fields.Datetime.now(),
            "note": _("Generated from Appointment: %s\nBooking Date: %s")
            % (self.reference, self.booking_date),
        }

        sale_order = SaleOrder.create(order_vals)

        line_vals = {
            "product_id": self.service_id.product_id.id,
            "product_uom_qty": 1.0,
            "price_unit": self.service_id.price,
            "name": _("[%s] %s\nAppointment: %s\nDate: %s")
            % (
                self.service_id.product_id.default_code or "SERVICE",
                self.service_id.name,
                self.reference,
                self.booking_date.strftime("%Y-%m-%d %H:%M")
                if self.booking_date
                else "",
            ),
        }

        sale_order.write({"order_line": [fields.Command.create(line_vals)]})

        self.write({"sale_order_id": sale_order.id})

        self.message_post(
            body=_("Sale Order %s created from this appointment.") % sale_order.name,
            subject=_("Quotation Created"),
        )

        return {
            "name": _("Sale Order"),
            "type": "ir.actions.act_window",
            "res_model": "sale.order",
            "res_id": sale_order.id,
            "view_mode": "form",
            "target": "current",
        }

    def action_view_sale_order(self):
        self.ensure_one()

        if not self.sale_order_id:
            raise UserError(_("No sale order linked to this appointment."))

        return {
            "name": _("Sale Order"),
            "type": "ir.actions.act_window",
            "res_model": "sale.order",
            "res_id": self.sale_order_id.id,
            "view_mode": "form",
            "target": "current",
        }
