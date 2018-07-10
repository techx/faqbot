"""This contains all the faqbot callbacks from
the jank email parsing script.

In all functions below, the :reply_object refers
to an object that can be used to reply-all back
to the thread using the `reply_email` function.
"""

from faqbot.core.utils import increment_mail_stat

def triggered_email(body, argv, reply_object):
    """This routine gets triggered when an @faqbot
    body message is sent. It is more accurate that
    an action is needed on this context.

    :body is the parsed body, should start off 
    with the @faqbot ... as a string.

    :argv is the splitted arguments, where
    argv[0] is the trigger.

    """

    # Let's first update our statistic.
    increment_mail_stat()
    
    print argv

def raw_email(parsed, raw, reply_object):
    """If no trigger is found, this routine is fired.
    Be cautious, this may be a false positive.

    The use of this method is to implement confident
    auto replies, without triggering faqbot.
    """
    pass