
from odoo import models, fields, api
import logging
_logger = logging.getLogger(__name__)

class notification(models.Model):
    _name = 'custom.notification'
    _description = 'custom.notification'

    name = fields.Char(string="Name")
    title = fields.Char(string="Title")
    send_to = fields.Many2many('res.users')
    send_by = fields.Many2one('res.users')
    message = fields.Text(string="Message")
    date = fields.Datetime(string="Date", default=fields.Datetime.now)
    status = fields.Selection([('sent', 'Sent'), ('not sent', 'Not Sent')],
                              string="Status", default='not sent')
    
   
    def send_notification(self,subject,body,send_to):
        _logger.info("self $$$$$$$$$$ %s",self)
        users = send_to
        _logger.info("users getting $$$$$$$$ %s",users)
        partner_ids = send_to.mapped('partner_id.id')
        # partner_ids = [(6,0,users.partner_id.id)]
        _logger.info("partner_ids getting $$$$$$$$ %s",partner_ids)
        if users:
            notifications = self.env['mail.message'].create({
                'message_type' : 'notification',
                'body' : body,
                'subject' : subject,
                'model' : self._name,
                'res_id' : self.id,
            })

            for partner_id in partner_ids:
                self.env['mail.notification'].create({
                'mail_message_id': notifications.id,
                'res_partner_id': partner_id,
                'notification_type': 'inbox',  # Explicitly set the type
                'notification_status': 'ready',  # Default status
                'is_read': False,  # Mark as unread
            })
                
            notifications.write({
                 'notified_partner_ids' : [(6,0,partner_ids)]
            })

            if notifications:
                _logger.info("notification ------- %s",notifications)



    def send_message(self,body,send_to):
        _logger.info("self $$$$$$$$$$ %s",self)

        reciver = send_to.mapped('partner_id.id')
        _logger.info("reciver getting $$$$$$$$ %s",reciver)
        sender = self.env.user
        send = sender.mapped('partner_id.id')
        _logger.info("sender getting $$$$$$$$ %s",send)
        marge = reciver + send
        _logger.info("marge getting $$$$$$$$ %s",marge)

        domain = [
                    ('channel_partner_ids' , '=' , reciver),
                    ('channel_partner_ids' , '=' , send),
                    ('channel_type','=','chat')
                ]
        discuss = self.env['discuss.channel'].search(domain)
        if discuss:
            _logger.info("discuss channel found $$$$$$$$ %s",[[d.name , d.id] for d in discuss])

            self.env['mail.message'].create({
                'author_id' : sender.partner_id.id,
                'body' : body,
                'subtype_id' : 1,
                'message_type' : 'comment',
                'model' : 'discuss.channel',
                'res_id' : discuss.id
            })
        else:
            _logger.info("discuss channel not found $$$$$$$$")

    def send_general_message(self):
        _logger.info("send_general_message $$$$$$$$$$ %s",self)
        for rec in self:
            subject = rec.title
            body = rec.message
            send_to = rec.send_to
            rec.send_notification(subject,body,send_to)

    def send_one_2_one_message(self):
        _logger.info("send_one_2_one_message $$$$$$$$$$ %s",self)
        for rec in self:
            body = rec.message
            send_to = rec.send_to
            rec.send_message(body,send_to)
    
   
