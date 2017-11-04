## FAQ Bot

A bot that replies with predefined templates to FAQ emails.

### Usage

For now, reply-one to any email to `admin@hackmit.org` with the body text:

[Full List of Commands](https://github.com/techx/faq-bot/blob/master/faq.py)

```
@faqbot edu
```

This will reply to the person a generic response to "I don't have an educational email"

```
@faqbot whitelist [email]
```

This will whitelist the given email in quill and reply to the person.

```
@faqbot mixed
```

This will reply to the person a generic response to "What if I have both MIT and other people in my team?"



### Config

The `config.py` template:

```python
IMAP_SERVER = "imap.gmail.com"
SMTP_SERVER = "smtp.gmail.com"
MAIL_USER = ""
MAIL_PASSWORD = ""
TRIGGER = "@faqbot"

SEND_MAIL_USER = MAIL_USER
SEND_MAIL_PASSWORD = MAIL_PASSWORD
MAIL_FROM = "team@hackmit.org"

# Quill stuff
ENDPOINT = "https://my.hackmit.org/api/settings/whitelist"
ACCESS_TOKEN = "" # JWT from quill admin

# Admin password
ADMIN_PASSWORD = ''

# Footer
FOOTER = """
<br><br> <i>This is a cute footer.</i>
"""
```

For HackMIT grab it from the TechX Google Drive

### Development

Resolve dependencies,

```bash
pip install -r requirements.txt
```

To run for local debugging,

```bash
python bot.py
```

To run on production,

```bash
python run.py
```

### Security

As of now, the bot is secure as long as the spec doesn't leak. If it leaks, we can easily trace the attack. tldr; keep the spec safe, but not a big deal if it leaks.