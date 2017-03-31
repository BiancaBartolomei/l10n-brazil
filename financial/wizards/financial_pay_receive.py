# -*- coding: utf-8 -*-
# Copyright 2017 KMEE
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import api, fields, models
import datetime


def data_proxima_util(data_inicial, dias_uteis):
    pass


class FinancialPayreceive(models.TransientModel):

    _name = 'financial.pay_receive'
    _inherit = ['account.abstract.payment']

    payment_type = fields.Selection(
        required=False,
    )
    payment_method_id = fields.Many2one(
        required=False,
    )
    ref = fields.Char()
    date_payment = fields.Date(
        required=True,
        default=fields.Date.context_today
    )
    date_credit_debit = fields.Date(
        compute='_compute_date_credit_debit'
    )
    amount_discount = fields.Monetary(
        string=u'Discount',
    )
    amount_interest = fields.Monetary(
        string=u'Interest',
        readonly=True,
    )
    journal_id = fields.Many2one(
        required=False,
    )
    bank_id = fields.Many2one(
        'res.partner.bank',
        string=u'Bank Account',
        required=True,
    )
    payment_mode_id = fields.Many2one(
        comodel_name='account.payment.mode',
        string=u'Payment mode',
    )
#    payment_term_id = fields.Many2one(
#        comodel_name='account.payment.term',
#        string=u'Payment term',
#    )

#    @api.depends('payment_mode_id', 'amount', 'date_business_maturity')
#    def compute_interest(self):
#        for record in self:
#            if self.env['resource.calendar']. \
#                    data_eh_dia_util_bancario(datetime.today()) and record. \
#                    state == 'open' and \
#                    (datetime.today() > datetime.strptime
#                        (record.date_business_maturity, '%Y-%m-%d')):
#                day = (
#                    datetime.today() - datetime.strptime(
#                        record.date_maturity,
#                        '%Y-%m-%d'))
#                interest = record.amount * (record.payment_mode_id.
#                                            interest_percent * day.days) / 100
#
#                delay_fee = (record.payment_mode_id.
#                             delay_fee_percent / 100) * record.amount
#                record.amount_interest = interest + delay_fee

    @api.onchange('payment_mode_id', 'date_payment')
    def _compute_date_credit_debit(self):
        compensation_days = self.payment_mode_id.compensation_days
        date_base = datetime.datetime.strptime(self.date_payment, '%Y-%m-%d')
        while compensation_days > 0:
            if self.env['resource.calendar'].data_eh_dia_util(date_base):
                compensation_days -= 1
            date_base = date_base + datetime.timedelta(days=1)

#        computations = \
#            self.payment_term_id.compute(self.amount, self.date_payment)
#        business_date_payment = computations[0][0][0]
#        date_payment = \
#            datetime.datetime.strptime(business_date_payment, "%Y-%m-%d")
#
#        self.date_credit_debit = date_payment + datetime.timedelta(
#            days=self.payment_mode_id.compensation_days)
        self.date_credit_debit = date_base

    @api.model
    def default_get(self, vals):
        res = super(FinancialPayreceive, self).default_get(vals)
        active_id = self.env.context.get('active_id')
        if (self.env.context.get('active_model') == 'financial.move' and
                active_id):
            fm = self.env['financial.move'].browse(active_id)
            res['currency_id'] = fm.currency_id.id
            res['amount'] = fm.amount
            res['payment_mode_id'] = fm.payment_mode_id.id
            # res['payment_term_id'] = fm.payment_term_id.id
            res['company_id'] = fm.company_id.id
            res['bank_id'] = fm.bank_id.id
        return res

    @api.multi
    def doit(self):
        for wizard in self:
            active_id = self._context['active_id']
            account_financial = self.env['financial.move']

            financial_to_pay = account_financial.browse(active_id)

            if financial_to_pay.financial_type == 'p':
                financial_type = 'pp'
            else:
                financial_type = 'rr'

            values = account_financial._prepare_financial_move(
                bank_id=wizard.bank_id.id,
                company_id=wizard.company_id.id,
                currency_id=wizard.currency_id.id,
                financial_type=financial_type,
                partner_id=financial_to_pay.partner_id.id,
                date=wizard.date_payment,
                document_number=financial_to_pay.document_number,
                date_maturity=financial_to_pay.date_maturity,
                amount=wizard.amount,
                account_id=financial_to_pay.account_id.id,
                financial_payment_id=active_id,
                date_credit_debit=wizard.date_credit_debit,
            )
            financial = account_financial.create(values)
            financial.action_confirm()
