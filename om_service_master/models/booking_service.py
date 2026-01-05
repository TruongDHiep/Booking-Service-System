# -*- coding: utf-8 -*-
from odoo import models, fields, api, _
from odoo.exceptions import ValidationError


class BookingService(models.Model):
    _name = "booking.service"
    _description = "Booking Service"
    _order = "name"
    _rec_name = "name"

    name = fields.Char(
        string="Service Name",
        required=True,
        index=True,
        help="Name of the service offered to customers",
    )

    image = fields.Image(
        string="Service Image",
        max_width=1024,
        max_height=1024,
        help="Representative image for the service (displayed on website)",
    )

    duration = fields.Float(
        string="Duration (Hours)",
        default=1.0,
        required=True,
        help="Time required to complete the service in hours",
    )

    price = fields.Monetary(
        string="Price",
        currency_field="currency_id",
        required=True,
        help="Standard price for this service",
    )

    currency_id = fields.Many2one(
        "res.currency",
        string="Currency",
        default=lambda self: self.env.company.currency_id,
        required=True,
    )

    # Product Integration (for Sales)
    product_id = fields.Many2one(
        "product.product",
        string="Related Product",
        required=False,
        domain="[('type', '=', 'service')]",
        help="Link this service to a product for sales order generation",
    )

    max_concurrent_bookings = fields.Integer(
        string="Max Concurrent Bookings",
        default=1,
        help="Maximum number of appointments that can be booked at the same time slot.\n"
        "• 1 = Exclusive booking (e.g., Hotel Room, Private Consultation)\n"
        "• >1 = Multiple bookings allowed (e.g., Spa with 3 therapists, Class with 10 seats)\n"
        "• 0 = Unlimited (no restriction)",
    )

    active = fields.Boolean(
        string="Active",
        default=True,
        help="Uncheck to archive the service without deleting it",
    )

    description = fields.Text(
        string="Description", help="Detailed description of the service"
    )

    # Service Detail Page Fields
    slug = fields.Char(
        string="URL Slug",
        compute="_compute_slug",
        store=True,
        index=True,
        help="SEO-friendly URL slug generated from service name",
    )

    description_html = fields.Html(
        string="Detailed Description",
        help="Rich text description displayed on service detail page",
    )

    duration_display = fields.Char(
        string="Duration Display",
        compute="_compute_duration_display",
        store=True,
        help='Human-readable duration format (e.g., "50m", "1h30")',
    )

    # Computed Methods
    @api.depends("duration")
    def _compute_duration_display(self):
        """Format duration as human-readable text."""
        for record in self:
            if not record.duration:
                record.duration_display = "0m"
                continue

            hours = int(record.duration)
            minutes = int((record.duration - hours) * 60)

            if hours > 0 and minutes > 0:
                record.duration_display = f"{hours}h{minutes:02d}"
            elif hours > 0:
                record.duration_display = f"{hours}h"
            else:
                record.duration_display = f"{minutes}m"

    @api.depends("name")
    def _compute_slug(self):
        """Generate URL-friendly slug from service name."""
        for record in self:
            if record.name:
                slug = record.name.lower()
                slug = slug.replace(" ", "-")
                import re

                slug = re.sub(r"[^a-z0-9\-]", "", slug)
                slug = re.sub(r"-+", "-", slug)
                slug = slug.strip("-")

                base_slug = slug
                counter = 1
                while self.search(
                    [("slug", "=", slug), ("id", "!=", record.id)], limit=1
                ):
                    slug = f"{base_slug}-{counter}"
                    counter += 1

                record.slug = slug
            else:
                record.slug = False

    def get_detail_url(self):
        """Get the URL for service detail page."""
        self.ensure_one()
        return f"/booking/service/{self.slug}" if self.slug else "#"

    # CRUD Methods
    @api.model_create_multi
    def create(self, vals_list):
        """Override create to auto-create product if not provided."""
        for vals in vals_list:
            if not vals.get("product_id"):
                product = self.env["product.product"].create(
                    {
                        "name": vals.get("name", "Service"),
                        "type": "service",
                        "list_price": vals.get("price", 0.0),
                        "sale_ok": True,
                        "purchase_ok": False,
                    }
                )
                vals["product_id"] = product.id

        return super().create(vals_list)

    def write(self, vals):
        """Override write to auto-create product if not provided."""
        for record in self:
            if not record.product_id and not vals.get("product_id"):
                product = self.env["product.product"].create(
                    {
                        "name": vals.get("name", record.name),
                        "type": "service",
                        "list_price": vals.get("price", record.price),
                        "sale_ok": True,
                        "purchase_ok": False,
                    }
                )
                vals["product_id"] = product.id

            if "price" in vals and record.product_id:
                record.product_id.write({"list_price": vals["price"]})

        return super().write(vals)

    @api.constrains("duration")
    def _check_duration(self):
        """Ensure duration is positive."""
        for record in self:
            if record.duration <= 0:
                raise ValidationError(
                    _("Service duration must be greater than 0 hours.")
                )

    @api.constrains("price")
    def _check_price(self):
        """Ensure price is non-negative."""
        for record in self:
            if record.price < 0:
                raise ValidationError(_("Service price cannot be negative."))
