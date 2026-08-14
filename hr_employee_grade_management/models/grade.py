from odoo import models, fields, api


class GradeLevel(models.Model):
    _name = 'grade.level'
    _description = 'Employee Grade Level'
    _order = 'sequence, name'

    name = fields.Char(required=True)
    code = fields.Char(help="Optional short code for this grade (e.g. GL-07).")
    sequence = fields.Integer(default=10)
    active = fields.Boolean(default=True)
    company_id = fields.Many2one(
        'res.company', string="Company", default=lambda self: self.env.company
    )

    # =========================
    # BASE PAY
    # =========================
    wage = fields.Float(string="Basic Wage", default=0.0)

    # =========================
    # DYNAMIC ALLOWANCES
    # =========================
    allowance_line_ids = fields.One2many(
        'grade.allowance.line', 'grade_id', string="Allowances", copy=True
    )

    total_allowance = fields.Float(
        string="Total Allowances",
        compute='_compute_totals',
        store=True,
    )

    total_package = fields.Float(
        string="Total Package",
        compute='_compute_totals',
        store=True,
        help="Basic wage plus all allowances on this grade.",
    )

    employee_count = fields.Integer(
        string="Employees",
        compute='_compute_employee_count',
    )

    @api.depends('wage', 'allowance_line_ids.amount')
    def _compute_totals(self):
        for grade in self:
            grade.total_allowance = sum(grade.allowance_line_ids.mapped('amount'))
            grade.total_package = grade.wage + grade.total_allowance

    def _compute_employee_count(self):
        for grade in self:
            grade.employee_count = self.env['hr.employee'].search_count(
                [('current_grade_id', '=', grade.id)]
            )

    def action_view_employees(self):
        self.ensure_one()
        return {
            'name': 'Employees',
            'type': 'ir.actions.act_window',
            'res_model': 'hr.employee',
            'view_mode': 'list,form',
            'domain': [('current_grade_id', '=', self.id)],
        }
