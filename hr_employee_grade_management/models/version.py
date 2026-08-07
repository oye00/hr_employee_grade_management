from odoo import models, fields, api


class HrVersion(models.Model):
    # In Odoo 19, hr.contract was renamed to hr.version, and the hr_contract
    # module was merged into core hr. date_start/date_end became non-stored
    # compatibility aliases; the real stored fields are contract_date_start
    # and contract_date_end (found via developer mode on the employee's
    # Payroll tab).
    _inherit = 'hr.version'

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
    # CREATE VERSION/CONTRACT
    # =========================
    @api.model_create_multi
    def create(self, vals_list):
        versions = super().create(vals_list)

        for version in versions:
            if version.employee_id and version.grade_id:
                # grade.history requires a start_date, so only log history
                # if one is available -- but always refresh Current Grade
                # regardless, since a missing start date shouldn't hide an
                # otherwise-valid grade assignment.
                if version.contract_date_start:
                    self.env['grade.history'].create({
                        'employee_id': version.employee_id.id,
                        'contract_id': version.id,
                        'grade_id': version.grade_id.id,
                        'start_date': version.contract_date_start,
                        'end_date': version.contract_date_end or False,
                    })
                version.employee_id._compute_current_grade()

        return versions

    # =========================
    # UPDATE VERSION/CONTRACT (GRADE CHANGE LOGIC)
    # =========================
    def write(self, vals):

        old_grades = {v.id: v.grade_id for v in self}

        res = super().write(vals)

        if 'grade_id' in vals:

            history_model = self.env['grade.history']

            for version in self:

                old_grade = old_grades.get(version.id)
                new_grade = version.grade_id

                old_id = old_grade.id if old_grade else False
                new_id = new_grade.id if new_grade else False

                # Covers: first-time assignment (old_id False), an actual
                # grade change, and clearing the grade (new_id False).
                # The previous version of this check required old_grade to
                # already be set, which silently skipped first assignment.
                if old_id == new_id:
                    continue

                effective_date = version.contract_date_start or fields.Date.today()

                previous_history = history_model.search([
                    ('contract_id', '=', version.id),
                    ('end_date', '=', False)
                ], order="start_date desc", limit=1)

                if previous_history:
                    previous_history.write({
                        'end_date': effective_date
                    })

                if new_grade:
                    history_model.create({
                        'employee_id': version.employee_id.id,
                        'contract_id': version.id,
                        'grade_id': new_grade.id,
                        'start_date': effective_date,
                        'end_date': False,
                    })

                old_name = old_grade.name if old_grade else "No Grade"
                new_name = new_grade.name if new_grade else "No Grade"
                version.message_post(
                    body=f"Grade changed from {old_name} to {new_name}"
                )

                version.employee_id._compute_current_grade()

        return res
