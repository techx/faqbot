'''
    This was written by Shreyas Kapur in collaboration with 
    Michael Kaminsky
    https://github.com/mkaminsky11
'''

from config import *
from faq import *
import quill
import email
from email.utils import getaddresses, parseaddr
from email.mime.text import MIMEText
import smtplib
from flanker import mime

import imaplib2, time
from threading import *
import email_finder

class Idler(object):
    def __init__(self, conn, last_id):
        self.thread = Thread(target=self.idle)
        self.mail = conn
        self.event = Event()
        self.last_id = last_id

    def start(self):
        self.thread.start()

    def stop(self):
        self.event.set()

    def join(self):
        self.thread.join()

    def idle(self):
        while True:
            try:
                if self.event.isSet():
                    return
                self.needsync = False

                def callback(args):
                    if not self.event.isSet():
                        self.needsync = True
                        self.event.set()

                self.mail.idle(callback=callback)
                self.event.wait()
                if self.needsync:
                    self.event.clear()
                    self.dosync()
            except Exception as e:
                continue # TO-DO Better error handling.

    # The method that gets called when a new email arrives.
    def dosync(self):
        print "You\'ve Got Mail."
        did_except = True
        while did_except:
            try:
                result, data = self.mail.search(None, "ALL")
                did_except = False
            except:
                # Attempt reconnect
                did_except = True
                print "Disconnected, attempting reconnect."
                self.mail = imaplib2.IMAP4_SSL(IMAP_SERVER)
                self.mail.login(MAIL_USER, MAIL_PASSWORD)

                self.mail.select("inbox", readonly=True)

        ids = data[0]
        id_list = ids.split()
        new_mail_ids = []

        if id_list[-1] < self.last_id:
            new_mail_ids = []
        else:
            for i in xrange(len(id_list)-1, 0, -1):
                if id_list[i] == self.last_id:
                    break
                else:
                    new_mail_ids.append(id_list[i])
        self.last_id = id_list[-1]

        for mail_id in new_mail_ids:
            result, data = self.mail.fetch(mail_id, "(RFC822)")
            # print data
            raw_email = "null"
            for d in data:
                if type(d) is tuple:
                    if "RFC822" in d[0]:
                        raw_email = d[1]

            if raw_email == "null":
                continue

            email_message = email.message_from_string(raw_email)
            flanker_msg = mime.from_string(raw_email)

            body = "null"

            try:
                for part in flanker_msg.parts:
                    if part.body.encode('ascii', 'ignore').startswith(TRIGGER):
                        body = part.body.encode('ascii', 'ignore')
                        break
            except Exception as e:
                pass

            # If body is still null, just look for this stuff
            if body == "null":
                for l in raw_email.split('\n'):
                    if l.startswith(TRIGGER):
                        body = l

            # CR-LF ugh
            body = body.replace('\r', '')

            if body.startswith(TRIGGER) and "From" in email_message:
                if len(body.split(' ')) >= 2:
                    command = body.split(' ')[1].strip()

                    # Ugly custom rule
                    if command.startswith('edu'):
                        command = "edu"
                    if command.startswith('mixed'):
                        command = "mixed"

                    # Hacky
                    for c in COMMANDS.keys():
                        if command.startswith(c):
                            command = c
                            break
                else:
                    command = "faq"

                print "Request from {} for subject {} with command {}.".format(email_message["From"], email_message["Subject"], command)
                tos = email_message.get_all('to', [])
                ccs = email_message.get_all('cc', [])
                all_recipients = getaddresses(tos + ccs) + [parseaddr(email_message["Reply-To"] or email_message["From"])]

                if command.startswith('whitelist'):
                    # Compute the whitelist email
                    wl_email = None
                    for line in body.split('\n'):
                        if line.startswith(TRIGGER):
                            tokens = line.split(' ')
                            if len(tokens) >= 3:
                                wl_email = tokens[2]

                    if not wl_email:
                        return

                    print "Whitelist Email:", wl_email

                    # Post to quill
                    quill.post_wl(quill.get_wl() + [wl_email])

                    content = COMMANDS['whitelist'].format(email=wl_email) + FOOTER
                else:
                    if command not in COMMANDS:
                        return
                    content = COMMANDS[command] + FOOTER

                reply_sujet = "Re: " + email_message["Subject"] if not email_message['Subject'].startswith('Re:') else email_message["Subject"]
                recipients = []
                for r in all_recipients:
                    recipients.append(r[1])

                # Try to find the initial sender
                recipients += email_finder.get_emails(raw_email)

                # Remove dupes
                recipients = list(set(recipients))

                print recipients

                msg = MIMEText(content, 'html')
                msg['Subject'] = reply_sujet
                msg["Message-ID"] = email.utils.make_msgid()
                msg["In-Reply-To"] = email_message["Message-ID"]
                msg["References"] = email_message["Message-ID"]
                msg["To"] = ", ".join(recipients)
                msg["From"] = MAIL_FROM

                s = smtplib.SMTP_SSL(SMTP_SERVER)
                s.login(SEND_MAIL_USER, SEND_MAIL_PASSWORD)
                s.sendmail(MAIL_FROM, recipients, msg.as_string())
                s.quit()

# Set the following two lines to your creds and server
mail = imaplib2.IMAP4_SSL(IMAP_SERVER)
mail.login(MAIL_USER, MAIL_PASSWORD)

mail.select("[Gmail]/All Mail", readonly=True)

result, data = mail.search(None, "ALL")

ids = data[0]
id_list = ids.split()
latest_email_id = id_list[-1]


idler = Idler(mail, latest_email_id)
idler.start()

print "Client started on {}, waiting for emails.".format(MAIL_USER)
while True:
    try:
        time.sleep(0.3)
    except KeyboardInterrupt:
        print "Bye"
        break

idler.stop()
idler.join()
mail.close()
mail.logout()
