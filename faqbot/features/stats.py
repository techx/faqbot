"""The stats feature is a mandotary feature
that collects various aggregated information
about all the faqbot emails for fun.
"""

from faqbot import app
from faqbot.web.auth import requires_auth
from faqbot.core.utils import get_menu
from faqbot.features.feature import Feature

import math

from faqbot.core.store import gen_defaults, Store

from flask import render_template

DEFAULTS = {"num_emails": 0}

STORE = "stats"

gen_defaults(DEFAULTS, STORE)


class Stats(Feature):
    @staticmethod
    def triggered_callback(body, argv, reply_object):
        # Let's simply increment our counter.
        with Store(STORE) as s:
            s["num_emails"] += 1

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
    with Store(STORE) as s:
        times = s["num_emails"]
        hours = int(round((times * 5) / 60.0))

    return render_template("stats.html", menu=get_menu(), times=times, hours=hours)


# A secret url for cheatsies :P
@app.route(Stats.get_url() + "/mod/<int:n>")
@requires_auth()
def mod_stats_number(n):
    with Store(STORE) as s:
        s["num_emails"] = n

    return "OK, new number is: " + str(n)
