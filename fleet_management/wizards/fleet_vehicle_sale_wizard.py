from odoo import models, fields, api, _
from odoo.exceptions import UserError

class FleetVehicleSaleWizard(models.TransientModel):
    _name = 'fleet.vehicle.sale.wizard'
    _description = 'Mark Vehicles as Sold'

    reason = fields.Text(string="Reason for Sale", required=True)

    def action_mark_as_sold(self):
        active_ids = self.env.context.get('active_ids')
        vehicles = self.env['fleet.vehicle'].browse(active_ids)
        if not vehicles:
            raise UserError(_("No vehicles selected."))

        template = self.env.ref('fleet_management.email_template_vehicle_sold')

        for vehicle in vehicles:
            vehicle.status = 'sold'
            vehicle.message_post(
                body=_(
                    "Vehicle marked as Sold. Reason: %s"
                ) % (self.reason)
            )
            template.send_mail(vehicle.id, force_send=True)
