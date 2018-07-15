"""Just some random helpers."""

from faqbot.core.store import load_config, save_config


def start_trigger(s, triggers):
    return any([s.startswith(t) for t in triggers])


MENU = None


def get_menu():
    global MENU

    if MENU:
        return MENU

    MENU = load_config("menu")
    return MENU
