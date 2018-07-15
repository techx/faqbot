from flask import Flask

app = Flask(__name__)

from flask import request

import faqbot.config as config

# All dem configs.
app.config["APP_NAME"] = config.APP_NAME

# Debug.
app.config["TEMPLATES_AUTO_RELOAD"] = True
app.config["DEBUG"] = config.DEBUG

# Regiser flask controllers.
import faqbot.web
