# from odoo import models, fields, api
#
#
#
# class CRM(models.Model):
#
#     _inherit = 'crm.lead'
#
#     range_id = fields.Many2one('date.range', 'crm_range_id')
#     range_line_id = fields.Many2one('date.range.line', 'crm_line_id')
#
#
# class DateRange(models.Model):
#     _name = 'date.range'
#     _description = 'Date Range'
#
#     crm_range_id = fields.One2many('crm.lead')
#     start_date = fields.Date('Start Date')
#     end_date = fields.Date('End Date')
#
#     @api.depends('start_date', 'end_date')
#     def _compute_dates(self):
#         for record in self:
#             record.dates = [fields.Date.to_date(fields.Date.from_string(date_str)) for date_str in (record.start_date + ' ' + str(i) for i in range((record.end_date - record.start_date).days + 1))]
#
#     dates = fields.One2many('date.range.line', 'date_range_id', string='Dates')
#
# class DateRangeLine(models.Model):
#
#     _name = 'date.range.line'
#
#     _description = 'Date Range Line'
#
#     crm_line_id = fields.One2many('crm.lead')
#     date = fields.Date('Date')
#
#     date_range_id = fields.Many2one('date.range', string='Date Range')
#
#     def create_date_range(self):
#
#         start_date = fields.Date.from_string(self.start_date)
#
#         end_date = fields.Date.from_string(self.end_date)
#
#         date_range = self.env['date.range'].create({
#
#             'start_date': start_date,
#
#             'end_date': end_date,
#
#         })
#
#         return {
#
#             'name': _('Date Range'),
#
#             'type': 'ir.actions.act_window',
#
#             'view_mode': 'tree',
#
#             'res_model': 'date.range',
#
#             'res_id': date_range.id,
#
#         }