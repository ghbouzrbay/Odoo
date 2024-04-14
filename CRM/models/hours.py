from odoo import models, fields, api
from datetime import datetime, timedelta
from odoo.exceptions import UserError, ValidationError
from odoo import http



class CRM(models.Model):
    _inherit = 'crm.lead'

    hours = fields.One2many('crm.hours', 'crm_id')
    mois = fields.One2many('crm.hours', 'crm_id')
    @api.model
    def default_get(self, fields):
        defaults = super(CRM, self).default_get(fields)
        hours_days = [
            (0, 0, {'hours_of_day': '00:00', 'monday': True, 'tuesday': True, 'thursday': True, 'wednesday': True, 'friday': True, 'saturday': True, 'sunday': True}),
            (0, 0, {'hours_of_day': '01:00', 'monday': True, 'tuesday': True, 'thursday': True, 'wednesday': True, 'friday': True, 'saturday': True, 'sunday': True}),
            (0, 0, {'hours_of_day': '02:00', 'monday': True, 'tuesday': True, 'thursday': True, 'wednesday': True, 'friday': True, 'saturday': True, 'sunday': True}),
            (0, 0, {'hours_of_day': '03:00', 'monday': True, 'tuesday': True, 'thursday': True, 'wednesday': True, 'friday': True, 'saturday': True, 'sunday': True}),
            (0, 0, {'hours_of_day': '04:00', 'monday': True, 'tuesday': True, 'thursday': True, 'wednesday': True, 'friday': True, 'saturday': True, 'sunday': True}),
            (0, 0, {'hours_of_day': '05:00', 'monday': True, 'tuesday': True, 'thursday': True, 'wednesday': True, 'friday': True, 'saturday': True, 'sunday': True}),
            (0, 0, {'hours_of_day': '06:00', 'monday': True, 'tuesday': True, 'thursday': True, 'wednesday': True, 'friday': True, 'saturday': True, 'sunday': True}),
            (0, 0, {'hours_of_day': '07:00', 'monday': True, 'tuesday': True, 'thursday': True, 'wednesday': True, 'friday': True, 'saturday': True, 'sunday': True}),
            (0, 0, {'hours_of_day': '08:00', 'monday': True, 'tuesday': True, 'thursday': True, 'wednesday': True, 'friday': True, 'saturday': True, 'sunday': True}),
            (0, 0, {'hours_of_day': '09:00', 'monday': True, 'tuesday': True, 'thursday': True, 'wednesday': True, 'friday': True, 'saturday': True, 'sunday': True}),
            (0, 0, {'hours_of_day': '10:00', 'monday': True, 'tuesday': True, 'thursday': True, 'wednesday': True, 'friday': True, 'saturday': True, 'sunday': True}),
            (0, 0, {'hours_of_day': '11:00', 'monday': True, 'tuesday': True, 'thursday': True, 'wednesday': True, 'friday': True, 'saturday': True, 'sunday': True}),
            (0, 0, {'hours_of_day': '12:00', 'monday': True, 'tuesday': True, 'thursday': True, 'wednesday': True, 'friday': True, 'saturday': True, 'sunday': True}),
            (0, 0, {'hours_of_day': '13:00', 'monday': True, 'tuesday': True, 'thursday': True, 'wednesday': True, 'friday': True, 'saturday': True, 'sunday': True}),
            (0, 0, {'hours_of_day': '14:00', 'monday': True, 'tuesday': True, 'thursday': True, 'wednesday': True, 'friday': True, 'saturday': True, 'sunday': True}),
            (0, 0, {'hours_of_day': '15:00', 'monday': True, 'tuesday': True, 'thursday': True, 'wednesday': True, 'friday': True, 'saturday': True, 'sunday': True}),
            (0, 0, {'hours_of_day': '16:00', 'monday': True, 'tuesday': True, 'thursday': True, 'wednesday': True, 'friday': True, 'saturday': True, 'sunday': True}),
            (0, 0, {'hours_of_day': '17:00', 'monday': True, 'tuesday': True, 'thursday': True, 'wednesday': True, 'friday': True, 'saturday': True, 'sunday': True}),
            (0, 0, {'hours_of_day': '18:00', 'monday': True, 'tuesday': True, 'thursday': True, 'wednesday': True, 'friday': True, 'saturday': True, 'sunday': True}),
            (0, 0, {'hours_of_day': '19:00', 'monday': True, 'tuesday': True, 'thursday': True, 'wednesday': True, 'friday': True, 'saturday': True, 'sunday': True}),
            (0, 0, {'hours_of_day': '20:00', 'monday': True, 'tuesday': True, 'thursday': True, 'wednesday': True, 'friday': True, 'saturday': True, 'sunday': True}),
            (0, 0, {'hours_of_day': '21:00', 'monday': True, 'tuesday': True, 'thursday': True, 'wednesday': True, 'friday': True, 'saturday': True, 'sunday': True}),
            (0, 0, {'hours_of_day': '22:00', 'monday': True, 'tuesday': True, 'thursday': True, 'wednesday': True, 'friday': True, 'saturday': True, 'sunday': True}),
            (0, 0, {'hours_of_day': '23:00', 'monday': True, 'tuesday': True, 'thursday': True, 'wednesday': True,
                    'friday': True, 'saturday': True, 'sunday': True}),

        ]
        print("ddddddddddddddddddddddddddddddd", defaults, self, hours_days)
        defaults.update({'hours': hours_days})
        return defaults

    consumption_money = fields.Float(string="Consumption Money (HT)")
    consumption_energy = fields.Float(string="Consumption Energy (Kwh)")
    legacy_energy = fields.Float(string="Legacy Energy LCOE($ HT/KWh )", compute="_compute_legacy_energy")
    facture = fields.Selection([('Flat Price', 'Flat Price'), ('Time_based', 'Time_based'), ('Ladder Price', 'Ladder Price'), ('Other','Other')], string="Facture Method")
    project = fields.Selection([('Public REP', 'Public REP'), ('Private EPC', 'Private EPC'), ('Private PPA', 'Private PPA'), ('Other','Other')], string="Project Type")
    site = fields.Selection([('On-Grid', 'On-Grid'), ('Off-Grid', 'Off-Grid'), ('Hybrid', 'Hybrid'), ('PV-Storage', 'PV-Storage'), ('Greeen Thermal', 'Greeen Thermal'), ('Other', 'Other')], string="Site Type")
    installation = fields.Selection([('Gound Mounted', 'Gound Mounted'), ('Pitched Roof ', 'Pitched Roof'), ('Flat Roof', 'Flat Roof'), ('Waterproof Roof ', 'Waterproof Roof'), ('Other', 'Other')], string="Installation Method")
    structure = fields.Selection([('Yes', 'Yes'), ('No', 'No')], string="Structure Analysis Required?")

    @api.depends('consumption_energy', 'consumption_money')
    def _compute_legacy_energy(self):
        for order in self:
            if order.consumption_energy != 0:
                order.legacy_energy = order.consumption_money / order.consumption_energy
            else:
                order.legacy_energy = 0.0

    # message = fields.Text(compute="_compute_message")
    # def _compute_message(self):
    #     message_body = "Le traitement est terminé. @Ahmmed, Vous pouvez le vérifier"
    #     self.message_post(body=message_body)



    holidays = fields.Selection([('Oui', 'Oui'), ('Non', 'Non')], string='Holidays Off')
    temps_travail = fields.Selection(
        [('Temporary', 'Temporary'), ('Part-time', 'Part-time'), ('Full-time', 'Full-time')], string='Temperatures')
    aid_adha = fields.Integer(string='AÏD AL-ADHA')
    aid_fitr = fields.Integer(string='AÏD AL-FITR')
    an_muslman = fields.Boolean(string='PREMIER DE AN MUSULMAN')


    abonnement = fields.Selection([('MT', 'MT'), ('BT', 'BT')], string="TYPE D'ABONNEMENT (MT,BT)")
    puissance = fields.Float(string='PUISANCE INSTALLÉE')
    transformateur = fields.Integer(string='Nombre de transformateurs MT/BT')
    disjoncteur = fields.Many2many('crm.disjoncteur', string='TELECHARGER LES FICHIERS', required=True)
    infrastructure = fields.Char(string='INFRASTRUCTURE ÉLECTRIQUE EXISTANTE')
    reglementation = fields.Float(string='REGLEMENTATION LOCALES ET NORMES')
    eloignement = fields.Float(string="LOIGNEMENT ENTRE LE POINT D'INJECTION ET LA CENTRALE SOLAIRE")


    mois_jv = fields.Boolean(string='JANVIER')
    mois_fr = fields.Boolean(string='FEVRIER')
    mois_mr = fields.Boolean(string='MARS')
    mois_av = fields.Boolean(string='AVRIL')
    mois_my = fields.Boolean(string='MAY')
    mois_ju = fields.Boolean(string='JUIN')
    mois_jui = fields.Boolean(string='JUILLET')
    mois_au = fields.Boolean(string='AOUT')
    mois_se = fields.Boolean(string='SEPTEMBRE')
    mois_oc = fields.Boolean(string='OCTBRE')
    mois_nv = fields.Boolean(string='NOVEMBRE')
    mois_de = fields.Boolean(string='DECEMBRE')

    factures = fields.Boolean(default=False, string="FACTURES")

    @api.onchange('factures')
    def _on_factures_change(self):
        if self.factures:
            self.update({
                'mois_jv': True,
                'mois_fr': True,
                'mois_mr': True,
                'mois_av': True,
                'mois_my': True,
                'mois_ju': True,
                'mois_jui': True,
                'mois_au': True,
                'mois_se': True,
                'mois_oc': True,
                'mois_nv': True,
                'mois_de': True,
            })
        else:
            self.update({
                'mois_jv': False,
                'mois_fr': False,
                'mois_mr': False,
                'mois_av': False,
                'mois_my': False,
                'mois_ju': False,
                'mois_jui': False,
                'mois_au': False,
                'mois_se': False,
                'mois_oc': False,
                'mois_nv': False,
                'mois_de': False,
            })


    zone_urbaine = fields.Boolean(string='ZONE Urbaine')
    zone_industrie = fields.Boolean(string='ZONE Industrie')
    zone_rurale = fields.Boolean(string='ZONE Rurale')
    zone_cotiere =fields.Boolean(string='ZONE Cotière')

    disposition_1 = fields.Boolean(string='TOITS INCLINÉS')
    disposition_2 = fields.Boolean(string='TOITS PLATS')
    disposition_3 = fields.Boolean(string='COPLANAIRE')
    disposition_6 = fields.Boolean(string='INSTALLATIONS SUR LES FAÇADES')

    # structure_15 = fields.Boolean(string='INCLINAISON STRUCTURE 15°')
    # structure_30 = fields.Boolean(string='INCLINAISON STRUCTURE 30°')
    # structure_other = fields.Boolean(string='INCLINAISON STRUCTURE Autre')
    selection_angle = fields.Selection([('structure_15', '15°'), ('structure_30', '30°'), ('structure_autres', 'Autres')], string='INCLINAISON STRUCTURE')

    height_installation = fields.Float(string='HAUTEUR INSTALLATION (m)')
    pente_toiture = fields.Float(string='PENTE TOITURE (°degree)')
    condition_conception = fields.Boolean(string='CONDITIONS DE CONCEPTION SELON RÉGLEMENTATION')
    condition_other = fields.Boolean(string='CONDITIONS DE CONCEPTION AUTRES')
    speed = fields.Float(string='VITESSE DU VENT (KM/H)')
    snow_change = fields.Float(string='CHARGE DE NEIGE (KG/M²)')

    # @api.model
    # def import_files(self, directory, file_types):
    #     for root, dirs, files in os.walk(directory):
    #         for file in files:
    #             file_path = os.path.join(root, file)
    #             file_ext = os.path.splitext(file_path)[1].lower()
    #             if file_ext in file_types:
    #                 if file_ext == '.zip':
    #                     with zipfile.ZipFile(file_path, 'r') as zip_file:
    #                         for inner_file in zip_file.namelist():
    #                             inner_file_ext = os.path.splitext(inner_file)[1].lower()
    #                             if inner_file_ext in file_types:
    #                                 with zip_file.open(inner_file) as zfile:
    #                                     content = zfile.read()
    #                                     self.import_file(inner_file, content, inner_file_ext)
    #                 else:
    #                     with open(file_path, 'rb') as file:
    #                         content = file.read()
    #                         self.import_file(file.name, content, file_ext)

    # @api.model
    # def import_file(self, file_name, content, file_ext):
    #     if file_ext == '.xlsx':
    #         workbook = xlrd.open_workbook(file_contents=content)
    #         worksheet = workbook.sheet_by_index(0)
    #         for row_index in range(worksheet.nrows):
    #             row = worksheet.row_values(row_index)
    #             # Handle row data as per your requirement
    #     elif file_ext == '.docx':
    #         document = docx.Document(BytesIO(content))
    #         for paragraph in document.paragraphs:
    #     # Handle paragraph data as per your requirement
    #     elif file_ext == '.csv':
    #         decoded_content = content.decode('utf-8')
    #         reader = csv.reader(decoded_content.splitlines(), delimiter=',')
    #         for row in reader:
    #     # Handle CSV row data as per your requirement
    #     else:
    #         raise Exception("Type de fichier non pris en charge : %s" % file_ext)



class WorkHours(models.Model):
    _name = 'crm.hours'

    crm_id = fields.Many2one('crm.lead')

    hour_00h00 = fields.Text(string="00")
    hour_01h00 = fields.Text(string="01")
    hour_02h00 = fields.Text(string="02")
    hour_03h00 = fields.Text(string="03")
    hour_04h00 = fields.Text(string="04")
    hour_05h00 = fields.Text(string="05")
    hour_06h00 = fields.Text(string="06")
    hour_07h00 = fields.Text(string="07")
    hour_08h00 = fields.Text(string="08")
    hour_09h00 = fields.Text(string="09")
    hour_10h00 = fields.Text(string="10")
    hour_11h00 = fields.Text(string="11")
    hour_12h00 = fields.Text(string="12")
    hour_13h00 = fields.Text(string="13")
    hour_14h00 = fields.Text(string="14")
    hour_15h00 = fields.Text(string="15")
    hour_16h00 = fields.Text(string="16")
    hour_17h00 = fields.Text(string="17")
    hour_18h00 = fields.Text(string="18")
    hour_19h00 = fields.Text(string="19")
    hour_20h00 = fields.Text(string="20")
    hour_21h00 = fields.Text(string="21")
    hour_22h00 = fields.Text(string="22")
    hour_23h00 = fields.Text(string="23")



    monday = fields.Boolean(string="Monday")
    tuesday = fields.Boolean(string="Tuesday")
    wednesday = fields.Boolean(string="Wednesday")
    thursday = fields.Boolean(string=" Thursday")
    friday = fields.Boolean(string="Friday")
    saturday = fields.Boolean(string="Saturday")
    sunday = fields.Boolean(string="Sunday")



    hours_of_day_selection = [
        ('00:00', '00:00'), ('01:00', '01:00'), ('02:00', '02:00'), ('03:00', '03:00'),
        ('04:00', '04:00'), ('05:00', '05:00'), ('06:00', '06:00'), ('07:00', '07:00'),
        ('08:00', '08:00'), ('09:00', '09:00'), ('10:00', '10:00'), ('11:00', '11:00'),
        ('12:00', '12:00'), ('13:00', '13:00'), ('14:00', '14:00'), ('15:00', '15:00'),
        ('16:00', '16:00'), ('17:00', '17:00'), ('18:00', '18:00'), ('19:00', '19:00'),
        ('20:00', '20:00'), ('21:00', '21:00'), ('22:00', '22:00'), ('23:00', '23:00')
    ]





    hours_of_day = fields.Selection(selection=hours_of_day_selection, string='Hours of Day')




    toggle = fields.Boolean(default=False, string="SLEC ALL")

    @api.onchange('toggle')
    def _on_toggle_change(self):
        if self.toggle:
            self.update({
                'monday': True,
                'tuesday': True,
                'wednesday': True,
                'thursday': True,
                'friday': True,
                'saturday': True,
                'sunday': True,
            })
        else:
            self.update({
                'monday': False,
                'tuesday': False,
                'wednesday': False,
                'thursday': False,
                'friday': False,
                'saturday': False,
                'sunday': False,
            })



class Disjoncteur(models.Model):
    _name = 'crm.disjoncteur'

    name = fields.Char(string='Name')
    attachment_ids = fields.Many2many('ir.attachment', string='Attachments')
    disj_id = fields.Many2one('crm.lead')
    mimetype = fields.Char(string="MIME Type")
    crm_controller_id = fields.Many2one('crm.controller')


class Controller(http.Controller):
    _name = 'crm.controller'

    @http.route('/download/files', type='http', auth='public')
    def download_files(self, file_ids, **kwargs):
        attachments = request.env['ir.attachment'].browse([int(id) for id in file_ids.split(',')])

        import io
        import zipfile

        zip_buffer = io.BytesIO()
        with zipfile.ZipFile(zip_buffer, 'w') as zip_file:
            for attachment in attachments:
                zip_file.writestr(attachment.name, attachment.datas)

        zip_buffer.seek(0)
        return http.send_file(zip_buffer, filename='attachments.zip')

