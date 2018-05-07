#!/usr/bin/env python
# -- coding: utf-8 --

import smtplib
from logger import moonbbs_log
from datetime import datetime
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import sys

reload(sys)
sys.setdefaultencoding('utf8')

LOG = moonbbs_log()

class msg_queue(object):

    def __init__(self):
        LOG.debug('initialize the message queue')
        self.not_sent = []
        self.sent = []

    def enqueue(self, msg):
        if msg not in self.sent and msg not in self.not_sent:
            self.not_sent.append(msg)

    def flush(self, email_server=None):
        LOG.info('flushing all the messages in the not_sent queue')
        for msg in self.not_sent:
            email_server.sent_discount_info(msg)
            self.sent.append(msg)

        self.not_sent = []

    def store(self, repo=None):
        pass

    def clear(self):
        LOG.warning('cleaning all messages from both queues')
        self.not_sent = []
        self.sent = []

    def size_of_unsent(self):
        return len(self.not_sent)

    def size_of_sent(self):
        return len(self.sent)

class email_Notification(object):

    def __init__(self, username, password, host_email = 'smtp.gmail.com', port = 587):

        LOG.debug('setting up email notification')
        try:
            self.server = smtplib.SMTP(host_email, port)
            self.server.ehlo()
            self.server.starttls()
            self.server.ehlo()
            self.server.login(username, password)
        except Exception as e:
            LOG.error('email server setup failed, quiting....')
            raise e

        msg = "Email confirmation: email server setup complete"
        self.from_mail = username + '@gmail.com'
        try:
            self.server.sendmail(self.from_mail, self.from_mail, msg)
            LOG.debug('confirmation email sent')
        except Exception as e:
            LOG.error('confirmation email failed to deliver')
            raise e

    def quit(self):
        self.server.quit()

    def sent_discount_info(self, msg):
        message = MIMEMultipart()
        message['From'] = self.from_mail
        message['To'] = self.from_mail
        #message['Subject'] = 'Discount info at %s'%str(datetime.now())
        message['Subject'] = msg
        message.attach(MIMEText(str(msg)))
        self._email(message)

    def _email(self, msg):
        try:
            self.server.sendmail(self.from_mail, self.from_mail, msg.as_string())
            LOG.debug('email with info sent')
        except Exception as e:
            LOG.error('email failed to deliver')
            raise e
