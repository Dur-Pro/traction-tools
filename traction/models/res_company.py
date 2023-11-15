from odoo import api, models, fields, _


class ResCompany(models.Model):
    _inherit = 'res.company'

    purpose = fields.Html(string='Purpose/Cause/Passion')
    niche = fields.Html(string='Our target customer')

    value_ids = fields.One2many(
        comodel_name='traction.value',
        inverse_name='company_id',
        string='Core Values'
    )

    strategy_ids = fields.One2many(
        comodel_name='traction.strategy',
        inverse_name='company_id',
        string='Strategies'
    )

    vision_ids = fields.One2many(
        comodel_name='traction.vision',
        inverse_name='company_id',
        string='Visions'
    )
