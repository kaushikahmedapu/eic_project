# -*- encoding: utf-8 -*-
##############################################################################
#
#    Bista Solutions Pvt. Ltd
#    Copyright (C) 2019 (http://www.bistasolutions.com)
#
#############################################################################
from odoo import api, fields, models, _


class JournalEntry(models.TransientModel):
   _name = 'journal.entry'
   _description = 'Journal Entry'


   journal = fields.Many2one('account.journal', string='Journal', required=True)
   account = fields.Many2one('account.account', string='Account', required=True)



   def action_pos_entry(self):
       pro_list= self.env['account.analytic.line'].search([('is_paid','=',True)]).ids
       pro_list_id_for_print = self.env['account.analytic.line'].search([('is_paid','=',True)]).mapped('total_value')
       print("***********************",sum(pro_list_id_for_print))
       tree_view_id  = self.env.ref("eic_project.view_account_analytic_line_form_inherit_2").id
       return {
         'name': _('Timesheet'),
         'res_model': 'account.analytic.line',
         'domain': [('id', 'in', pro_list)],
         'type': 'ir.actions.act_window',
         'view_mode': 'list',
         'views': [(tree_view_id, 'tree')],
      }

   def action_cancel_entry(self):
       pass

   @api.onchange('journal')
   def _onchange_journal(self):
        if self.journal :
            self.account = self.journal.default_debit_account_id
