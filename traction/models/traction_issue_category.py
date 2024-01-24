from odoo import models, fields


class IssueCategory(models.Model):
    _name = "traction.issue.category"
    _description = "Issue Category"

    name = fields.Char()
    sequence = fields.Integer(default=1)
    issue_ids = fields.One2many(
        comodel_name="traction.issue",
        inverse_name="category_id",
    )