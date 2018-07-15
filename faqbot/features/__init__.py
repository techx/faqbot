"""The features module contains all of faqbot's
features such as templating and quill interface.

This provides a nice interface to add new email features.

Adding a new feature requires updating the following file:

    features.__init__
        You need to import it if you're creating defaults
        and such from your class.

Additionally, each feature can implement its own flask
routes to render templates that change the config.

Follow the quill.py feature to get a sense of how things
work.
"""

import faqbot.features.stats
import faqbot.features.templates
import faqbot.features.quill
import faqbot.features.smartreply

FEATURES = [
    stats.Stats,
    templates.Templates,
    quill.Quill,
    smartreply.SmartReply
]

def dump_menu():
    from faqbot.core.store import save_config

    menu = []

    for feature in FEATURES:
        menu.append({
            'name': feature.get_name(),
            'url': feature.get_url()
        })

    save_config(menu, "menu")

dump_menu()