# -*- encoding: utf-8 -*-
##############################################################################
#
#    Bista Solutions Pvt. Ltd
#    Copyright (C) 2019 (http://www.bistasolutions.com)
#
#############################################################################
from odoo import api, fields, models, _


class TimeSheet(models.TransientModel):
   _name = 'time.sheet'
   _description = 'Time Sheet'


   date_from = fields.Date(string='Date From', required=True)
   date_to = fields.Date(string='Date To', required=True)

   def action_update_attachment (self):
      
      pro_list= self.env['account.analytic.line'].search([('date', '>=', self.date_from), ('date', '<=', self.date_to),('is_billable','=','billable'), ('is_paid','!=',True)]).ids
      tree_view_id  = self.env.ref("eic_project.view_account_analytic_line_form_inherit_2").id
      return {
         'name': _('Timesheet'),
         'res_model': 'account.analytic.line',
         'domain': [('id', 'in', pro_list)],
         'type': 'ir.actions.act_window',
         'view_mode': 'list',
         'views': [(tree_view_id, 'tree')],
      }

   
    
