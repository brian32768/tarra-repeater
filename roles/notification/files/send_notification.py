#!/usr/bin/env python
#
#  Send a notification message to a list of recipients.
#  Rate limit message sending to avoid hammering users when events repeat..
#
#   FIXME:
#   We should tell the user how many messages get supressed.
#   There should be a web accessible log of all messages.
#   The email should include a link to the log.
#
from __future__ import unicode_literals

import sys,os,socket,subprocess
import locale
import logging
import json
from twilio.rest import TwilioRestClient, exceptions
import smtplib
from email.mime.text import MIMEText

logger = logging.getLogger(__name__)
mailhost = "localhost"

def load_twilio_config():
    number     = os.environ.get('SMS_NUMBER')
    sms_sid    = os.environ.get('SMS_API_SID')
    sms_secret = os.environ.get('SMS_API_SECRET')
    return (number, sms_sid, sms_secret)

def load_recipients(recipients):
    with open(recipients) as json_file:
        json_data = json.load(json_file)
    return json_data

class SmsClient(object):
    def __init__(self):
        (twilio_number, twilio_sms_sid,
         twilio_sms_secret) = load_twilio_config()

        self.twilio_number = twilio_number
        self.twilio_client = TwilioRestClient(twilio_sms_sid,
                                              twilio_sms_secret)
    def send_message(self, body, to):
        self.twilio_client.messages.create(body=body,
                                           to=to, from_=self.twilio_number)

class SmtpClient(object):
    def __init__(self, mailhost):
        self.sender = 'root'
        self.mailhost = mailhost

    def send_message(self, subject, body, recipient):
        msg = MIMEText(body)
        msg['Subject'] = subject
        msg['From'] = self.sender
        msg['To'] = recipient

        s = smtplib.SMTP(self.mailhost)
        s.sendmail(self.sender, [recipient], msg.as_string())
        s.quit()

#========================================================================

def send_notification(recipient_file, sms_message, email_subject, email_body, mailhost='localhost'):

    recipients = load_recipients(recipient_file)

    # using the sms client requires environment variables we might not have,
    # so don't load it unless we need it
    sms_client = None
    for r in recipients:
        if 'phone_number' in r:
            try:
                sms_client = SmsClient()
            except exceptions.TwilioException as e:
                logger.error("Twilio credentials not found. Can't send SMS messages.")
            break

    smtp_client = SmtpClient(mailhost)

    count = 0
    for r in recipients:

        # Prefer SMS if it's available

        if 'phone_number' in r and sms_client:
            try:
                sms_client.send_message(sms_message, r['phone_number'])
                count += 1
                continue # Skip sending email
            except exceptions.TwilioRestException as e:
                logger.error("Twilio REST exception %s" % str(e))
            except Exception as e:
                logger.error("SMS exception %s" % str(e))

        # Come here if SMS is not working and try fallback email address,
        # or use a simple email account for primary notification target.

        if 'email' in r:
            try:
                smtp_client.send_message(email_subject, email_body, r['email'])
            except Exception as e:
                logger.error("Email exception %s" % str(e))

    return count


########################################################################

if __name__ == "__main__":
    
    hostname=socket.gethostname() # Get my hostname.

    count = send_notification('test.list',
                              "SMS notification test from %s" % hostname,
                              "Email notification test", "Test from %s" % hostname,
                              mailhost = "localhost")

    logger.info('Notifications sent: %d' % count)
    exit(0)
