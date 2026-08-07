from odoo import models, fields


class HrEmployee(models.Model):
    _inherit = 'hr.employee'

    current_grade_id = fields.Many2one(
        'grade.level',
        string="Current Grade",
        compute="_compute_current_grade",
        store=True,
    )

    def _compute_current_grade(self):
        version_model = self.env['hr.version']
        for emp in self:
            versions = version_model.search([
                ('employee_id', '=', emp.id),
                ('grade_id', '!=', False),
            ])
            if versions:
                # Prefer the version with the latest contract_date_start;
                # a version without one just falls to the end rather than
                # being excluded outright.
                latest = versions.sorted(
                    key=lambda v: (v.contract_date_start or fields.Date.min, v.id),
                    reverse=True
                )[0]
                emp.current_grade_id = latest.grade_id
            else:
                emp.current_grade_id = False
