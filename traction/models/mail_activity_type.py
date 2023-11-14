from odoo import api, models, fields, tools, _
from odoo.tools import is_html_empty
from odoo.exceptions import ValidationError


class MailActivityType(models.Model):
    _inherit = "mail.activity.type"

    category = fields.Selection(selection_add=[('issue', 'Issue'), ('headline', 'Headline')])

