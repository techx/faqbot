"""The stats feature is a mandotary feature
that collects various aggregated information
about all the faqbot emails for fun.
"""

from faqbot import app
from faqbot.web.auth import requires_auth
from faqbot.features import Feature

from faqbot.core.store import (
    gen_defaults,
    Store
)

DEFAULTS = {
    'num_emails': 0
}

STORE = "stats"

gen_defaults(DEFAULTS, STORE)

class Stats(Feature):
    @staticmethod
    def triggered_callback(body, argv, reply_object):
        # Let's simply increment our counter.
        with Store(STORE) as config:
            config['num_emails'] += 1

    @staticmethod
    def raw_callback(parsed, raw, reply_object):
        pass

    @staticmethod
    def get_name():
        return "Statistics"

    @staticmethod
    def get_url():
        return "/stats"

# Web control panel render.
@app.route(Stats.get_url())
@requires_auth()
def stats_panel():
    return "Stats panel!"