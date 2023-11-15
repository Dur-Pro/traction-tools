from odoo import api, models, fields, _
from datetime import datetime


class TractionVision(models.Model):
    _name = 'traction.vision'
    _description = 'Vision'
    _inherit = ['mail.thread', 'mail.activity.mixin']

    name = fields.Char(
        string='Vision',
        copy=False,
        readonly=True,
        index=True,
        default=lambda self: _('New')
    )

    company_id = fields.Many2one(
        comodel_name='res.company',
        string='Company',
        required=True,
        default=lambda self: self.env.company
    )

    vision_range = fields.Selection(
        [
            ('3mth', 'Three months'),
            ('1yr', 'One year'),
            ('3yr', 'Three years'),
            ('10yr', 'Ten years')
        ],
        default='3mth',
        string='Vision range'
    )

    target_revenue = fields.Float(string='Revenue')
    target_profit = fields.Float(string='Profit')
    target_date = fields.Date(string='Target date')
    target_picture = fields.Html(string='Pictures/Goals')

    measurable_ids = fields.One2many(
        comodel_name='traction.measurable',
        inverse_name='vision_id',
        string='Measurable'
    )

    rock_ids = fields.One2many(
        comodel_name='traction.rock',
        inverse_name='vision_id',
        string='Rocks'
    )

    # issue_ids = fields.One2many(comodel_name='traction.issue',
    #                             inverse_name='traction_id',
    #                             string='Issues')

    @api.model
    def create(self, vals):
        if vals.get('name', _('New')) == _('New'):
            vision_range_key = vals.get('vision_range')
            range_code = self._fields['vision_range'].selection
            range_code_dict = dict(range_code)
            range_name = range_code_dict.get(vision_range_key)
            company_id = self.env.company
            vals['name'] = company_id.name + " in " + range_name

        result = super(TractionVision, self).create(vals)
        return result


