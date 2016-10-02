import os

from .base import *

DEBUG = False

ALLOWED_HOSTS = ['tributary.foundation', 'www.tributary.foundation']

EMAIL_BACKEND = 'anymail.backends.mailgun.MailgunBackend'
