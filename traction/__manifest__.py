{
    'name': 'EOS',
    'version': '17.0.1.0.0',
    'summary': '',
    'author': '',
    'company': '',
    'maintainer': '',
    'license': 'LGPL-3',
    'depends': [
        'calendar',
        'uom',
    ],
    'demo': [
        'data/traction_demo.xml'
    ],
    'data': [
        'security/ir.model.access.csv',
        'security/traction_record_rules.xml',
        'data/calendar_event_agenda_template.xml',
        # 'views/traction_value.xml',
        # 'views/traction_strategy.xml',
        # 'views/traction_vision.xml',
        'views/traction_team.xml',
        # 'views/traction_traction.xml',
        'views/traction.xml',
        # 'views/traction_measurable.xml',
        # 'views/traction_measurable_value.xml',
        'views/traction.xml',
        'views/mail_channel_views.xml',
        'views/traction_issues_list.xml',
        'views/traction_issues.xml',
        'views/traction_headlines.xml',
        'views/calendar_event_agenda_template_views.xml',
        'views/calendar_event_views.xml',
        # 'wizards/close_meeting_wizard.xml',
        'report/calendar_event_templates.xml',
        'report/calendar_event_report.xml',
    ],
    'assets': {
        'web.assets_backend': [
            'traction/static/src/components/common.js',
            'traction/static/src/components/systray_issues/systray_issues.js',
            'traction/static/src/components/systray_headlines/systray_headlines.js',
            'traction/static/src/js/issues_list_kanban.js',
        ],
        'web.assets_qweb': [
            'traction/static/src/components/systray_headlines/systray_headlines.xml',
            'traction/static/src/components/systray_issues/systray_issues.xml',
        ],
    },
    'installable': True,
    'application': True,
    'auto_install': False,
}
