from odoo import api, fields, models

class Meeting(models.Model):
    _inherit = ["calendar.event"]

    level10_id = fields.Many2one(comodel_name='traction.level10',
                                 string='Level 10',
                                 index=True)