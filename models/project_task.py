# -*- encoding: utf-8 -*-
##############################################################################
#
#    Bista Solutions Pvt. Ltd
#    Copyright (C) 2019 (http://www.bistasolutions.com)
#
#############################################################################
from odoo import api, fields, models, _
from odoo.exceptions import ValidationError


class ProjectTask(models.Model):
    _inherit = 'project.task'

    is_finished = fields.Boolean(string='Is Finished', default=False)
    quantity = fields.Float(string='Quantity', default=0.0)
    unit_value = fields.Float(string='Unit Value', default=0.0)
    total_value = fields.Float(string='Total Value')
    is_billable = fields.Selection([('billable', 'Billable'), ('non_billable', 'Non-Billable')], string='Is Billable', default='billable')
    resource_type = fields.Selection([('internal', 'Internal'), ('external', 'External')], string='Resource Type', default='internal')
    work_place = fields.Selection([('offshore', 'Offshore'), ('nearshore', 'Nearshore'), ('onsite','onsite')], string='Work From', default='offshore')
    coa_id = fields.Many2one('account.account', string='Account')
    def domain_set(self):
        project_obj= self.env['project.project'].browse(self.env.context.get('active_id'))
        my_list = project_obj.member.ids + [self.env.uid] + [project_obj.user_id.id]
        return [('id', 'in',my_list)]

    user_id = fields.Many2one('res.users',
        string='Assigned to',
        default=lambda self: self.env.uid,
        domain = domain_set ,
        index=True, track_visibility='always')

   

    
    @api.model
    def create(self, vals):
        quantity = 0.0
        unit_value = 0.0
        if 'quantity' in vals.keys():
            quantity = vals['quantity']
        if 'unit_value' in vals.keys():
            unit_value = vals['unit_value']
        vals['total_value'] = quantity * unit_value
        res = super(ProjectTask, self).create(vals)
        return res

    @api.multi
    def write(self, vals):
        quantity = self.quantity
        unit_value = self.unit_value
        if 'quantity' in vals.keys():
            quantity = vals['quantity']
        if 'unit_value' in vals.keys():
            unit_value = vals['unit_value']
        vals['total_value'] = quantity * unit_value
        res = super(ProjectTask, self).write(vals)
        return res

    @api.onchange('timesheet_ids')
    def _onchange_quantity(self):
        time_sheet_ids = self.timesheet_ids.mapped('quantity')
        if sum(time_sheet_ids) >= self.quantity:
            raise ValidationError(_('Total quantity should not be greater than quantity'))
        

class AccountAnalyticLine(models.Model):
    _inherit = 'account.analytic.line'

    is_finished = fields.Boolean(string='Is Finished', default=False)
    quantity = fields.Float(string='Quantity')
    unit_value = fields.Float(string='Unit Value')
    total_value = fields.Float(string='Total Value')
    is_billable = fields.Selection([('billable', 'Billable'), ('non_billable', 'Non-Billable')], string='Is Billable', default='billable')
    resource_type = fields.Selection([('internal', 'Internal'), ('external', 'External')], string='Resource Type', default='internal')
    work_place = fields.Selection([('offshore', 'Offshore'), ('nearshore', 'Nearshore'), ('onsite','onsite')], string='Work From', default='offshore')
    is_paid = fields.Boolean(string='Is Paid', default=False)
   
    @api.onchange('quantity', 'unit_value')
    def _onchange_quantity_unit_value(self):
        if self.quantity and self.unit_value:
            self.total_value = self.quantity * self.unit_value
        else:
            self.total_value = 0.0

    def create_journal_entry(self):
       return {
            'name': _('Journal Entry'),
            'view_type': 'form',
            'view_mode': 'form',
            'res_model': 'journal.entry',
            'type': 'ir.actions.act_window',
            'target': 'new',
       }


           

            
