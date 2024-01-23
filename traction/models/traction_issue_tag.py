from odoo import models, fields, api, _
from random import randint

class IssueTag(models.Model):
    _name="traction.issue.tag"
    _description="Issue Tag"

    @api.model
    def _get_default_color(self):
        return randint(1, 11)

    name = fields.Char(translate=True)
    color = fields.Integer(
        string='Color',
        default=_get_default_color
    )
    issue_ids = fields.Many2many(
        comodel_name="traction.issue",
        relation="traction_issue_tag_rel",
        column1="tag_id",
        column2="issue_id",
        string="Issues",
    )
