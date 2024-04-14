from odoo import api, models, fields
from datetime import datetime


SELECTION_CHOICES = [
        ('monthly', 'Monthly'),
        ('daily', 'Daily'),
        ('hourly', 'Hourly'),
    ]
class CRM(models.Model):

    _inherit = 'crm.lead'

    def open_my_wizard(self):
        return {
            'name': 'Gestion Profil',
            'type': 'ir.actions.act_window',
            'res_model': 'sinoma_crm.my_wizard',
            'view_mode': 'form',
            'view_type': 'form',
            'target': 'new',
        }

    # @api.depends('sinoma_crm_my_wizard_id')
    # def _compute_my_wizard_data(self):
    #     for record in self:
    #         my_wizard_data = record.sinoma_crm_my_wizard_id
    #         if my_wizard_data:
    #             record.selection_field = my_wizard_data.selection_field
    #             record.start_date = my_wizard_data.start_date
    #             record.end_date = my_wizard_data.end_date
    #             record.ratio = my_wizard_data.ratio
    #             record.consumption = my_wizard_data.consumption
    #             record.pprice = my_wizard_data.pprice


    selection_field = fields.Selection(SELECTION_CHOICES, required=True)
    start_date = fields.Date('Start Date')
    end_date = fields.Date('End Date')
    ratio = fields.Float('Ratio')
    consumption = fields.Float('Consumption')
    pprice = fields.Float('Price')
    crm_lead_id = fields.Many2one('crm.lead')
    sinoma_crm_my_wizard_id = fields.Many2many('sinoma_crm.my_wizard')


class MyWizard(models.TransientModel):
    _name = 'sinoma_crm.my_wizard'

    name = fields.Char('Type', required=True)
    start_date = fields.Date('Start Date')
    end_date = fields.Date('End Date')
    ratio = fields.Float('Ratio')
    consumption = fields.Float('Consumption')
    pprice = fields.Float('Price')
    crm_lead_id = fields.One2many('crm.lead', 'sinoma_crm_my_wizard_id')

    Contry = [
        ('morocco', 'Morocco'),
        ('colombia', 'Colombia')
    ]

    selection_contry = fields.Selection(Contry, required=True)
    selection_field = fields.Selection(SELECTION_CHOICES, required=False)

    @api.model
    def create(self, vals):
        res = super(MyWizard, self).create(vals)
        if res.crm_lead_id:
            res.crm_lead_id.write({
                'selection_field': res.selection_field,
                'start_date': res.start_date,
                'end_date': res.end_date,
                'ratio': res.ratio,
                'consumption': res.consumption,
                'pprice': res.pprice,
            })
        return res

    def action_validate_and_save(self):
        self.ensure_one()
        self.crm_lead_id = self.crm_lead_id  # Force recompute of crm_lead_id
        return {'type': 'ir.actions.act_window_close'}
