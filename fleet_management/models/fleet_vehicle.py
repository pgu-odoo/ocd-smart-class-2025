from odoo import api, models, fields
from datetime import timedelta, date
from odoo.exceptions import ValidationError


class FleetVehicle(models.Model):
    _name = 'fleet.vehicle'
    _description = 'Fleet Vehicles'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _order = 'id desc'

    name = fields.Char(required=True)
    brand = fields.Char()
    model = fields.Char()
    license_plate = fields.Char()
    purchase_date = fields.Date(copy=False)
    last_service_date = fields.Date(string="Last Service Date")
    service_interval_days = fields.Integer(default=180)
    odometer_km = fields.Float()
    status = fields.Selection([
        ('active', 'Active'),
        ('sold', 'Sold')
        ], default='active', readonly=True)
    maintenance_cost = fields.Float()
    image = fields.Image(string="Photo")
    driver_id = fields.Many2one(
        'res.partner',
        string="Driver"
        )
    company_id = fields.Many2one('res.company')
    tag_ids = fields.Many2many('fleet.vehicle.tags')
    order_ids = fields.One2many('fleet.vehicle.rental', 'vehicle_id')
    vehicle_age_years = fields.Float(string='Vehicle Age (Years)', compute='_compute_vehicle_age')
    daily_rate = fields.Float(string="Daily Rate")


    _check_percentage = models.Constraint(
       'CHECK(odometer_km > 0)',
       'The Odometer should be greater than 0.',
    )

    @api.constrains('purchase_date')
    def _check_purchase_date(self):
        for record in self:
            if record.purchase_date and record.purchase_date > fields.Date.today():
                raise ValidationError("Purchase date cannot be in the future.")

    @api.depends('purchase_date')
    def _compute_vehicle_age(self):
        for record in self:
            if record.purchase_date:
                delta = date.today() - record.purchase_date
                record.vehicle_age_years = round(delta.days / 365.0, 2)
            else:
                record.vehicle_age_years = 0.0

    def action_open_related_orders(self):
        return {
            'type': 'ir.actions.act_window',
            'name': 'Rental Orders',
            'res_model': 'fleet.vehicle.rental',
            'view_mode': 'list,form',
            'domain': [('vehicle_id', '=', self.id)],
        }