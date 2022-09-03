from odoo import api, models, fields, tools, _
from odoo.tools import is_html_empty

class MailActivityType(models.Model):
    _inherit = "mail.activity.type"

    category = fields.Selection(selection_add=[('issue', 'Issue'), ('headline', 'Headline')])

class MailActivity(models.Model):
    _inherit = "mail.activity"

    level10_ids = fields.Many2many(comodel_name='traction.level10',
                                   relation='traction_level_10_activity_rel',
                                   string='Level 10',
                                   copy=False)