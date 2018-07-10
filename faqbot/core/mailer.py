"""This file contains the reply-all routine."""

import faqbot.legacy.email_finder as email_finder

from faqbot.config import *
from email.utils import getaddresses, parseaddr, make_msgid
from email.mime.text import MIMEText

import smtplib

def reply_email(reply_object, body):
    sujet = reply_object['subject']
    reply_sujet = "Re: " + sujet if not sujet.startswith('Re:') else sujet
    recipients = []
    for r in reply_object['all_recipients']:
        recipients.append(r[1])

    # Try to find the initial sender
    re = reply_object['raw_email']

    if len(re.split('From: ')) >= 2:
        re = re.split('From: ')[1]

    recipients += email_finder.get_emails(re)

    # Remove dupes
    recipients = list(set(recipients))

    print recipients

    msg = MIMEText(body, 'html')
    msg['Subject'] = reply_sujet
    msg["Message-ID"] = make_msgid()
    msg["In-Reply-To"] = reply_object['msg_id']
    msg["References"] = reply_object['msg_id']
    msg["To"] = ", ".join(recipients)
    msg["From"] = MAIL_FROM

    s = smtplib.SMTP_SSL(SMTP_SERVER)
    s.login(SEND_MAIL_USER, SEND_MAIL_PASSWORD)
    s.sendmail(MAIL_FROM, recipients, msg.as_string())
    s.quit()