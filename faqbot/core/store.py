"""Manages persisting data onto disk, things like
templates and dynamic configuration details.
"""

from faqbot.legacy.faq import COMMANDS
from faqbot.core.defaults import DEFAULTS

import pickle
import copy
import os

STORE_FILE = 'store.p'

def save_config(store):
    pickle.dump(store, open(STORE_FILE, 'w'))

def load_config():
    return pickle.load(open(STORE_FILE))

def gen_defaults():
    if not os.path.exists(STORE_FILE):
        store = copy.deepcopy(DEFAULTS)

        # Load these from legacy.
        store['templates'] = copy.deepcopy(COMMANDS)

        save_config(store)

# Always try and generate defaults.
gen_defaults()