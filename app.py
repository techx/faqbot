"""Main file to run the entire faq-bot app.

This runs the webserver and the background listener thread
for incoming emails.
"""

from faqbot import app
from faqbot.config import PORT, DEBUG
from faqbot.core.mail import start_mail_thread

if __name__ == '__main__':
    start_mail_thread()

    app.run(
        host='0.0.0.0',
        port=PORT,
        debug=DEBUG
    )