"""Main file to run the entire faq-bot app.

This runs the webserver and the background listener thread
for incoming emails.
"""

from faqbot import app
from faqbot.config import PORT, DEBUG

if __name__ == '__main__':
    app.run(
        host='0.0.0.0',
        port=PORT,
        debug=DEBUG
    )