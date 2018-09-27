"""This module handles the whitelist commands
and interfaces with quill.
"""

from faqbot import app
from faqbot.web.auth import requires_auth
from faqbot.core.utils import get_menu
from faqbot.features.feature import Feature
from faqbot.core.mailer import reply_email

from faqbot.core.store import gen_defaults, load_config, Store

from flask import request, render_template, redirect, url_for
from dkim import dkim_verify, arc_verify
from email import message_from_string
from email.utils import parseaddr

DEFAULTS = {"enabled": False, "whitelist": []}

STORE = "whitelist"

gen_defaults(DEFAULTS, STORE)


class Whitelist(Feature):
    @staticmethod
    def triggered_callback(body, argv, reply_object):
        pass

    @staticmethod
    def raw_callback(parsed, raw, reply_object):
        pass

    @staticmethod
    def get_name():
        return "Whitelist"

    @staticmethod
    def get_url():
        return "/whitelist"


def is_whitelisted(body):
    # Read configuration and short circuit.
    with Store(STORE) as s:
        if not s["enabled"]:
            return True

        whitelist = s["whitelist"]

    return is_whitelisted_internal(body, whitelist=whitelist)

def is_whitelisted_internal(body, whitelist=[]):
    """This is a special method that is used by the mail parsing script to
    figure out of any of the callbacks must be triggered or not. This hook
    will not be called for any other feature.
    """
    # Let's make sure no spoofing is happening.
    if not (dkim_verify(body) or arc_verify(body)):
        print "No DKIM"
        return False

    parsed = message_from_string(body)
    from_address = parsed["From"]
    _, address = parseaddr(from_address)
    
    return address in whitelist


# Web control panel render.
@app.route(Whitelist.get_url())
@requires_auth()
def whitelist_panel():
    config = load_config(STORE)
    return render_template("whitelist.html", menu=get_menu(), c=config)


@app.route(Whitelist.get_url() + "/api/enable")
@requires_auth()
def enable_whitelist():
    with Store(STORE) as s:
        s["enabled"] = True
    return "OK"


@app.route(Whitelist.get_url() + "/api/disable")
@requires_auth()
def disable_whitelist():
    with Store(STORE) as s:
        s["enabled"] = False
    return "OK"


@app.route(Whitelist.get_url() + "/api/config", methods=["POST"])
@requires_auth()
def config_whitelist():
    with Store(STORE) as s:
        s["whitelist"] = request.form.get("whitelist").split()
        
    return redirect(url_for("whitelist_panel"))
