from odoo import models, fields, api
from datetime import datetime, timedelta


class FleetVehicleRental(models.Model):
    _name = 'fleet.vehicle.rental'
    _description = 'Fleet Vehicle Rental'
    _order = 'start_date desc'

    name = fields.Char(string="Rental Reference", required=True, copy=False, readonly=True, default=lambda self: 'New')
    vehicle_id = fields.Many2one('fleet.vehicle', string='Vehicle', required=True)
    driver_id = fields.Many2one('res.partner', string='Driver/Customer', required=True)
    
    start_date = fields.Datetime(
        string="Start Date",
        default=lambda self: fields.Datetime.now()
    )
    end_date = fields.Datetime(
        string="End Date",
        default=lambda self: fields.Datetime.now() + timedelta(days=1)
    )    
    state = fields.Selection([
        ('draft', 'Draft'),
        ('rented', 'Rented'),
        ('returned', 'Returned'),
        ('cancelled', 'Cancelled'),
    ], string='Status', default='draft')
    notes = fields.Text(string="Notes")
    rental_days = fields.Integer(string="Total Days", compute="_compute_rental_days", store=True)
    cost = fields.Float(string="Rental Cost", compute="_compute_cost", store=True)

    @api.depends('start_date', 'end_date')
    def _compute_rental_days(self):
        for rec in self:
            if rec.start_date and rec.end_date:
                rec.rental_days = (rec.end_date - rec.start_date).days + 1
            else:
                rec.rental_days = 0

    @api.depends('rental_days', 'state')
    def _compute_cost(self):
        for rec in self:
            if rec.rental_days:
                rec.cost = rec.rental_days * rec.vehicle_id.daily_rate
            else:
                rec.cost = 0.0

    @api.model_create_multi
    def create(self, vals_list):
        for vals in vals_list:
            if vals.get('name', 'New') == 'New':
                vals['name'] = self.env['ir.sequence'].next_by_code('fleet.vehicle.rental') or 'New'
        return super().create(vals_list)
    
    def action_confirm(self):
        for record in self:
            record.state = 'rented'

    def action_cancel(self):
        for record in self:
            record.state = 'cancelled'

    def action_return(self):
        for rec in self:
            rec.state = 'returned'
