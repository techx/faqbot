## FAQ Bot

A bot that replies with predefined templates to FAQ emails.

### Usage

For now, reply-one to any email to `admin@hackmit.org` with the body text:

```
@faqbot edu
```

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