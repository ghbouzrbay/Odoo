from odoo import models, fields, api
from odoo.exceptions import AccessError


# @mail_thread(copy=False)
class CRM(models.Model):
    _inherit = 'crm.lead'

    project_id = fields.Many2one('project.project', string="Project")
    opportunity_ids = fields.Many2many('sale.order.template', 'crm_id', string="Opportunities")
    message_id = fields.Many2one('mail.mail')

    @api.model
    @api.returns('crm.lead', lambda value: value.id)
    def create(self, values):
        project_vals = {
            'name': values.get('name'),

        }
        project = self.env['project.project'].create(project_vals)
        template_vals = {
            'name': values.get('name', 'New Template'),
            'crm_id': self.env.context.get('active_id'),
        }
        template = self.env['sale.order.template'].create(template_vals)

        message_body = 'Merci de valider la tache %s.' % (values.get('name') or 'Nouvelle opportunité')
        message_subject = 'Nouvelle opportunité @Marc Demo'
        message = self.env['mail.mail'].create({
            'subject': message_subject,
            'body': message_body,
            'model': template._name,
            'res_id': template.id,
        })

        values['project_id'] = project.id
        values['opportunity_ids'] = template

        opportunity = super(CRM, self).create(values)

        opportunity.message_subscribe(partner_ids=opportunity.message_follower_ids.mapped('partner_id').ids)

        opportunity.message_post(body=opportunity.name)
        message.sudo().send()

        return opportunity

    @api.onchange('opportunity_ids')
    def _onchange_opportunity_ids(self):
        if self.opportunity_ids:
            self.order_template_ids = [(6, 0, [])]
            self.order_template_ids = [(4, opportunity.id) for opportunity in self.opportunity_ids]


    def action_open_project_settings(self):
        return {
            'type': 'ir.actions.act_window',
            'res_model': 'project.project',
            'view_mode': 'tree,form',
            'target': 'current',
            'domain': [('id', '=', self.project_id.id)],
        }


    def action_open_order_template_settings(self):
        return {
            'type': 'ir.actions.act_window',
            'res_model': 'sale.order.template',
            'view_mode': 'tree,form',
            'target': 'current',
            'domain': [('id', 'in', self.opportunity_ids.ids)],
        }

    project_count = fields.Integer('# Project', compute='_compute_project_count')

    @api.depends('project_id')
    def _compute_project_count(self):
        if self.ids:
            project_data = self.env['project.project'].sudo()._read_group([
                ('crm_project_id', 'in', self.ids)
            ], ['crm_project_id'], ['crm_project_id'])
            mapped_data = {m['crm_project_id'][0]: m['project_id_count'] for m in project_data}
        else:
            mapped_data = dict()
        for lead in self:
            lead.project_count = mapped_data.get(lead.id, 0)

    template_count = fields.Integer('# Template', compute='_compute_template_count')
    # @api.depends('opportunity_ids')
    # def _compute_template_count(self):
    #     read_group_result = self.env['sale.order.template']._read_group([('crm_id', 'in', self.ids)], ['crm_id'],
    #                                                            ['crm_id'])
    #     result = dict((data['crm_id'][0], data['template_id_count']) for data in read_group_result)
    #     for sheet in self:
    #         sheet.template_count = result.get(sheet.id, 0)


class SaleOrderTemplate(models.Model):
    _inherit = 'sale.order.template'

    crm_id = fields.Many2one('crm.lead', string="CRM Lead")



class Project(models.Model):
    _inherit = "project.project"

    crm_project_id = fields.Many2many('crm.lead', 'project_id')