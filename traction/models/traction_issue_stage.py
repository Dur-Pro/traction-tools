from odoo import models, fields, api


class IssueStage(models.Model):
    _name = "traction.issue.stage"
    _description = "Issue Stage"
    _order = 'sequence, id'

    name = fields.Char()
    sequence = fields.Integer(default=1)
    issue_ids = fields.One2many(
        comodel_name="traction.issue",
        inverse_name="stage_id",
    )
    fold = fields.Boolean('Folded in Kanban', help="This stage is folded in the kanban view.")
    is_closing_stage = fields.Boolean("Closing Stage", help="This stage represents a closed issue.")
    issues_list_id = fields.Many2one(
        comodel_name="traction.issues.list",
        string="Issues List",
        default=lambda self: self.env.context.get("default_issues_list_id")
    )
