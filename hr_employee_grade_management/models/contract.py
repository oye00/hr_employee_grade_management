from odoo import models, fields, api


class HrContract(models.Model):
    _inherit = 'hr.contract'

    grade_id = fields.Many2one(
        'grade.level',
        string="Grade Level",
        tracking=True
    )

    wage = fields.Float(
        related='grade_id.wage',
        store=True,
        readonly=True
    )

    # =========================
    # CREATE CONTRACT
    # =========================
    @api.model_create_multi
    def create(self, vals_list):
        contracts = super().create(vals_list)

        for contract in contracts:
            if contract.employee_id and contract.grade_id and contract.date_start:
                self.env['grade.history'].create({
                    'employee_id': contract.employee_id.id,
                    'contract_id': contract.id,
                    'grade_id': contract.grade_id.id,
                    'start_date': contract.date_start,
                    'end_date': contract.date_end or False,
                })

        return contracts

    # =========================
    # UPDATE CONTRACT (GRADE CHANGE LOGIC)
    # =========================
    def write(self, vals):

        old_grades = {c.id: c.grade_id for c in self}

        res = super().write(vals)

        if 'grade_id' in vals:

            history_model = self.env['grade.history']

            for contract in self:

                old_grade = old_grades.get(contract.id)
                new_grade = contract.grade_id

                old_id = old_grade.id if old_grade else False
                new_id = new_grade.id if new_grade else False

                # Covers: first-time assignment (old_id False), an actual
                # grade change, and clearing the grade (new_id False).
                # The previous version of this check required old_grade to
                # already be set, which silently skipped first assignment
                # -- the most common real-world case.
                if old_id == new_id:
                    continue

                effective_date = contract.date_start or fields.Date.today()

                previous_history = history_model.search([
                    ('contract_id', '=', contract.id),
                    ('end_date', '=', False)
                ], order="start_date desc", limit=1)

                if previous_history:
                    previous_history.write({
                        'end_date': effective_date
                    })

                if new_grade:
                    history_model.create({
                        'employee_id': contract.employee_id.id,
                        'contract_id': contract.id,
                        'grade_id': new_grade.id,
                        'start_date': effective_date,
                        'end_date': False,
                    })

                old_name = old_grade.name if old_grade else "No Grade"
                new_name = new_grade.name if new_grade else "No Grade"
                contract.message_post(
                    body=f"Grade changed from {old_name} to {new_name}"
                )

        return res
