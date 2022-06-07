# -*- coding: utf-8 -*-
{
    'name': 'EIC PROJECT',
    'version': '1.0',
    'summary': 'PROJECT',
    'sequence': 10,
    'description': """EIC PROJECT""",
    'category': '',
    'website': '',
    'images': [],
    'depends': ['base','project','hr_timesheet'],
    'data': [
        'views/project_task.xml',
        'views/time_sheet.xml',
        'views/journal_entry_server_action.xml',
        'views/journal_entry.xml',
        'views/project_project.xml',
    ],
    'demo': [

    ],
    'qweb': [

    ],
    'installable': True,
    'application': True,
    'auto_install': False,
    'license': 'LGPL-3',
}
