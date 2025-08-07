from odoo import models, fields, api


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

    @api.model_create_multi
    def create(self, vals_list):
        for vals in vals_list:
            if vals.get('name', 'New') == 'New':
                vals['name'] = self.env['ir.sequence'].next_by_code('fleet.vehicle.rental') or 'New'
        return super().create(vals_list)
    