"""This is the classic faqbot usecase
of replying to people with predefined
templates.
"""

from faqbot.features import Feature
from faqbot.legacy.faq import COMMANDS
from faqbot.core.mailer import reply_email

from faqbot.core.store import (
    gen_defaults,
    Store
)

DEFAULTS = {
    'enabled': True,
    'templates': COMMANDS, # Import defaults from legacy.
}

STORE = "templates"

gen_defaults(DEFAULTS, STORE)

class Templates(Feature):
    @staticmethod
    def triggered_callback(body, argv, reply_object):
        if len(argv) >= 2:
            command = argv[1]

            with Store(STORE) as config:
                if command in config['templates']:
                    reply = config['templates'][command]
                    reply_email(reply_object, reply)

                    return

    @staticmethod
    def raw_callback(parsed, raw, reply_object):
        pass

    @staticmethod
    def get_name():
        return "Templates"

    @staticmethod
    def get_url():
        return "/templates"