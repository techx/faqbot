"""This module handles the whitelist commands
and interfaces with quill.
"""

from faqbot import app
from faqbot.web.auth import requires_auth
from faqbot.core.utils import get_menu
from faqbot.features.feature import Feature
from faqbot.legacy.quill_api import post_wl, get_wl
from faqbot.core.mailer import reply_email

from faqbot.core.store import gen_defaults, load_config, Store

from flask import request, render_template, redirect, url_for

DEFAULTS = {
    "enabled": True,
    "quill_url": "https://my.hackmit.org/api/settings/whitelist",
    "quill_token": "",
    "reply": "Hi! <br><br> We've whitelisted the email address {email}. You can now use this for registration! <br><br> Best,<br> Hackbot",
}

STORE = "quill"

gen_defaults(DEFAULTS, STORE)


class Quill(Feature):
    @staticmethod
    def triggered_callback(body, argv, reply_object):
        if len(argv) >= 3:
            command = argv[1]
            email = argv[2]

            with Store(STORE) as s:
                if command == "whitelist" and s["enabled"]:
                    at = s["quill_token"]
                    ep = s["quill_url"]

                    already_whitelisted = get_wl(at, ep)
                    if email not in already_whitelisted:
                        post_wl(already_whitelisted + [email], at, ep)

                    reply = s["reply"].format(email=email)
                    reply_email(reply_object, reply)

                    return

    @staticmethod
    def raw_callback(parsed, raw, reply_object):
        pass

    @staticmethod
    def get_name():
        return "Quill"

    @staticmethod
    def get_url():
        return "/quill"


# Web control panel render.
@app.route(Quill.get_url())
@requires_auth()
def quill_panel():
    config = load_config(STORE)
    return render_template("quill.html", menu=get_menu(), c=config)


@app.route(Quill.get_url() + "/api/enable")
@requires_auth()
def enable_quill():
    with Store(STORE) as s:
        s["enabled"] = True
    return "OK"


@app.route(Quill.get_url() + "/api/disable")
@requires_auth()
def disable_quill():
    with Store(STORE) as s:
        s["enabled"] = False
    return "OK"


@app.route(Quill.get_url() + "/api/config", methods=["POST"])
@requires_auth()
def config_quill():
    with Store(STORE) as s:
        s["quill_url"] = request.form.get("quill_url")
        s["quill_token"] = request.form.get("quill_token")
        s["reply"] = request.form.get("reply")

    return redirect(url_for("quill_panel"))
