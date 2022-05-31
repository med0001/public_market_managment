from odoo import api, fields, models
import json




class listdesmarche(models.Model):
    _name="list.des.marche"
    _description= u"Liste des marchés"
    _rec_name = 'abv'

    name = fields.Char(string='N° de marché')
    objet = fields.Char(string='Objet')
    appelation = fields.Char(string='Appellation')
    abv = fields.Char(string='Abréviation')
    maitreouvrage = fields.Char(string="Maitre d'ouvrage")
    delegation = fields.Char(string="Délégué")
    respprojet = fields.Char(string="Responsable projet")
    bordereau = fields.One2many("list.bordereau.des.prix", "chantier_id", string="Bordereau des prix")
    nbratt = fields.One2many("recap.des.att", "recap_id", string="Recap des attachements")





class listbordereaudesprix(models.Model):
    _name ="list.bordereau.des.prix"
    _description = u"Bordereau des prix"
    _order = "sequence"

    name = fields.Char(string="Code prix")
    designation = fields.Char(string="Désignation")
    unite = fields.Char(string="Unité(s)")
    quantite = fields.Float(string="Quantité")
    prixun = fields.Float(string="PU HT")
    montant = fields.Float(string="Montant HT", store=False, compute='_calcul_montant_prix')
    chantier_id = fields.Many2one("list.des.marche", string="Chantier")
    typedeprix = fields.Selection([('section', 'Section'), ('prix', 'Prix')], 'Type de prix')
    lesquantite = fields.One2many("detail.des.att", "listprix", string="Detail quantité")
    sequence = fields.Integer()

    @api.depends('prixun', 'quantite')
    def _calcul_montant_prix(self):
        for prix in self:
            prix.montant = prix.quantite * prix.prixun

    @api.onchange('typedeprix')
    def _onchange_typedeprix(self):
        for type in self:
            if type.typedeprix == "section":
                type.unite = "-"
                type.quantite = 0
                type.prixun = 0


class recapdesatt(models.Model):
    _name ="recap.des.att"
    _description = u"Récapitulatif des attachements"

    name = fields.Integer(string="N° de l'attachement", readonly=True, required=True, store=True, group_operator=False)
    mois = fields.Date(string="Mois")
    typeatt = fields.Selection([('tr', 'Attachcemnt réel'), ('mo', 'Attachement MO')], "Type d'attachement")
    recap_id = fields.Many2one("list.des.marche", string="Chantier", required=True)
    detail_id = fields.One2many("detail.des.att", "nuatt", string="Detail quantité")
    montant = fields.Float(string="Montant HT", store=False, compute='_calcul_montant_prixsss')
    etatatt = fields.Selection([('cre', 'Créé'), ('clt', 'Clôturé'), ('vld', 'Validé')], "Etat d'attachement")
    montant = fields.Float(string="Montant d'attachement HT", compute='_compute_montant_att', store=False, group_operator=True)


    @api.onchange('recap_id')
    def _def_att_numb(self):
        attnumb = []
        for att in self.env["recap.des.att"].search([('recap_id.id', '=', self.recap_id.id)], order='id desc'):
            attnumb.append(att.name)
        if attnumb:
            self.name = attnumb[0] + 1
        else:
            self.name = 1


    def action_cloturer_att(self):
        if self.etatatt == "cre":
            self.etatatt = 'clt'
    def action_valider_att(self):
        if self.etatatt == "clt":
            self.etatatt = 'vld'

    def _compute_montant_att(self):
        montants = 0
        for att in self:
            for prix in att.env['detail.des.att'].search([('nuatt.id', '=', att.id)]):
                montants = prix.name * prix.listprix.prixun
            att.montant = montants





class detaildesatt(models.Model):


    _name ="detail.des.att"
    _description = u"Détail des attachements"


    name = fields.Float(string="Quantité mois")
    nuatt = fields.Many2one("recap.des.att", string="N° attachements")
    marcheid = fields.Many2one("list.des.marche", string="Marché")
    listprix = fields.Many2one("list.bordereau.des.prix", string="N° Prix", required=True)
    prix_id_domain = fields.Char(compute="_compute_prix_id_domain", readonly=True, store=False)
    designation_prix = fields.Char(string="Désignation" , readonly=True, store=False, compute="_depends_designation")
    unite_prix = fields.Char(string="Unité(s)", readonly=True, store=False, compute="_depends_designation")
    quantite_prix = fields.Float(string="Quantité", readonly=True, store=False, compute="_depends_designation")
    PU_prix = fields.Float(string="PU HT", readonly=True, store=False, compute="_depends_designation")
    montant_prix = fields.Float(string="Montant marché", readonly=True, store=False)
    quantiteant_prix = fields.Float(string="Qtité Ant", readonly=True, store=False)
    quantitecml_prix = fields.Float(string="Qtité Cml", readonly=True, store=False)
    montantant_prix = fields.Float(string="Montant Ant", readonly=True, store=False)
    montantm_prix = fields.Float(string="Montant mois", readonly=True, store=False)
    montantcml_prix = fields.Float(string="Montant Cml", readonly=True, store=False)

    sequence = fields.Integer()


    @api.depends('marcheid')
    def _compute_prix_id_domain(self):
        period_ids = []
        for chantier in self.env["list.bordereau.des.prix"].search([('chantier_id.id', '=', self.marcheid.id), ('typedeprix', '=', 'prix')]):
            period_ids.append(chantier.id)
        if period_ids:
            self.prix_id_domain =  json.dumps(
                [('id', 'in', period_ids)]
            )



    @api.depends('listprix')
    def _depends_designation(self):
        self.designation_prix = self.listprix.designation
        self.unite_prix = self.listprix.unite
        self.quantite_prix = self.listprix.quantite
        self.PU_prix = self.listprix.prixun
        self.montant_prix = self.listprix.quantite * self.listprix.prixun
        quantitess = 0
        for prix in self.env["detail.des.att"].search([('listprix.id', '=', self.listprix.id),('nuatt.name', '<', self.nuatt.name)]):
            quantitess = prix.name + quantitess
        self.quantiteant_prix = quantitess
        self.quantitecml_prix = quantitess + self.name
        self.montantant_prix = quantitess * self.PU_prix
        self.montantm_prix = self.name * self.PU_prix
        self.montantcml_prix = (quantitess + self.name) * self.PU_prix

    @api.onchange('name')
    def _onchange_qttmoi(self):
        self.quantitecml_prix = self.name + self.quantiteant_prix
        self.montantm_prix = self.name * self.PU_prix
        self.montantcml_prix = self.quantitecml_prix * self.PU_prix

    @api.onchange('quantitecml_prix')
    def _onchange_qttcml(self):
        self.name = self.quantitecml_prix - self.quantiteant_prix
        self.montantm_prix = self.name * self.PU_prix
        self.montantcml_prix = self.quantitecml_prix * self.PU_prix





