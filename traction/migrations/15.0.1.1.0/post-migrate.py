from odoo import api, SUPERUSER_ID


def migrate(cr, version):
    env = api.Environment(cr, SUPERUSER_ID, {})
    issue_type = env.ref('traction.mail_activity_data_issue')
    headline_type = env.ref('traction.mail_activity_data_headline')
    issue_headline_activities = env['mail.activity'].search(
        [('activity_type_id', 'in', [issue_type.id, headline_type.id])]
    )
    issue_headline_activities.write({'user_id': env.ref('base.user_root').id })

