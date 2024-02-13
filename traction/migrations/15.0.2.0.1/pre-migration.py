from openupgradelib import openupgrade

model_spec = [
    ('traction.issue.category', 'traction.issue.stage'),
]

fields_spec = [
    (
        'traction.issue',
        'traction_issue',
        'category_id',
        'stage_id',
    ),
]
@openupgrade.migrate()
def migrate(env, version):
    openupgrade.rename_fields(env, fields_spec)
    openupgrade.rename_models(env.cr, model_spec)
