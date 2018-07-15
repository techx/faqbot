from faqbot import app
from faqbot.config import ADMIN_PASSWORD
from faqbot.core.utils import get_menu

import datetime
import os

from faqbot.web.auth import requires_auth, encode_token, auth_request

from flask import send_from_directory, request, redirect, url_for, render_template


@app.route("/login", methods=["GET", "POST"])
def login():
    # Are we already auth?
    if auth_request(request):
        return redirect(url_for("index"))

    error = None

    if request.method == "GET":
        pass

    if request.method == "POST":
        # Perform auth.
        if request.form.get("faqbot_password", None) == ADMIN_PASSWORD:
            # Yay, let's construct the auth token.
            token = encode_token()
            response = app.make_response(redirect(url_for("index")))

            # Set the cookie. Yum.
            response.set_cookie(
                "jwt",
                token,
                expires=datetime.datetime.now() + datetime.timedelta(days=90),
            )

            return response
        else:
            error = "Wrong password. Boo."

    return render_template("login.html", error=error)


@app.route("/logout", methods=["GET", "POST"])
def logout():
    response = app.make_response(redirect(url_for("login")))
    response.set_cookie("jwt", "")
    return response


@app.route("/")
@requires_auth()
def index():
    menu = get_menu()
    return redirect(menu[0]["url"])
