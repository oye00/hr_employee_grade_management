========================
Employee Grade Management
========================

.. Note: badges below assume you'll host this on GitHub. Update the
   repository path once your repo is live, or remove badges you don't need.

.. image:: https://img.shields.io/badge/licence-OPL--1-blue.png
    :target: https://www.odoo.com/documentation/user/legal/licenses.html
    :alt: License: OPL-1

This module gives you a clean, dynamic way to manage employee compensation
grades in Odoo — independent of payroll. Define grade levels, attach any
number of custom allowance types to each grade, assign employees to grades
through their contract, and keep a full audit trail of every grade change.

**Table of contents**

.. contents::
   :local:

Overview
========

Most organizations pay according to a grade or band system rather than
negotiating each salary individually — Grade 5, Grade 7, Level III, and so
on. Each grade typically carries a base wage plus a standard bundle of
allowances (housing, transport, HMO, and similar). Odoo's core HR does not
model this out of the box: contracts only expose a flat wage field, with no
concept of which grade tier an employee sits on or what that tier includes.

Employee Grade Management adds that layer, without assuming anything about
*how* your allowances are named, how many there are, or how payroll is
computed downstream. Everything is configurable from the UI — no code
changes required to add a new allowance type or grade.

Key Features
============

- **Grade Levels** — define any number of grades, each with its own base
  wage.
- **Dynamic Allowance Types** — define reusable allowance types (Housing,
  Transport, HMO, or anything specific to your organization) once, and
  reuse them across every grade.
- **Per-Grade Allowance Amounts** — attach any combination of allowance
  types to a grade, each with its own amount. Totals (allowances and full
  package) compute automatically.
- **Employee Assignment** — assign a grade to an employee through their
  contract; the employee's current grade, wage, and allowance breakdown are
  visible directly on their profile.
- **Automatic Grade History** — every grade change is logged automatically
  with a start and end date, giving you a complete audit trail for
  promotions, compliance, or appraisal cycles.
- **Smart Buttons** — jump straight from a grade to the list of employees
  currently on it.

What This Module Does Not Do
=============================

This module manages grade and allowance *structure* only. It does not
compute or generate payslips. If you need the allowances defined here to
automatically flow into payroll computation, see the companion
**Grade Management – Payroll Bridge** module, which connects this data to
Odoo Payroll's salary rules.

Configuration
=============

1. Go to **Employees > Grade Management > Allowance Types** and define the
   allowance types your organization uses (e.g. Housing, Transport).
2. Go to **Employees > Grade Management > Grade Levels** and create your
   grades. Set a base wage, then add allowance lines in the *Allowances*
   tab, picking an allowance type and an amount for each.
3. Open an employee record and set their **Grade Level** in the Grade
   Information section. Their current grade, wage, and totals will update
   automatically.

Usage
=====

- Changing an employee's grade automatically closes the previous grade
  history entry and opens a new one, dated from the contract's start date.
- The **Employees** smart button on a grade shows how many employees
  currently hold that grade.
- Grade history is visible under **Employees > Grade Management > Grade
  History**, filterable by employee or grade.

Bug Tracker
===========

Bugs are tracked on the module's issue tracker. In case of trouble, please
check there to see if your issue has already been reported. If you spot an
issue, please help fixing it by providing a detailed and welcomed feedback,
including steps to reproduce.

Credits
=======

Authors
-------

* Oyeyemi

Maintainers
-----------

This module is maintained by the author listed above.

For support or implementation help (including connecting this module to
your payroll setup), please get in touch directly.
