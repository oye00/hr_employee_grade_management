from odoo import models, fields, api


class HrEmployee(models.Model):
    _inherit = 'hr.employee'

    current_grade_id = fields.Many2one(
        'grade.level',
        string="Current Grade",
        compute="_compute_current_grade",
        store=True,
        tracking=True,
    )

    @api.depends('contract_ids.grade_id', 'contract_ids.date_start')
    def _compute_current_grade(self):
        for emp in self:
            contracts = emp.contract_ids.filtered(lambda c: c.grade_id)
            if contracts:
                # Prefer the contract with the latest date_start; a
                # contract without one just falls to the end rather than
                # being excluded outright.
                latest = contracts.sorted(
                    key=lambda c: (c.date_start or fields.Date.min, c.id),
                    reverse=True
                )[0]
                emp.current_grade_id = latest.grade_id
            else:
                emp.current_grade_id = False
