from odoo import models, fields


class FleetVehicleTags(models.Model):
  _name = 'fleet.vehicle.tags'
  _description = 'Fleet Vehicle Tags'

  name = fields.Char()
