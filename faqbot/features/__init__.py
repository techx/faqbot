"""The features module contains all of faqbot's
features such as templating and quill interface.

This provides a nice interface to add new email features.

Adding a new feature requires updating the following files:

    core.callbacks
        You need to register your feature's callback.

    core.defaults
        You need to add default configuration for your
        feature.

    features.__init__
        You need to import it if you're creating defaults
        and such from your class.

Additionally, each feature can implement its own flask
routes to render templates that change the config.
"""

import faqbot.features.stats
import faqbot.features.templates

ABSTRACT_ERROR = "Abstract method not implemented."

class Feature(object):
    @staticmethod
    def triggered_callback(body, argv, reply_object):
        """ See callbacks.py
        """

        raise NotImplementedError(ABSTRACT_ERROR)
    
    @staticmethod
    def raw_callback(parsed, raw, reply_object):
        """ See callbacks.py
        """

        raise NotImplementedError(ABSTRACT_ERROR)

    @staticmethod
    def get_name():
        """ Gets the name of this feature to be shown
        in the the menu on the left.
        """

        raise NotImplementedError(ABSTRACT_ERROR)

    @staticmethod
    def get_url():
        """ Gets the url of the feature's main page.
        Example: /stats
        """

        raise NotImplementedError(ABSTRACT_ERROR)