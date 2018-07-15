import pickle
from faq import COMMANDS


def save_commands(COMMANDS):
    pickle.dump(COMMANDS, open("faq.pkl", "w"))


def load_commands():
    return pickle.load(open("faq.pkl"))


def pickle_faq():
    pickle.dump(COMMANDS, open("faq.pkl", "w"))
