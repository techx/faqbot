"""This file contains the reply-all routine."""

import faqbot.legacy.email_finder as email_finder

from faqbot.config import *
from email.utils import getaddresses, parseaddr, make_msgid
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.application import MIMEApplication

import smtplib

def init_finder(re):
    # Try to find the initial sender
    if len(re.split('From: ')) >= 2:
        re = ''.join(re.split('From: ')[1:])

    lines = re.split('\n')
    kk = []
    for x in lines:
        if (not 'Message-ID: ' in x):
            kk.append(x)

    re = "".join(kk)
    re = re.replace('[', '<').replace(']', '>')

    recipients = [x.replace('=', '') for x in email_finder.get_emails(re)]

    # Remove dupes
    recipients = list(set(recipients))

    return recipients

def reply_email(reply_object, body, attach=None, attach_fn="file.pdf", reply_one=None):
    sujet = reply_object['subject']
    reply_sujet = "Re: " + sujet if not sujet.startswith('Re:') else sujet
    recipients = []
    for r in reply_object['all_recipients']:
        recipients.append(r[1])

    re = reply_object['raw_email']
    recipients += init_finder(re)

    print recipients

    if attach is None:
        msg = MIMEText(body + FOOTER, 'html')
    else:
        msg = MIMEMultipart()
        msg.attach(MIMEText(body + FOOTER, 'html'))
        achh = MIMEApplication(attach)
        achh.add_header('Content-Disposition', 'attachment', filename=attach_fn)
        msg.attach(achh)

    msg['Subject'] = reply_sujet
    msg["Message-ID"] = make_msgid()
    msg["In-Reply-To"] = reply_object['msg_id']
    msg["References"] = reply_object['msg_id']

    if reply_one:
        msg["To"] = reply_one
        recipients = [reply_one]
    else:
        msg["To"] = ", ".join(recipients)

    msg["From"] = MAIL_FROM

    s = smtplib.SMTP_SSL(SMTP_SERVER)
    s.login(SEND_MAIL_USER, SEND_MAIL_PASSWORD)
    s.sendmail(MAIL_FROM, recipients, msg.as_string())
    s.quit()