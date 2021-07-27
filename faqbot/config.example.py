"""Main configuration file. Can either pull from the
environment or from this file.
"""

from faqbot.config import MAIL_BOX
import os

"""
===== WEB SPECIFIC =====
"""

# What's this app called?
APP_NAME = os.environ.get("APP_NAME", "faqbot")

# App network port.
PORT = os.environ.get("PORT", 8114)

# Is the app running in debug mode?
DEBUG = bool(os.environ.get("DEBUG", False))

# Secret for JWTs.
SECRET = os.environ.get("SECRET", "CHANGE THIS")

# Admin password.
ADMIN_PASSWORD = os.environ.get("ADMIN_PASSWORD", "P9Jt_B=uMvgu6#EG")

"""
===== MAIL SPECIFIC =====
"""

# IMAP server details.
IMAP_SERVER = ["imap.gmail.com"] # if you have a custom Port [serverDNS, port]
SMTP_SERVER = ["smtp.gmail.com"] # if you have a custom Port [serverDNS, port]
MAIL_USER = "admin@hackmit.org"
MAIL_PASSWORD = "CHANGE THIS"
MAIL_BOX = "[Gmail]/allmail"

# SMTP server details.
SEND_MAIL_USER = MAIL_USER
SEND_MAIL_PASSWORD = MAIL_PASSWORD
MAIL_FROM = "team@hackmit.org"

# This footer is appended at the end of _every_ email
# sent by this bot. Just to make sure people can reach
# out again if they want to.
FOOTER = """
<br><br> <i>~~ This was an automated message, please <a href="mailto:team@hackmit.org">email us</a> again if this didn't help! ~~</i>
"""

TRIGGERS = ["@faqbot", "@fb"]
