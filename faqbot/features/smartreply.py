"""This feature can definitely use some cleanup.

This is the smart reply module, which learns from all faqbot usages
in the past and learns to auto-reply.
"""

from faqbot import app
from faqbot.web.auth import requires_auth
from faqbot.core.utils import get_menu
from faqbot.features.feature import Feature
from faqbot.legacy.quill_api import post_wl, get_wl
from faqbot.core.mailer import reply_email
from flanker import mime
from email_reply_parser import EmailReplyParser

from faqbot.config import *

# ML
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.feature_extraction.text import TfidfTransformer
from sklearn.linear_model import SGDClassifier
from sklearn.pipeline import Pipeline
from sklearn.externals import joblib
import numpy as np
import pickle
import os

import imaplib2
import random
import email

from faqbot.core.store import gen_defaults, load_config, save_config, Store

from flask import request, render_template, redirect, url_for

DEFAULTS = {
    "enabled": False,
    "mock": True,
    "threshold": 0.6,
    "email": ["help@hackmit.org", "team@hackmit.org"],
}

STORE = "smartreply_settings"
MODEL_LOC = os.path.join("store", "smartreply_model.p")

gen_defaults(DEFAULTS, STORE)

# Also load the ML model if present.
if os.path.exists(MODEL_LOC):
    model = joblib.load(MODEL_LOC)


def collect_data():
    """Messy code to download training data.
    """
    c = load_config("templates")
    templates = c["templates"]

    training_data = []

    mail = imaplib2.IMAP4_SSL(IMAP_SERVER)
    mail.login(MAIL_USER, MAIL_PASSWORD)

    mail.select("[Gmail]/All Mail", readonly=True)

    result, data = mail.search(None, '(BODY "%s")' % ("@faqbot"))

    ids = data[0]
    id_list = ids.split()

    for idx, r_id in enumerate(id_list):
        _, data = mail.fetch(r_id, "(RFC822)")

        print "%i / %i (%i%%)" % (
            idx,
            len(id_list),
            int(float(idx) / len(id_list) * 100),
        )

        raw_email = "null"
        for d in data:
            if type(d) is tuple:
                if "RFC822" in d[0]:
                    raw_email = d[1]

        flanker_msg = mime.from_string(raw_email)

        body = "null"

        try:
            for part in flanker_msg.parts:
                if str(part) == "(text/plain)":
                    pp = part.body.encode("ascii", "ignore")
                    body = pp
        except Exception as _:
            pass

        if body == "null":
            continue

        parsed_body = EmailReplyParser.read(body)

        if len(parsed_body.fragments) >= 2:
            if parsed_body.fragments[0].content.split()[0] == "@faqbot":
                fb = parsed_body.fragments[0].content.split()[1]
                original = parsed_body.fragments[1].content

                lines = []

                for l in original.split("\n"):
                    if l.startswith("> "):
                        tl = l.replace(">", "").strip()
                        if tl != "" and not (tl.startswith("On")):
                            lines.append(l.replace(">", ""))

                key = fb
                original = "\n".join(lines)

                # Now that we have this, let's make sure it's
                # valid and stuff and then save it.

                if key in templates:
                    training_data.append((key, original))
                    save_config(training_data, "smartreply_data")


def train_model():
    """Messy code to build model.
    """
    data = load_config("smartreply_data")
    # data = [d for d in data if d[0] != 'whitelist']

    X = [d[1] for d in data]
    Y = [d[0] for d in data]

    text_clf_svm = Pipeline(
        [
            ("vect", CountVectorizer(stop_words="english")),
            ("tfidf", TfidfTransformer()),
            (
                "clf-svm",
                SGDClassifier(
                    loss="log", penalty="l2", alpha=1e-3, n_iter=5, random_state=42
                ),
            ),
        ]
    )

    text_clf_svm = text_clf_svm.fit(X, Y)
    joblib.dump(text_clf_svm, MODEL_LOC)
    # for p in preds:
    #     print np.max(p), text_clf_svm.classes_[np.argmax(p)]


class SmartReply(Feature):
    @staticmethod
    def triggered_callback(body, argv, reply_object):
        pass

    @staticmethod
    def raw_callback(parsed, raw, reply_object):
        print "[SR] Smartreply Callback!"
        with Store(STORE) as s:
            if not s["enabled"]:
                return

            body = "null"
            for part in parsed.parts:
                if str(part) == "(text/plain)":
                    body = part.body.encode("ascii", "ignore")

            print "[SR] Parsed body to:", body

            if body == "null":
                return

            body = EmailReplyParser.parse_reply(body)

            email_message = email.message_from_string(raw)

            print "[SR] To", email_message["To"]

            sent_to = None

            for e in s["email"]:
                if e in email_message["To"]:
                    sent_to = e

            if sent_to is None:
                return

            p = model.predict_proba([body])[0]

            confidence = np.max(p)
            class_ = model.classes_[np.argmax(p)]

            templates = load_config("templates")["templates"]

            print "[SR] Confidence %.2f, Class: %s" % (confidence, class_)

            if confidence > float(s["threshold"]) and class_ in templates:
                if s["mock"]:
                    reply = "<b>(Team Only, Confidence: %.2f)</b><br><br>" % confidence
                    reply += templates[class_]
                    reply_email(reply_object, reply, reply_one=sent_to)
                else:
                    reply = templates[class_]
                    reply_email(reply_object, reply)

                return

    @staticmethod
    def get_name():
        return "Smart Reply"

    @staticmethod
    def get_url():
        return "/smartreply"


# Web control panel render.
@app.route(SmartReply.get_url(), methods=["POST", "GET"])
@requires_auth()
def smart_reply_panel():
    prediction = None

    if request.method == "POST":
        if "text" in request.form:
            text = request.form["text"]
            p = model.predict_proba([text])[0]

            confidence = np.max(p)
            class_ = model.classes_[np.argmax(p)]

            prediction = (confidence, class_)

    return render_template(
        "smart_reply.html", c=load_config(STORE), menu=get_menu(), prediction=prediction
    )


@app.route(SmartReply.get_url() + "/settings", methods=["POST"])
@requires_auth()
def config_sr():
    with Store(STORE) as s:
        s["threshold"] = request.form.get("threshold")
        s["email"] = request.form.get("email").split(",")

    return redirect(url_for("smart_reply_panel"))


@app.route(SmartReply.get_url() + "/api/enable")
@requires_auth()
def enable_sr():
    with Store(STORE) as s:
        s["enabled"] = True
    return "OK"


@app.route(SmartReply.get_url() + "/api/disable")
@requires_auth()
def disable_sr():
    with Store(STORE) as s:
        s["enabled"] = False
    return "OK"


@app.route(SmartReply.get_url() + "/api/mock/enable")
@requires_auth()
def enable_sr_mock():
    with Store(STORE) as s:
        s["mock"] = True
    return "OK"


@app.route(SmartReply.get_url() + "/api/mock/disable")
@requires_auth()
def disable_sr_mock():
    with Store(STORE) as s:
        s["mock"] = False
    return "OK"
