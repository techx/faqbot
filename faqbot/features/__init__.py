"""The features module contains all of faqbot's
features such as templating and quill interface.

This provides a nice interface to add new email features.

Adding a new feature requires updating the following files:

    core.callbacks
        You need to register your feature's callback.

    core.defaults
        You need to add default configuration for your
        feature.

Additionally, each feature can implement its own flask
routes to render templates that change the config.
"""