import base64
import datetime

import dateutil.parser

from django.conf import settings
from django.utils.crypto import salted_hmac


# MAX_TOKEN_AGE is the maximum age of an email verification token for
# it to still be considered valid.
MAX_TOKEN_AGE = datetime.timedelta(days=14)


class InvalidTokenException(Exception):
    pass


class EmailTokenVerifier(object):
    def __init__(self, key=None, salt=None):
        '''Create a new EmailTokenVerifier using the specified key and
        salt. By default, the app's SECRET_KEY and EMAIL_TOKEN_SALT
        from settings are used.

        '''
        if key is None:
            key = settings.SECRET_KEY
        if salt is None:
            salt = settings.EMAIL_TOKEN_SALT

        self._key = key
        self._salt = salt

    def verify_email(self, email, token):
        '''Returns True if the token validates the given email, else returns
        False.

        '''
        try:
            token_email, token_timestamp = self.parse_token(token)
        except InvalidTokenException:
            return False

        if token_email != email:
            return False

        if token_timestamp < (datetime.datetime.now() - MAX_TOKEN_AGE):
            return False

        return True

    def parse_token(self, token):
        '''Checks the signature of a token. If it's invalid, raises an
        InvalidTokenException. Otherwise, returns the email address and
        timestamp encoded in the token.

        '''
        if isinstance(token, str):
            token = token.encode()
        parts = token.split(b":")
        if len(parts) != 3:
            raise InvalidTokenException("token has invalid format")

        encoded_email, encoded_timestamp, have_sig = parts

        have_sig = parts[2]
        want_sig = self._sign(encoded_email, encoded_timestamp)
        if have_sig != want_sig:
            raise InvalidTokenException("token signature is invalid")

        try:
            email = _decode_email(encoded_email)
        except:
            raise InvalidTokenException("token email is invalid")

        try:
            timestamp = _decode_timestamp(encoded_timestamp)
        except:
            raise InvalidTokenException("token timestamp is invalid")

        return email, timestamp

    def generate_token(self, email_address):
        '''Given an email address, generates a utf8-encoded verification token.

        The token is of the form email:timestamp:signature. Email and
        timestamp are base-64 encoded.

        The signature is the base64-encoded HMAC of the base-64 encoded
        email:timestamp string. The project's SECRET_KEY, salted with
        EMAIL_TOKEN_SALT, is used as the key for the HMAC.

        '''
        b64_email = _encode_email(email_address)

        now = datetime.datetime.now()
        b64_timestamp = _encode_timestamp(now)

        b64_sig = self._sign(b64_email, b64_timestamp)

        parts = (b64_email, b64_timestamp, b64_sig)
        token =  b':'.join(parts)

        return token.decode('utf-8')

    def _sign(self, b64_email, b64_timestamp):
        '''Given a base64-encoded email and timestamp, return the
        base64-encoded HMAC signature for an email verification token.

        '''
        val = b64_email + b':' + b64_timestamp
        sig = salted_hmac(self._salt, val, self._key)
        return base64.urlsafe_b64encode(sig.digest())


def _encode_email(email_address):
    return base64.urlsafe_b64encode(email_address.encode())


def _decode_email(encoded_email):
    return base64.urlsafe_b64decode(encoded_email).decode('utf-8')


def _encode_timestamp(timestamp):
    return base64.urlsafe_b64encode(timestamp.isoformat().encode())


def _decode_timestamp(encoded_timestamp):
    timestamp_string = base64.urlsafe_b64decode(encoded_timestamp).decode('utf-8')
    return dateutil.parser.parse(timestamp_string)
