{
    'name': 'Fleet Management',
    'version': '1.0',
    'category': 'Operations',
    'summary': 'Track company vehicles, maintenance, and scheduling.',
    'description': """
Custom Fleet Management
========================
Manage vehicles, track maintenance schedules, and automate service reminders.
""",
    'author': 'Odoo PS',
    'website': 'https://yourcompany.com',
    'category': 'Operations/Fleet',
    'depends': [
        'base',
    ],
    'data': [
        'security/security.xml',
        'security/ir.model.access.csv',
    ],
    'demo': [],
    'license': 'LGPL-3',
    'installable': True,
    'application': True,
    'auto_install': False,
}
