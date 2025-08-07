from odoo import models, fields

class FleetVehicle(models.Model):
    _name = 'fleet.vehicle'
    _description = 'Fleet Vehicles'

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
