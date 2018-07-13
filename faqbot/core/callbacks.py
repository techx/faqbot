"""This contains all the faqbot callbacks from
the jank email parsing script.

In all functions below, the :reply_object refers
to an object that can be used to reply-all back
to the thread using the `reply_email` function.
"""

from faqbot.features import FEATURES
from faqbot.features.stats import Stats
from faqbot.features.templates import Templates

def triggered_email(body, argv, reply_object):
    """This routine gets triggered when an @faqbot
    body message is sent. It is more accurate that
    an action is needed on this context.

    :body is the parsed body, should start off 
    with the @faqbot ... as a string.

    :argv is the splitted arguments, where
    argv[0] is the trigger.

    """

    # TODO Maybe implement some sort of auth
    # only for triggered messages. We only 
    # want people from our team doing this.

    for f in FEATURES:
        f.triggered_callback(body, argv, reply_object)

def raw_email(parsed, raw, reply_object):
    """If no trigger is found, this routine is fired.
    Be cautious, this may be a false positive.

    The use of this method is to implement confident
    auto replies, without triggering faqbot.
    """
    pass