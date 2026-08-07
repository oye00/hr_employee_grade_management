from odoo import models, fields


class GradeHistory(models.Model):
    _name = 'grade.history'
    _description = 'Employee Grade History'
    _order = 'start_date desc'

    employee_id = fields.Many2one('hr.employee', required=True)
    contract_id = fields.Many2one('hr.version', ondelete='cascade', string="Contract")
    grade_id = fields.Many2one('grade.level', required=True)

    start_date = fields.Date(required=True)
    end_date = fields.Date()
