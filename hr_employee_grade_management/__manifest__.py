{
    'name': 'Grade Management',
    'version': '19.0.1.0.0',
    'summary': 'Define employee grade levels, attach flexible allowances, and assign employees to grades.',
    'description': """
Grade Management
================
Manage employee compensation grades independently of payroll:

* Define grade levels with a base wage
* Attach any number of custom allowance types to each grade, each with its own amount
* Automatically track grade history per employee/contract, including grade-change dates
* See an employee's current grade on their profile
* Reusable allowance types shared across all grades

This module manages the grade and allowance *structure* only -- it does not
compute payslips. Pair it with Odoo Payroll or your own payroll module,
which can reference grade_id, current_grade_id, and the allowance lines.

Note: built for Odoo 19, where hr.contract was renamed to hr.version and the
hr_contract module was merged into core hr.
""",
    'category': 'Human Resources',
    'author': 'Lumint House',
    'website': '',
    'license': 'OPL-1',
    'depends': ['hr'],
    'data': [
        'security/ir.model.access.csv',
        'views/grade_views.xml',
        'views/grade_allowance_type_views.xml',
        'views/grade_history_views.xml',
        'views/employee_views.xml',
        'views/grade_menu.xml',
    ],
    'installable': True,
    'application': True,
}
