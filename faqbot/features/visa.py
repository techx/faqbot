"""Generates visa PDF letter and replies back,
attaching it!
"""

# Visa stuff
import os

if os.path.exists('faqbot/static/visa'):
    from weasyprint import default_url_fetcher, HTML
    from weasyprint.fonts import FontConfiguration
    from jinja2 import FileSystemLoader, Environment

    # Faqbot stuff
    from faqbot import app
    from faqbot.features.feature import Feature
    from faqbot.core.mailer import reply_email
    from faqbot.core.utils import get_menu
    from faqbot.web.auth import requires_auth

    from flask import request, render_template, redirect, url_for

    def render_from_template(directory, template_name, **kwargs):
        loader = FileSystemLoader(directory)
        env = Environment(loader=loader)
        template = env.get_template(template_name)
        return template.render(**kwargs)

    def custom_fetcher(url):
        if url.startswith('img:'):
            return dict(
                file_obj=open('faqbot/static/visa/' + url.split(':')[-1], 'rb'),
                mime_type='image/png'
            )
        else:
            return default_url_fetcher(url)

    def get_visa_pdf(firstname, lastname, country):
        html = render_from_template('faqbot/static/visa', 'visa.html',
            firstname=firstname,
            lastname=lastname,
            country=country
        )

        font_config = FontConfiguration()        
        h = HTML(string=html, url_fetcher=custom_fetcher)

        return h.write_pdf(font_config=font_config)

    class Visa(Feature):
        @staticmethod
        def triggered_callback(body, argv, reply_object):
            if len(argv) >= 5:
                if argv[1] == 'visa':
                    print "Processing visa request!"
                    firstame = argv[2]
                    lastname = argv[3]
                    country = argv[4]

                    reply = """Here is your visa letter!"""

                    visa_letter = get_visa_pdf(firstame, lastname, country)
                    reply_email(reply_object, reply, attach=visa_letter, attach_fn="visa_letter.pdf")

        @staticmethod
        def raw_callback(parsed, raw, reply_object):
            pass

        @staticmethod
        def get_name():
            return "Visa"

        @staticmethod
        def get_url():
            return "/visa"

    # Web control panel render.
    @app.route(Visa.get_url())
    @requires_auth()
    def visa_panel():
        return render_template("visa.html", menu=get_menu())