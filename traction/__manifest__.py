{
    'name': 'EOS',
    'version': '15.0.1.0.0',
    'summary': '',
    'author': '',
    'company': '',
    'maintainer': '',
    'license': 'LGPL-3',
    'depends': [
        'project'
    ],
    'data': [
        'security/ir.model.access.csv',
        'views/traction.xml',
        # 'views/traction_vision.xml',
        # 'views/traction_measurable.xml'
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
