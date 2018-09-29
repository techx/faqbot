"""This is the classic faqbot usecase
of replying to people with predefined
templates.
"""

from faqbot import app
from faqbot.web.auth import requires_auth
from faqbot.core.utils import get_menu
from faqbot.features.feature import Feature
from faqbot.legacy.faq import COMMANDS
from faqbot.core.mailer import reply_email

from faqbot.core.store import gen_defaults, load_config, Store

from flask import request, render_template, redirect, url_for

import datetime
import random

DEFAULTS = {
    "enabled": True,
    "templates": COMMANDS,  # Import defaults from legacy.
    "autosign": False,
    "signature": "Hackbot",
}

STORE = "templates"
NEWLINE = "<br>"

gen_defaults(DEFAULTS, STORE)


def generate_closing():
    """Helper function that generates a closing signature.
    The signature doesn't start with any new lines, and is
    up to the caller to add the <br> tags.
    """

    now = datetime.datetime.now()

    time_options = [
        (4 <= now.weekday() <= 6, "Have a great weekend!"),
        (5 <= now.hour < 8, "Have a good evening!"),
        (True, "Have a great week!"),
    ]

    signoff_options = ["Best", "Cheers", "Regards"]

    with Store(STORE) as s:
        return (
            next(
                option + 2 * NEWLINE for condition, option in time_options if condition
            )  # Have a great something.
            + random.choice(signoff_options)
            + ","
            + NEWLINE  # Best,
            + s["signature"]  # Hackbot
        )


class Templates(Feature):
    @staticmethod
    def triggered_callback(body, argv, reply_object):
        if len(argv) >= 2:
            command = argv[1]

            with Store(STORE) as s:
                if command in s["templates"] and s["enabled"]:
                    reply = s["templates"][command]

                    if s["autosign"]:
                        reply += 2*NEWLINE + generate_closing()

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


# Web control panel render.
@app.route(Templates.get_url())
@requires_auth()
def templates_panel():
    config = load_config(STORE)
    return render_template("templates.html", menu=get_menu(), c=config)


@app.route(Templates.get_url() + "/api/enable")
@requires_auth()
def enable_templates():
    with Store(STORE) as s:
        s["enabled"] = True
    return "OK"


@app.route(Templates.get_url() + "/api/disable")
@requires_auth()
def disable_templates():
    with Store(STORE) as s:
        s["enabled"] = False
    return "OK"

@app.route(Templates.get_url() + "/api/autosign/on")
@requires_auth()
def enable_autosign():
    with Store(STORE) as s:
        s["autosign"] = True
    return "OK"


@app.route(Templates.get_url() + "/api/autosign/off")
@requires_auth()
def disable_autosign():
    with Store(STORE) as s:
        s["autosign"] = False
    return "OK"

@app.route(Templates.get_url() + "/api/set", methods=["POST"])
@requires_auth()
def set_template():
    key = request.form.get("key", None)
    if key is None or key.strip() == "":
        return redirect(url_for("templates_panel"))

    with Store(STORE) as s:
        s["templates"][key] = request.form.get("value")

    return redirect(url_for("templates_panel"))


@app.route(Templates.get_url() + "/delete/<key>")
@requires_auth()
def delete_template(key):
    with Store(STORE) as s:
        del s.store["templates"][key]

    return redirect(url_for("templates_panel"))

@app.route(Templates.get_url() + "/api/signature", methods=["POST"])
@requires_auth()
def set_signature():
    signature = request.form.get("signature", DEFAULTS["signature"])

    with Store(STORE) as s:
        s["signature"] = signature 

    return redirect(url_for("templates_panel"))