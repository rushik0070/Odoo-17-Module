
from odoo import http
from odoo.http import request
import logging
_logger = logging.getLogger(__name__)

class Owl(http.Controller):

    @http.route('/get/task/data',auth="public",type="json")
    def fetch_task_data(self):
        task_object = request.env['owl.task'].sudo().search([])
        data = []
        for task in task_object:
            id = task.id
            task_name = task.name
            task_start_time = task.start_time
            task_end_time = task.end_time
            task_manager = task.task_manager.name
            task_priority = task.priority
            
            data.append({
                'id' : id,
                'task_name' : task_name,
                'task_start_time' : task_start_time,
                'task_end_time' : task_end_time,
                'task_manager' : task_manager,
                'task_priority' : task_priority
            })
            _logger.info("$$$$$ data $$$$$ %s",data)

        result = data
        
        _logger.info("$$$$$$ result $$$$$$$ %s",result)

        return result
    
    @http.route('/get/employee/name',auth="public",type="json")
    def fetch_employee_name(self):
        employee = request.env['hr.employee'].sudo().search([])
        return [{'id' : emp.id , 'name' : emp.name} for emp in employee]
    
    @http.route('/get/sale/data', auth='public',type="json")
    def fetch_sale_data(self):
        sale_objects = request.env['sale.order'].sudo().search([])
        total_quotation = sale_objects.filtered(lambda s : s.state == 'draft')
        _logger.info("total_quotation gettting ----->>>>> %s",total_quotation)
        total_order = sale_objects.filtered(lambda s: s.state == 'sale')
        _logger.info("total_order gettting ----->>>>> %s",total_order)

        order_name = sale_objects.mapped('name')
        untaxed = sale_objects.mapped('amount_untaxed')
        tax_amount = sale_objects.mapped('amount_tax')
        net_amount = sale_objects.mapped('amount_total')
        customer_name = sale_objects.mapped('partner_id.name')
        _logger.info("--- customer name ---- %s",customer_name)

        SaleOrderTable = request.env['sale.order']
        domain = ([])
        field = ['date_order','amount_untaxed','amount_tax','amount_total']
        groupby = ['partner_id']
        result = SaleOrderTable.read_group(
            domain=domain,
            fields=field,
            groupby=groupby
        )

        _logger.info("result ============%s",result)

        group_by_customer = []
        for customer in result:
            _logger.info("dic called ------- %s", customer)
            partner = customer.get('partner_id')
            if partner:  
                partner_name = partner[1]  
                group_data = {
                    'amount_untaxed': customer.get('amount_untaxed'),
                    'amount_tax': customer.get('amount_tax'),
                    'amount_total': customer.get('amount_total')
                }
                group_by_customer.append({partner_name: group_data})

        _logger.info(group_by_customer)

        data_dict = {
            'total_order' : len(sale_objects),
            'total_order_ids' : sale_objects.ids,
            'total_quotation' : len(total_quotation),
            'total_sale_quotation_ids' : total_quotation.ids,
            'total_sale_order' : len(total_order),
            'total_sale_order_ids' : total_order.ids,
            'order_ids' : sale_objects.mapped('id'),
            'order_name': order_name,
            'untaxed': untaxed,
            'tax_amount' : tax_amount,
            'net_amount' : net_amount,
            'customer_name' : customer_name,
            'group_by_customer' : group_by_customer
        }
        _logger.info(" --- data_dict object --- %s",data_dict)   
        return data_dict