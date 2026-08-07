from odoo import models, fields


class GradeAllowanceLine(models.Model):
    _name = 'grade.allowance.line'
    _description = 'Grade Allowance Line'
    _order = 'sequence, id'

    grade_id = fields.Many2one(
        'grade.level', string="Grade", required=True, ondelete='cascade'
    )
    allowance_type_id = fields.Many2one(
        'grade.allowance.type', string="Allowance Type", required=True
    )
    sequence = fields.Integer(default=10)
    amount = fields.Float(string="Amount", required=True, default=0.0)

    _sql_constraints = [
        ('grade_allowance_type_uniq', 'unique(grade_id, allowance_type_id)',
         'This allowance type is already added to this grade.'),
    ]
