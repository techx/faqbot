import pickle

def save_commands(COMMANDS):
    pickle.dump(COMMANDS, open('faq.pkl', 'w'))

def load_commands():
    return pickle.load(open('faq.pkl'))

def pickle_faq():
    from faq import COMMANDS
    pickle.dump(COMMANDS, open('faq.pkl', 'w'))