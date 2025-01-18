from odoo import models,fields,api
import logging
_logger = logging.getLogger(__name__)
from datetime import datetime,timedelta
# import timedelta

class CommonModel(models.AbstractModel):
    _name = 'common.model'

    status = fields.Selection([('1','First'),('2','Secound'),('3','Third')])

class taskWizard(models.TransientModel):
    _name = 'task.wizard'

    start_date = fields.Date(string="Start Date")
    end_date = fields.Date(string="End Date")

    def click_to_pdf(self):
        for res in self:
            data = {
                'data' : 'this is a test',
                'test' : [
                    {
                        '1' : 'pass',
                        '2' : 'Full pass'
                    }
                ]
            }
            report = self.env.ref('owl.report_project_').report_action(res,data)
            _logger.info("this is test %s",report)
            return report


class Department(models.Model):
    _name = 'owl.department'
    
    name = fields.Char(string="Department Name")
    code = fields.Char(string="Code")
    employee_ids = fields.One2many('owl.employee','department_id',string="Employee")

    def _compute_display_name(self):
        for res in self:
            res.display_name = f"{res.name} - {res.code if res.code else '000'}"
       
class Employee(models.Model):
    _name = 'owl.employee'
    _inherit = 'common.model'

    code = fields.Char(string="Emp No.",readonly=True)
    name = fields.Char(string="Employee Name")
    department_id = fields.Many2one('owl.department',string="Department")
    # department_id = fields.Many2one('owl.department',string="Department")
    
    @api.model
    def create(self,vals):
        res = super(Employee,self).create(vals)
        res.code = self.env['ir.sequence'].next_by_code('owl.employee')
        return res

class owltask(models.Model):
    _name = 'owl.task'
    _inherit = 'common.model'

    name = fields.Char(string="Task Name")
    start_time = fields.Date(string="Task Start Time")
    end_time = fields.Date(string="Task End Time")
    task_manager = fields.Many2one('hr.employee',string="Task Manager")
    priority = fields.Selection([('low','low'),('mid','mid'),('high','high')],string="Priority")

    # @api.model
    def create(self,vals):
        res = super(owltask,self).create(vals)
        _logger.info("task is created ----->>>>>>> %s",res)
        return res
    
    # @api.model
    def write(self,vals):
        res = super(owltask,self).write(vals)
        _logger.info("task is updated ----->>>>>>> %s",res)
        return res
    
    def unlink(self):
        _logger.info("task is going to delete ----->>>>>>> %s",self)
        res = super(owltask,self).unlink()
        _logger.info("task is deleted ----->>>>>>> %s",res)
        return res
    
    @api.onchange('start_time')
    def _onchange_end_date(self):
        for res in self:
            if res.start_time:
                res.end_time = res.start_time + timedelta(days=1)
                _logger.info("end time is ----->>>>>>> %s",res.end_time)
                
    
    # @api.depends('start_time')
    # def _compute_task_end_date(self):
    #     for res in self:
    #         today = datetime.today() + timedelta(days=1)
    #         _logger.info("today is ----->>>>>>> %s",today)
    #         if res.start_time:
    #             res.end_time = today
    #             _logger.info("end time is ----->>>>>>> %s",res.end_time)

    # def _set_task_end_date(self):
    #     for res in self:
    #         if res.end_time:
    #             res.start_time = datetime.today()
    #             _logger.info("start time is ----->>>>>>> %s",res.start_time)
    
    def button_test_orm(self):
        for res in self:

            query = """
                        SELECT COUNT(*) , LOWER(name) , STRING_AGG(id::TEXT, ',') AS concatenated_ids
                        FROM owl_task 
                        GROUP BY LOWER(name)
                        HAVING COUNT(*) > 1 ;
            """
            # """
            #             SELECT ot.name , ot.priority , mn.name , mn.job_id , job.name 
            #             FROM owl_task ot
            #             RIGHT JOIN hr_employee MN ON ot.task_manager = mn.id 
            #             LEFT JOIN hr_job job ON MN.job_id = job.id
                        
            # """
            self.env.cr.execute(query)
            results = self.env.cr.fetchall()
            fianl_data = []
            name_list = []
            for res in results:
                _logger.info("->>>>>>> %s",res)
                name_list.append(res[1])
            
            query_for_id = """
                    SELECT * FROM owl_task WHERE  lower(name) IN %s
"""
            _logger.info(' name list - > %s',name_list)
            self.env.cr.execute(query_for_id,(tuple(name_list),))
            records = self.env.cr.fetchall()
            for rec in records:
                _logger.info("data based on name -->>> %s",rec)
            # owl_template = self.env.ref('owl.owl_test_template')
            # if owl_template:
            #     _logger.info(owl_template.name)
            #     owl_template.send_mail(res.id , force_send=True)
            # search_object = self.env['owl.task'].search([('priority','=','mid')])
            # _logger.info("search object is ----->>>>>>> %s",[search_object.name for search_object in search_object])
            # browse_object = self.env['owl.task'].browse(search_object.ids)
            # _logger.info("browse object is ----->>>>>>> %s",[browse_object.name for browse_object in browse_object])
            # coy_object = res.copy()
            # _logger.info("copy object is ----->>>>>>> %s",coy_object)
            # filtered_object = self.env['owl.task'].filtered(lambda x : x.name == 'project 1')
            # _logger.info("filtered object is ----->>>>>>> %s",filtered_object)
            # final_data = []
            # read_groups_objects = self.env['owl.task'].read_group(domain=[],fields=['priority','id:count'],groupby=['priority'])
            # for group_data in read_groups_objects:
            #     _logger.info("group data is ----->>>>>>> %s",group_data)
            #     group_data = {
            #          'name': group_data['priority'],
            #          'priority': group_data['priority'],
            #          'priority_count': group_data['priority_count']

            #     }
            #     final_data.append(group_data)
            # _logger.info("task button is clicked")
            # _logger.info("final data is ----->>>>>>> %s",final_data)

            # owl_employee = self.env['owl.employee'].search([])
            # _logger.info("employee is ----->>>>>>> %s",owl_employee)

            # owl_department = self.env['owl.department'].search([],limit=1)
            # _logger.info("department is ----->>>>>>> %s",owl_department)

            # owl_employee_create = self.env['owl.employee'].create({
            #     'name' : 'Wipro',
            #     'department_id' : owl_department.id
            # })

            # owl_department_create = self.env['owl.department'].create({
            #     'name' : 'Management',
            # })

            # employee = self.env['owl.employee'].create({
            #         'name' : 'INFosys',
            #         'department_id' : owl_department_create.id
            # }) 

            # owl_department_create.write({
            #     'employee_ids' : [(4,employee.id)]
            # })

            # employee = self.env['owl.employee'].create(
            #    [ {'name' : 'w1', 'department_id' : owl_department.id},
            #     {'name' : 'w2', 'department_id' : owl_department.id},
            #     {'name' : 'w3', 'department_id' : owl_department.id}])

            # _logger.info("employee $$$$$$$$$$$$$$$$ %s",employee)

        # {'priority': 'high', 'priority_count': 1, 'id': 1, '__domain': [('priority', '=', 'high')]} 
        # {'priority': 'low', 'priority_count': 1, 'id': 1, '__domain': [('priority', '=', 'low')]} 
        # {'priority': 'mid', 'priority_count': 3, 'id': 3, '__domain': [('priority', '=', 'mid')]} 

            # {'task_manager': (1, 'Administrator'), 'task_manager_count': 3, 'name': 3, '__domain': [('task_manager', '=', 1)]}