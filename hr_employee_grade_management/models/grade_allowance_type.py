from odoo import models, fields


class GradeAllowanceType(models.Model):
    _name = 'grade.allowance.type'
    _description = 'Grade Allowance Type'
    _order = 'sequence, name'

    name = fields.Char(required=True)
    code = fields.Char(help="Optional short code, useful if a payroll module needs to reference this allowance.")
    sequence = fields.Integer(default=10)
    active = fields.Boolean(default=True)
    note = fields.Text(help="Internal notes about what this allowance covers or how it should be used.")

    _sql_constraints = [
        ('name_uniq', 'unique(name)', 'An allowance type with this name already exists.'),
    ]
