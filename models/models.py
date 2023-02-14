# -*- coding: utf-8 -*-

import random
from odoo import models, fields, api
from datetime import timedelta, datetime


class user(models.Model):
    _inherit = 'res.partner'
    _name = 'res.partner'
    _description = 'salespop users'

    #name = fields.Char(compute = "default_name_user", readonly = False)
    #user_name = fields.Char()
    mail = fields.Char(readonly = False, domain = [('mail','ilike','a')])
    password = fields.Char()
    num_tel = fields.Integer(readonly = False, domain = [('num_tel','<',1000000000),('num_tel','>',99999999)])
    on_sale = fields.One2many('salespop.product', 'seller')
    valoracion = fields.One2many('salespop.valoracion', 'valoracion_usuario')

    is_user_pop = fields.Boolean(default = False)

    @api.onchange('name') #preguntar com fer se s'execute sols una vegada
    def _default_name_userChange(self):                                             
            for f in self:
                if (f.name == ""):
                    f.name = "user"+(str(random.randint(0, 99999)))


    # @api.onchange('mail')
    # def _filter_dovahkiin_player(self):                                             
    #     return { 'like': {[('mail','like','%@%')]}}

class product(models.Model):
    _name = 'salespop.product'
    _description = 'salespop products'

    name = fields.Char()
    price = fields.Integer()
    categoria = fields.Many2one('salespop.category')
    description = fields.Char()
    ubication = fields.Char()
    publication_date = fields.Datetime(readonly=True, default=fields.Datetime.now)
    seller = fields.Many2one('res.partner', ondelete = "cascade")
    foto = fields.One2many('salespop.foto', 'product')
    label = fields.Many2one('salespop.label')

    def _many2manyFoto(self):
        for b in self:
            b.foto = self.env['salespop.foto'].search([('product.id','=',b.id)]).id

class category(models.Model):
    _name = 'salespop.category'
    _description = 'salespop categories'

    name = fields.Selection([('MOTOR', "Motor"), ('INMOBILIARIA', "Inmobiliaria"), ('JUEGOS', "Juegos"), ('INFORMATICA', "Informatica"), ('TELEFONIA', "Telefonia"), ('MODA', "Moda"), ('DEPORTES', "Deportes")], default = 'MOTOR')
    articulo_categoria = fields.One2many('salespop.product', 'categoria')

class valoracion(models.Model):
    _name = 'salespop.valoracion'
    _description = 'salespop valoracion'

    name = fields.Char()
    puntuacion = fields.Selection([('1', "MEDIOCRE"), ('2', "MALO"), ('3', "REGULAR"), ('4', "BUENO"), ('5', "MUY BUENO")], default = '1')
    valoracion_usuario = fields.Many2one('salespop.user', 'valoracion')

class foto(models.Model):
    _name = 'salespop.foto'
    _description = 'salespop foto'

    name = fields.Char()
    photo = fields.Image(size_width=200, max_height = 200, required = True)
    url_imagen = fields.Char()
    product = fields.Many2one('salespop.product')


class empleado(models.Model):
    _name = 'salespop.empleado'
    _description = 'salespop empleado'

    name = fields.Char()
    email = fields.Integer()
    password = fields.Char()



class label(models.Model):
    _name = 'salespop.label'
    _description = 'salespop label'

    name = fields.Char()
    product = fields.One2many('salespop.product', 'label')





#private String name;
#private int price;
#private String description;
#private String ubication;
#private Categoria categoria;
#private Date fechaPubli;
#private Usuario vendedor;
#
#     @api.depends('value')
#     def _value_pc(self):
#         for record in self:
#             record.value2 = float(record.value) / 100
