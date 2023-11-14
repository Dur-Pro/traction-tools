from odoo import api, models, fields, _
from datetime import datetime


class TractionRock(models.Model):
    _name = 'traction.rock'
    _description = 'Rock'
    _inherit = ['mail.thread', 'mail.activity.mixin']

    name = fields.Char(string='Name')
    # issue_ids = fields.One2many(comodel_name='traction.issue',
    #                             inverse_name='lv10_id',
    #                             string='Issues')
    vision_id = fields.Many2one(
        comodel_name='traction.vision',
        string='Vision'
    )

    user_id = fields.Many2one(
        comodel_name='res.users',
        string='Responsible',
        index=True)