
from odoo import models, fields, api
from collections import defaultdict
import logging
_logger = logging.getLogger(__name__)

class Invoice(models.Model):
    _inherit = 'account.move'

    def compute_tax_total(self):
        tax_totals = defaultdict(lambda: {'price_without_tax': 0.0, 'price_with_tax': 0.0})  # Default dict with a lambda to store both sums

        for line in self.invoice_line_ids:
            for tax in line.tax_ids:
                _logger.info(" --- tax --- %s", tax)
                _logger.info(" --- tax --- %s", line.price_subtotal)
                _logger.info(" --- tax --- %s", line.price_total)

                # Accumulate sum for both price_without_tax and price_with_tax for each tax
                tax_totals[tax]['price_without_tax'] += line.price_subtotal
                tax_totals[tax]['price_with_tax'] += line.price_total

        tax_summary = []
        for tax, totals in tax_totals.items():
            total_tax_price = totals['price_with_tax'] - totals['price_without_tax']
            # Now calculate the tax totals based on the accumulated values
            tax_summary.append({
                'taxname': tax.name,  # Tax name
                'taxtotal_without_tax': totals['price_without_tax'],  # Sum of price_without_tax
                'taxtotal_with_tax': totals['price_with_tax'],  # Sum of price_with_tax
                'total_tax_price': total_tax_price  # Total tax price calculated
            })

        return tax_summary
    
class StockMove(models.Model):
    _inherit = "stock.move"

    
    product_note = fields.Char(string="Note")
    

