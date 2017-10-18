# -*- coding: utf-8 -*-
#
# Copyright 2017 KMEE
#   Wagner Pereira <wagner.pereira@kmee.com.br>
# License AGPL-3 or later (http://www.gnu.org/licenses/agpl)
#
from odoo import api, fields, models

class LotacaoClassificacaoTributaria(models.Model):
    _name = 'esocial.lotacao_classificacao_tributaria'
    _description = 'Compatibilidade entre Tipos de Lotação e Classificação Tributária'

    _order = 'name'
    _sql_constraints = [
        ('codigo',
         'unique(codigo)',
         'Este código já existe',
        )
    ]

    codigo = fields.Char(
        size = 2,
        string = 'Código do Tipo de Lotação',
        required = True,
    )
    c1 = fields.Char(
        string = '01',
        required = True,

    )
    c2 = fields.Char(
        string='02',
        required=True,
    )
    c3 = fields.Char(
        string='03',
        required=True,
    )
    c4 = fields.Char(
        string='04',
        required=True,
    )
    c6 = fields.Char(
        string='06',
        required=True,
    )
    c7 = fields.Char(
        string='07',
        required=True,
    )
    c8 = fields.Char(
        string='08',
        required=True,
    )
    c9 = fields.Char(
        string='09',
        required=True,
    )
    c10 = fields.Char(
        string='10',
        required=True,
    )
    c11 = fields.Char(
        string='11',
        required=True,
    )
    c13 = fields.Char(
        string='13',
        required=True,
    )
    c14 = fields.Char(
        string='14',
        required=True,
    )
    c21 = fields.Char(
        string='21',
        required=True,
    )
    c22 = fields.Char(
        string='22',
        required=True,
    )
    c60 = fields.Char(
        string='60',
        required=True,
    )
    c70 = fields.Char(
        string='70',
        required=True,
    )
    c80 = fields.Char(
        string='80',
        required=True,
    )
    c85 = fields.Char(
        string='85',
        required=True,
    )
    c99 = fields.Char(
        string='99',
        required=True,
    )
    name = fields.Char(
        compute = '_compute_name',
        store = True,
    )

    @api.onchange('codigo')
    def _valida_codigo(self):
        for elementos in self:
            if not elementos.codigo.isdigit():
                res = {'warning': {
                        'title': _('Código Incorreto!'),
                        'message': _('Campo Código somente aceita números!'
                                     ' - Corrija antes de salvar')
                }}
                return res


    @api.depends('codigo', 'c1', 'c2', 'c3', 'c4', 'c6', 'c7', 'c8', 'c9', 'c10', 'c11', 'c13', 'c21', 'c22', 'c60', 'c70', 'c80', 'c85', 'c99')
    def _compute_name(self):
        for c in self:
            c.name = c.codigo + '-' + c.c1+c.c2+c.c3+c.c4+c.c6+c.c7+c.c8+c.c9+c.c10+c.c11+c.c13+c.c14+c.c21+c.c22+c.c60+c.c70+c.c80+c.c85+c.c99