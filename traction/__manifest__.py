{
    'name': 'EOS',
    'version': '15.0.1.0.0',
    'summary': '',
    'author': '',
    'company': '',
    'maintainer': '',
    'license': 'LGPL-3',
    'depends': [
        'calendar',
    ],
    'demo': [
        'data/traction_demo.xml'
    ],
    'data': [
        'security/ir.model.access.csv',
        'data/mail_data_various.xml',
        'data/calendar_event_agenda_template.xml',
        'views/mail_activity.xml',
        'views/traction_value.xml',
        'views/traction_strategy.xml',
        'views/traction_vision.xml',
        'views/traction_team.xml',
        'views/traction_traction.xml',
        'views/traction.xml',
        'views/traction_measurable.xml',
        'views/traction_measurable_value.xml',
        'views/traction.xml',
        'views/mail_channel_views.xml',
        'views/traction_identify_discuss_solve.xml',
        'views/calendar_event_agenda_template_views.xml',
        'views/calendar_event.xml',
        'wizards/close_meeting_wizard.xml',
        'report/calendar_event_templates.xml',
        'report/calendar_event_report.xml',
    ],
    'assets': {
        'web.assets_backend': [
            'traction/static/src/js/traction_dashboard.js'
        ],
        'web.assets_qweb': [
            'traction/static/src/xml/traction_dashboard.xml'
        ],
    },
    'installable': True,
    'application': True,
    'auto_install': False,
}
