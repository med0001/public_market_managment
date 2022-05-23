from odoo import api, fields, models




class listdesmarche(models.Model):
    _name="list.des.marche"
    _description= u"Liste des marchés"

    name = fields.Char(string='N° de marché')
    objet = fields.Char(string='Objet')
    appelation = fields.Char(string='Appellation')
    abv = fields.Char(string='Abréviation')
    maitreouvrage = fields.Char(string="Maitre d'ouvrage")
    delegation = fields.Char(string="Délégué")
    respprojet = fields.Char(string="Responsable projet")
    bordereau = fields.One2many("list.bordereau.des.prix", "chantier_id", string="Bordereau des prix")




class listbordereaudesprix(models.Model):
    _name ="list.bordereau.des.prix"
    _description = u"Bordereau des prix"
    _order = "sequence"

    name = fields.Char(string="Code prix")
    designation = fields.Char(string="Désignation")
    unite = fields.Char(string="Unité(s)")
    quantite = fields.Float(string="Quantité")
    prixun = fields.Float(string="PU HT")
    montant = fields.Float(string="Montant HT", store=False)
    chantier_id = fields.Many2one("list.des.marche", string="Chantier")
    typedeprix = fields.Selection([('section', 'Section'), ('prix', 'Prix')], 'Type de prix')
    sequence = fields.Integer()

