"""This is legacy borrowed code, because email
parsing is still a mess. This hooks into callbacks
into neater functions and such, so I'll let this
be like this for now, and do all the new stuff in
the callbacks.
"""

'''
    This was written by Shreyas Kapur in collaboration with 
    Michael Kaminsky
    https://github.com/mkaminsky11
'''

from faqbot.config import *
from faqbot.core.store import load_config
from faqbot.core.utils import start_trigger
import email
from email.utils import getaddresses, parseaddr
from email.mime.text import MIMEText
import smtplib
from flanker import mime

import imaplib2, time
from threading import *
import faqbot.legacy.email_finder as email_finder

import pickle

import faqbot.core.callbacks as callbacks

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
            except Exception as _:
                continue # TO-DO Better error handling.

    # The method that gets called when a new email arrives.
    def dosync(self):
        print "You\'ve Got Mail."
        did_except = True
        while did_except:
            try:
                _, data = self.mail.search(None, "ALL")
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
            _, data = self.mail.fetch(mail_id, "(RFC822)")

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
                    pp = part.body.encode('ascii', 'ignore')
                    if start_trigger(pp, TRIGGERS):
                        body = pp
                        break
            except Exception as _:
                pass

            # If body is still null, just look for this stuff
            if body == "null":
                for l in raw_email.split('\n'):
                    if start_trigger(l, TRIGGERS):
                        body = l

            # CR-LF ugh
            body = body.replace('\r', '')

            tos = email_message.get_all('to', [])
            ccs = email_message.get_all('cc', [])
            all_recipients = getaddresses(tos + ccs) + [parseaddr(email_message["Reply-To"] or email_message["From"])]

            reply_object = {
                'subject': email_message["Subject"],
                'all_recipients': all_recipients,
                'raw_email': raw_email,
                'msg_id': email_message["Message-ID"]
            }

            if start_trigger(body, TRIGGERS) and "From" in email_message:
                print "Request from {} for subject {}.".format(email_message["From"], email_message["Subject"])
                
                argv = [x.strip() for x in body.split()]
                callbacks.triggered_email(body, argv, reply_object)
            else:
                callbacks.raw_email(flanker_msg, raw_email, reply_object)

def start_mail_thread():
    print "Starting mail thread!"
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

    # # while True:
    # #     try:
    # #         time.sleep(0.3)
    # #     except KeyboardInterrupt:
    # #         print "Bye"
    # #         break

    # idler.stop()
    # idler.join()
    # mail.close()
    # mail.logout()
