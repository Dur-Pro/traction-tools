from odoo import api, models, fields, tools, _
from odoo.tools import is_html_empty

class MailActivityType(models.Model):
    _inherit = "mail.activity.type"

    category = fields.Selection(selection_add=[('issue', 'Issue'), ('headline', 'Headline')])

class MailActivity(models.Model):
    _inherit = "mail.activity"

    level10_id = fields.Many2one(
        comodel_name='traction.level10',
        string='Level 10',
        copy=False
    )

    meet_id = fields.Many2one(
        comodel_name='calendar.event',
        string='Meeting',
        copy=False
    )

    @api.constrains('activity_type_id')
    def _check_date_end(self):
        for record in self:
            if (record.activity_type_id in [11]) and (record.level10_id == False):
                raise ValidationError("Issues need to be assign to level 10")
        # all records passed the test, don't return anything