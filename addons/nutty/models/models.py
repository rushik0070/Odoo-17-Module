# -*- coding: utf-8 -*-

from odoo import models, fields, api ,tools, _
import logging
from odoo.exceptions import ValidationError
from odoo.tools import float_is_zero, float_compare, float_round, format_date, groupby
_logger = logging.getLogger(__name__)
import re

class ProductProduct(models.Model):
    _inherit = "product.product"
    

    variant_uom_id = fields.Many2one(
        'uom.uom', 
        string="Variant UoM", 
        help="Specific UoM for this variant, overrides product's UoM if set."
    )

    variant_uom_qty = fields.Float(string="Variant Uom Qty")

    variant_uom_category_id = fields.Many2one(
        'uom.category', 
        string="Variant UoM Category",
        related='product_tmpl_id.uom_id.category_id',
        store=True,
        readonly=True
    )

    @api.constrains('variant_uom_qty')
    def check_variant_uom_qty(self):
        for rec in self:
            if rec.variant_uom_qty < 0:
                raise ValidationError("Variant UoM Qty cannot be negative.")


class ProductTemplate(models.Model):
    _inherit = "product.template"
    

    variant_uom_id = fields.Many2one(
        'uom.uom', 
        string="Variant UoM", 
        help="Specific UoM for this variant, overrides product's UoM if set."
    )

    variant_uom_qty = fields.Float(string="Variant Uom Qty")

    variant_uom_category_id = fields.Many2one(
        'uom.category', 
        string="Variant UoM Category",
        related='uom_id.category_id',
        store=True,
        readonly=True
    )

    @api.constrains('variant_uom_qty')
    def check_variant_uom_qty(self):
        for rec in self:
            if rec.variant_uom_qty < 0:
                raise ValidationError("Variant UoM Qty cannot be negative.")


class PriceListItemInehrit(models.Model):
    _inherit = "product.pricelist.item"

    def _compute_price(self, product, quantity, uom, date, currency=None):
        """Compute the unit price of a product in the context of a pricelist application.

        Note: self and self.ensure_one()

        :param product: recordset of product (product.product/product.template)
        :param float qty: quantity of products requested (in given uom)
        :param uom: unit of measure (uom.uom record)
        :param datetime date: date to use for price computation and currency conversions
        :param currency: currency (for the case where self is empty)

        :returns: price according to pricelist rule or the product price, expressed in the param
                  currency, the pricelist currency or the company currency
        :rtype: float
        """
        self and self.ensure_one()  # self is at most one record
        product.ensure_one()
        uom.ensure_one()

        currency = currency or self.currency_id or self.env.company.currency_id
        currency.ensure_one()

        # Pricelist specific values are specified according to product UoM
        # and must be multiplied according to the factor between uoms
        product_uom = product.uom_id
        if product_uom != uom:
            convert = lambda p: product_uom._compute_price(p, uom)
        else:
            convert = lambda p: p

        if self.compute_price == 'fixed':

            if product.product_tmpl_id.product_variant_count > 1:
                # _logger.info("This is a variant of a product template.")
                # _logger.info("product %s",product)
                # _logger.info("variant_uom_id %s",product.variant_uom_id)
                # _logger.info("variant_uom_qty %s",product.variant_uom_qty)
                variant_uom_id = product.variant_uom_id
                variant_uom_qty = product.variant_uom_qty
            else:
                # _logger.info("This is a main product template.")
                # _logger.info("product %s",product)
                # _logger.info("variant_uom_id %s",product.product_tmpl_id.variant_uom_id)
                # _logger.info("variant_uom_qty %s",product.product_tmpl_id.variant_uom_qty)
                variant_uom_id = product.product_tmpl_id.variant_uom_id
                variant_uom_qty = product.product_tmpl_id.variant_uom_qty

            if variant_uom_id and variant_uom_qty:
                ratio = variant_uom_id.factor if variant_uom_id.factor else False
                if ratio and self.fixed_price:
                    price = (ratio * self.fixed_price) / variant_uom_qty
                else:
                    price = convert(self.fixed_price)
            else:
                price = convert(self.fixed_price)
        elif self.compute_price == 'percentage':
            base_price = self._compute_base_price(product, quantity, uom, date, currency)
            price = (base_price - (base_price * (self.percent_price / 100))) or 0.0
        elif self.compute_price == 'formula':
            base_price = self._compute_base_price(product, quantity, uom, date, currency)
            # complete formula
            price_limit = base_price
            price = (base_price - (base_price * (self.price_discount / 100))) or 0.0
            if self.price_round:
                price = tools.float_round(price, precision_rounding=self.price_round)

            if self.price_surcharge:
                price += convert(self.price_surcharge)

            if self.price_min_margin:
                price = max(price, price_limit + convert(self.price_min_margin))

            if self.price_max_margin:
                price = min(price, price_limit + convert(self.price_max_margin))
        else:  # empty self, or extended pricelist price computation logic
            price = self._compute_base_price(product, quantity, uom, date, currency)

        return price

class ResPartner(models.Model):
    _inherit = 'res.partner'

    user_pricelist_id = fields.Many2one(
        'product.pricelist',
        string='Customer type',
        help='Select a customer type for this partner'
    )

class ProductPackaging(models.Model):
    _inherit = "product.packaging"

    no_of_units = fields.Integer(string="No Of Units", default=0)

    def _find_suitable_product_packaging(self, product_qty, uom_id):
        """ try find in `self` if a packaging's qty in given uom is a divisor of
        the given product_qty. If so, return the one with greatest divisor.
        """
        packagings = self.sorted(lambda p: p.qty, reverse=True)
        for packaging in packagings:
            new_qty = packaging._check_qty(product_qty, uom_id)
            if new_qty == product_qty:
                return packaging
            else:
                return packaging
        return self.env['product.packaging']

class SaleOrderLine(models.Model):
    _inherit = 'sale.order.line'

    name = fields.Text(
        string="Product Name",
        compute='_compute_name',
        store=True, readonly=False, required=True, precompute=True)
    
    product_packaging_qty = fields.Float(
        string="Amount of Cases",
        compute='_compute_product_packaging_qty',
        store=True, readonly=False, precompute=True)
    
    @api.depends('product_id','product_packaging_id')
    def _compute_name(self):
      
        for line in self:
           
            if not line.product_id:
                continue
            lang = line.order_id._get_lang()
            if lang != self.env.lang:
                line = line.with_context(lang=lang)


            # Custom Code Added For Change Product Name
            name = line._get_sale_order_line_multiline_description_sale()
            new_name = re.search(r'\](.*)', name)
            if new_name != None:
                result = new_name.group(1)
            else:
                result = name

            if line.product_packaging_id:
                name = f'{result} - {line.product_packaging_id.name}'
            else:
                name = result

            if line.is_downpayment and not line.display_type:
                context = {'lang': lang}
                dp_state = line._get_downpayment_state()
                if dp_state == 'draft':
                    name = _("%(line_description)s (Draft)", line_description=name)
                elif dp_state == 'cancel':
                    name = _("%(line_description)s (Canceled)", line_description=name)
                else:
                    invoice = line._get_invoice_lines().filtered(
                        lambda aml: aml.quantity >= 0
                    ).move_id.filtered(lambda move: move.move_type == 'out_invoice')
                    if len(invoice) == 1 and invoice.payment_reference and invoice.invoice_date:
                        name = _(
                            "%(line_description)s (ref: %(reference)s on %(date)s)",
                            line_description=name,
                            reference=invoice.payment_reference,
                            date=format_date(line.env, invoice.invoice_date),
                        )
                del context
            
            line.name = name
    
    @api.onchange('product_packaging_id')
    def _onchange_product_packaging_id(self):
        if self.product_packaging_id and self.product_uom_qty:
            newqty = self.product_packaging_id._check_qty(self.product_uom_qty, self.product_uom, "UP")
            _logger.info("new qty $$$$$$$$$$$$ %s",newqty)
            _logger.info("product_packaging_qty $$$$$$$ %s",self.product_packaging_qty)
            self.product_packaging_qty = 1
            # if float_compare(newqty, self.product_uom_qty, precision_rounding=self.product_uom.rounding) != 0:
            #     return {
            #         'warning': {
            #             'title': _('Warning'),
            #             'message': _(
            #                 "This product is packaged by %(pack_size).2f %(pack_name)s. You should sell %(quantity).2f %(unit)s.",
            #                 pack_size=self.product_packaging_id.qty,
            #                 pack_name=self.product_id.uom_id.name,
            #                 quantity=newqty,
            #                 unit=self.product_uom.name
            #             ),
            #         },
            #     }
            
    @api.depends('product_id', 'product_uom_qty', 'product_uom')
    def _compute_product_packaging_id(self):
        _logger.info("_compute_product_packaging_id $$$$$$ is called %s",self)
        for line in self:
            if line.product_packaging_id.product_id != line.product_id:
                _logger.info("first if is working ############")
                line.product_packaging_id = False

            if line.product_id and line.product_uom_qty and line.product_uom:
                _logger.info("secound if is working ############")
                suggested_packaging = line.product_id.packaging_ids\
                        .filtered(lambda p: p.sales and (p.product_id.company_id <= p.company_id <= line.company_id))\
                        ._find_suitable_product_packaging(line.product_uom_qty, line.product_uom)
                line.product_packaging_id = suggested_packaging or line.product_packaging_id

class AccountPaymentTerm(models.Model):
    _inherit = "account.payment.term" 

    is_default_payment_term = fields.Boolean(string="Default Term For Sale Order",default=False)

    
class SaleOrder(models.Model):
    _inherit = 'sale.order'

    def _default_payment_term_id(self):
        return self.env['account.payment.term'].search([('is_default_payment_term','=',True)],limit=1)

    @api.depends('partner_id')
    def _compute_payment_term_id(self):
        _logger.info("_compute_payment_term_id $$$$$$$$ %s")
        for order in self:
            order = order.with_company(order.company_id)
            if order.partner_id.property_payment_term_id:
                order.payment_term_id = order.partner_id.property_payment_term_id

    picking_ids = fields.One2many(
        comodel_name='stock.picking',
        inverse_name='group_id',
        string='Stock Pickings',
    )

    payment_term_id = fields.Many2one(
        comodel_name='account.payment.term',
        string="Payment Terms",
        compute='_compute_payment_term_id',
        default = _default_payment_term_id,
        store=True, readonly=False, precompute=True, check_company=True, # Unrequired company
        domain="['|', ('company_id', '=', False), ('company_id', '=', company_id)]")

    stage = fields.Selection(
        [
            ('new', 'New Order'),
            ('reorder','Re-Order'),
            ('processing', 'Processing'),
            ('dispatched', 'Dispatched'),
            ('complete', 'Complete'),
            ('cancel', 'Cancelled'),
        ],
        string='Stage',
        group_expand='_expand_groups',
        compute='_compute_stage',
        store=True,
        tracking=True,
    )

    @api.model
    def _expand_groups(self, states, domain, order):
        return ['new', 'reorder', 'processing', 'dispatched', 'complete','cancel']

    @api.depends('state', 'picking_ids.state','partner_id')
    def _compute_stage(self):
        """
        Compute the stage based on the sales order state and stock picking state.
        - New Order: Sale order in draft or sent state.
        - Processing: Sale order in sale state, pickings are not ready.
        - Dispatched: Sale order in sale state, pickings are ready.
        - Complete: Sale order in done state or pickings are done.
        """

        for order in self:
            picking_states = order.picking_ids.mapped('state') if order.picking_ids else []
           
            # Default to 'new'
            stage = 'new'

            partner_orders = self.env['sale.order'].search([('partner_id', '=', order.partner_id.id),('state', '=', order.state)])

            if len(partner_orders) > 1:
                stage = 'reorder'
                        
            if order.state == 'sale':
                if 'assigned' in picking_states:
                    stage = 'dispatched'
                elif 'done' in picking_states:
                    stage = 'dispatched'
                else:
                    stage = 'processing'
            elif order.state == 'cancel':
                stage = 'cancel'
            
            # if 'invoiced' in invoice_states:  # When invoices are fully done
            #     stage = 'complete'

            order.stage = stage

    @api.onchange('partner_id')
    def _onchange_partner_id_set_pricelist(self):
        if self.partner_id and self.partner_id.user_pricelist_id:
            self.pricelist_id = self.partner_id.user_pricelist_id
        else:
            # Optionally, set a default pricelist if partner has none
            self.pricelist_id = False
    
    @api.depends('state', 'order_line.invoice_status')
    def _compute_invoice_status(self):
        """
        Compute the invoice status of a SO. Possible statuses:
        - no: if the SO is not in status 'sale' or 'done', we consider that there is nothing to
          invoice. This is also the default value if the conditions of no other status is met.
        - to invoice: if any SO line is 'to invoice', the whole SO is 'to invoice'
        - invoiced: if all SO lines are invoiced, the SO is invoiced.
        - upselling: if all SO lines are invoiced or upselling, the status is upselling.
        """
        confirmed_orders = self.filtered(lambda so: so.state == 'sale')
        (self - confirmed_orders).invoice_status = 'no'
        if not confirmed_orders:
            return
        lines_domain = [('is_downpayment', '=', False), ('display_type', '=', False)]
        line_invoice_status_all = [
            (order.id, invoice_status)
            for order, invoice_status in self.env['sale.order.line']._read_group(
                lines_domain + [('order_id', 'in', confirmed_orders.ids)],
                ['order_id', 'invoice_status']
            )
        ]
        for order in confirmed_orders:
            line_invoice_status = [d[1] for d in line_invoice_status_all if d[0] == order.id]
            if order.state != 'sale':
                order.invoice_status = 'no'
            elif any(invoice_status == 'to invoice' for invoice_status in line_invoice_status):
                if any(invoice_status == 'no' for invoice_status in line_invoice_status):
                    # If only discount/delivery/promotion lines can be invoiced, the SO should not
                    # be invoiceable.
                    invoiceable_domain = lines_domain + [('invoice_status', '=', 'to invoice')]
                    invoiceable_lines = order.order_line.filtered_domain(invoiceable_domain)
                    special_lines = invoiceable_lines.filtered(
                        lambda sol: not sol._can_be_invoiced_alone()
                    )
                    if invoiceable_lines == special_lines:
                        order.invoice_status = 'no'
                    else:
                        order.invoice_status = 'to invoice'
                else:
                    order.invoice_status = 'to invoice'
            elif line_invoice_status and all(invoice_status == 'invoiced' for invoice_status in line_invoice_status):
                order.invoice_status = 'invoiced'
            elif line_invoice_status and all(invoice_status in ('invoiced', 'upselling') for invoice_status in line_invoice_status):
                order.invoice_status = 'upselling'
            else:
                order.invoice_status = 'no'
            if order.invoice_status == 'invoiced':
                order.stage = 'complete'