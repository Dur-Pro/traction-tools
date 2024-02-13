from openupgradelib import openupgrade

model_spec = [
    ('traction.issue.category', 'traction.issue.stage'),
]

table_spec = [
    ('traction_issue_category', 'traction_issue_stage')
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
    openupgrade.rename_tables(env.cr, table_spec)
    openupgrade.rename_models(env.cr, model_spec)
    openupgrade.rename_fields(env, fields_spec)
