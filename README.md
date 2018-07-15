# FAQ Bot

A bot to manage emails that ask frequenty asked questions.

## How To Use

### Basic Usage

Reply all to the email thread without the person who sent the email. Or reply-one to `admin@hackmit.org` with the body text:

```
@faqbot edu
```

This will reply to the person a generic response to "I don't have an educational email"

You can also use the `@fb` trigger for shorthand.

### Quill

```
@faqbot whitelist <email>
```

This will whitelist the given email in quill and reply to the person.

### Smart Reply

Now that we've had enough faqbot usage, faqbot has started to learn emails > template mapping and will attempt to automatically reply to an email if it's confident enough.

### Management

Head over to faqbot.hackmit.org to view the control panel. There you can enable / disable features, tweak settings and add new templates.


## Development

### Setup

Resolve dependencies,

```bash
pip install -r requirements.txt
```

You need to place the `config.py` file which looks like,

```python
"""Main configuration file. Can either pull from the
environment or from this file.
"""

import os

'''
===== WEB SPECIFIC =====
'''

# What's this app called?
APP_NAME = os.environ.get('APP_NAME', "faqbot")

# App network port.
PORT = os.environ.get('PORT', 8114)

# Is the app running in debug mode?
DEBUG = bool(os.environ.get('DEBUG', False))

# Secret for JWTs.
SECRET = os.environ.get('SECRET', "CHANGE THIS")

# Admin password.
ADMIN_PASSWORD = os.environ.get('ADMIN_PASSWORD', "P9Jt_B=uMvgu6#EG")

'''
===== MAIL SPECIFIC =====
'''

# IMAP server details.
IMAP_SERVER = "imap.gmail.com"
SMTP_SERVER = "smtp.gmail.com"
MAIL_USER = "admin@hackmit.org"
MAIL_PASSWORD = "CHANGE THIS"

# SMTP server details.
SEND_MAIL_USER = MAIL_USER
SEND_MAIL_PASSWORD = MAIL_PASSWORD
MAIL_FROM = "team@hackmit.org"

# This footer is appended at the end of _every_ email
# sent by this bot. Just to make sure people can reach
# out again if they want to.
FOOTER = """
<br><br> <i>~~ This was an automated message, please <a href="mailto:team@hackmit.org">email us</a> again if this didn't help! ~~</i>
"""

TRIGGERS = ["@faqbot", "@fb"]
```

### Running

To run for local debugging,

```bash
python app.py
```

To run on production,

```bash
python run.py
```

### Writing Code

faqbot's codebase is designed to be hackable. The main directory to add a new feature is the `faqbot/features/` directory. Here you can register for email callbacks and use the faqbot API to send reply-all or reply-one messages based on the email you just received.

Adding new features is extensively documented in the [`features` module](faqbot/features/__init__.py). You can also take a look at the [quill feature](faqbot/features/quill.py) as an example feature to off of.

### Contributing

Try to follow PEP8 for everything oustide of `legacy/`. Contribute by opening pull requests and report bugs by creating issues. Email parsing in general is nasty so opening bugs for parsing errors will be really helpful.

## Security

As of now, the bot is secure as long as the spec doesn't leak. If it leaks, we can easily trace the attack. tldr; keep the spec safe, but not a big deal if it leaks.

Adding a whitelist of people who can use triggered faqbot is a big TODO that is in the works.