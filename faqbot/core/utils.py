"""Just some random helpers."""

from faqbot.core.store import load_config, save_config

def start_trigger(s, triggers):
    return any([s.startswith(t) for t in triggers])

def increment_mail_stat():
    store = load_config()
    
    if 'stats' in store:
        if 'total_mails' in store:
            store['stats']['total_mails'] += 1
        else:
            store['stats']['total_mails'] = 1
    else:
        store['stats'] = {
            'total_mails': 1
        }

    save_config(store)