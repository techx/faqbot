"""This defines the abstract faqbot feature
interface.
"""

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