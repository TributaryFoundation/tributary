from collections import namedtuple
import datetime
from unittest.mock import patch
import urllib.parse

from freezegun import freeze_time
from django.core import mail
from django.test import TestCase, Client
import stripe

from .models import Donation
from .verification import EmailTokenVerifier, InvalidTokenException, MAX_TOKEN_AGE, generate_token


class EmailVerificationTest(TestCase):
    @patch('stripe.Customer.create')
    def setUp(self, stripe_mock):
        self.email = 'donor@mail.com'
        self.good_token = generate_token(self.email)

        stripe_mock.return_value = stripe.Customer(id="mock-stripe-id")
        self.donation = Donation.objects.create_with_stripe_token('token', '', 'donor@mail.com', 1000, 100, '')

    def test_send_verification_email(self):
        with freeze_time('2016-01-01'):
            self.donation.send_verification_email('localhost')
            token = generate_token(self.email)
        self.assertEqual(len(mail.outbox), 1)
        email = mail.outbox[0]
        self.assertIn(self.donation.email_address, email.to)
        self.assertIn(urllib.parse.urlencode({'token':token}), email.body)

    def test_valid_token(self):
        resp = Client().get('/confirmed', {'token': self.good_token})
        self.assertEqual(resp.status_code, 200)

        donation = Donation.objects.get(email_address=self.email)
        self.assertTrue(donation.email_verified)

    def test_multiple_times(self):
        resp = Client().get('/confirmed', {'token': self.good_token})
        self.assertEqual(resp.status_code, 200)
        resp = Client().get('/confirmed', {'token': self.good_token})
        self.assertEqual(resp.status_code, 200)
        resp = Client().get('/confirmed', {'token': self.good_token})
        self.assertEqual(resp.status_code, 200)

        self.donation.refresh_from_db()
        self.assertTrue(self.donation.email_verified)

    def test_invalid_token(self):
        bad_token = self.good_token + 'junk'

        resp = Client().get('/confirmed', {'token': bad_token})
        self.assertEqual(resp.status_code, 404)

        self.donation.refresh_from_db()
        self.assertFalse(self.donation.email_verified)

    def test_expired_token(self):
        with freeze_time(datetime.datetime.now() - MAX_TOKEN_AGE - datetime.timedelta(days=1)):
            token = generate_token(self.email)

        resp = Client().get('/confirmed', {'token': token})
        self.assertEqual(resp.status_code, 404)

        self.donation.refresh_from_db()
        self.assertFalse(self.donation.email_verified)

    def test_no_such_email(self):
        token = generate_token("missing@email.com")

        resp = Client().get('/confirmed', {'token': token})
        self.assertEqual(resp.status_code, 404)

    def test_no_token_provided(self):
        resp = Client().get('/confirmed')
        self.assertEqual(resp.status_code, 404)


class VerificationTokenTest(TestCase):
    def setUp(self):
        key, salt = 'key', 'salt'
        self.verifier = EmailTokenVerifier(key, salt)

    def test_verify_email_invalid_token(self):
        bad_token = b"c3BlbmNlckB0cmlidXRhcnkuZm91bmRhdGlvbg==:MjAxNi0xMC0wMlQxOToyODo0Ny4wNTE3Mjc=:E9Ys7dUHzgt7dg9_puoJwN_Zr2k="
        self.assertIsNone(self.verifier.validate_token(bad_token))

    def test_verify_email_valid_token(self):

        '''Test that verify_email rejects tokens properly if they have the
        wrong email or an old timestamp.

        '''
        Testcase = namedtuple('Testcase', ['check_time', 'token_email', 'token_timestamp', 'returned'])

        cases = [
            Testcase(
                token_email='spencer@tributary.foundation',
                check_time=datetime.datetime(2016, 10, 30),
                token_timestamp=datetime.datetime(2016, 10, 30),
                returned='spencer@tributary.foundation',
            ),
            Testcase(
                token_email='rodrigo@tributary.foundation',
                check_time=datetime.datetime(2016, 10, 30),
                token_timestamp=datetime.datetime(2016, 10, 30),
                returned='rodrigo@tributary.foundation',
            ),
            Testcase(
                token_email='spencer@tributary.foundation',
                check_time=datetime.datetime(2016, 10, 30),
                token_timestamp=datetime.datetime(2016, 10, 30) - MAX_TOKEN_AGE + datetime.timedelta(seconds=1),
                returned='spencer@tributary.foundation',
            ),
            Testcase(
                token_email='spencer@tributary.foundation',
                check_time=datetime.datetime(2016, 10, 30),
                token_timestamp=datetime.datetime(2016, 10, 30) - MAX_TOKEN_AGE - datetime.timedelta(seconds=1),
                returned=None,
            ),

        ]
        for case in cases:
            with freeze_time(case.token_timestamp):
                token = self.verifier.generate_token(case.token_email)
            with freeze_time(case.check_time):
                have = self.verifier.validate_token(token)
            self.assertEqual(have, case.returned, case)

    def test_parse_token(self):
        Testcase = namedtuple('Testcase', ['token', 'valid', 'email', 'timestamp'])
        cases = [
            # Valid token:
            Testcase(
                token=b"c3BlbmNlckB0cmlidXRhcnkuZm91bmRhdGlvbg==:MjAxNi0xMC0wMlQxOToyNDoxMy40NDgwNzc=:E9Ys7dUHzgt7dg9_puoJwN_Zr2k=",
                valid=True,
                email='spencer@tributary.foundation',
                timestamp=datetime.datetime(2016, 10, 2, 19, 24, 13, 448077),
            ),
            # Valid string token:
            Testcase(
                token=u"c3BlbmNlckB0cmlidXRhcnkuZm91bmRhdGlvbg==:MjAxNi0xMC0wMlQxOToyNDoxMy40NDgwNzc=:E9Ys7dUHzgt7dg9_puoJwN_Zr2k=",
                valid=True,
                email='spencer@tributary.foundation',
                timestamp=datetime.datetime(2016, 10, 2, 19, 24, 13, 448077),
            ),
            # Empty token:
            Testcase(
                token=b'',
                valid=False,
                email='',
                timestamp=None,
            ),
            # Missing the signature:
            Testcase(
                token=b"c3BlbmNlckB0cmlidXRhcnkuZm91bmRhdGlvbg==:MjAxNi0xMC0wMlQxOToyNDoxMy40NDgwNzc=",
                valid=False,
                email='',
                timestamp=None,
            ),
            # Too many colons:
            Testcase(
                token=b"c3BlbmNlckB0cmlidXRhcnkuZm91bmRhdGlvbg==:MjAxNi0xMC0wMlQxOToyNDoxMy40NDgwNzc=:E9Ys7dUHzgt7dg9_puoJwN_Zr2k=:E9Ys7dUHzgt7dg9_puoJwN_Zr2k=",
                valid=False,
                email='',
                timestamp=None,
            ),
            # Signature off by one character:
            Testcase(
                token=b"c3BlbmNlckB0cmlidXRhcnkuZm91bmRhdGlvbg==:MjAxNi0xMC0wMlQxOToyNDoxMy40NDgwNzc=:E9Ys7dUHzgt7dg9_puoJwN_Zr2g=",
                valid=False,
                email='',
                timestamp=None,
            ),
            # Signature missing base64 padding:
            Testcase(
                token=b"c3BlbmNlckB0cmlidXRhcnkuZm91bmRhdGlvbg==:MjAxNi0xMC0wMlQxOToyNDoxMy40NDgwNzc=:E9Ys7dUHzgt7dg9_puoJwN_Zr2k",
                valid=False,
                email='',
                timestamp=None,
            ),
            # Valid signature, but changed timestamp:
            Testcase(
                token=b"c3BlbmNlckB0cmlidXRhcnkuZm91bmRhdGlvbg==:MjAxNi0xMC0wMlQxOToyODo0Ny4wNTE3Mjc=:E9Ys7dUHzgt7dg9_puoJwN_Zr2k=",
                valid=False,
                email='',
                timestamp=None,
            )
        ]
        for case in cases:
            if not case.valid:
                with self.assertRaises(InvalidTokenException):
                    self.verifier.parse_token(case.token)
            else:
                email, timestamp = self.verifier.parse_token(case.token)
                self.assertEqual(email, case.email)
                self.assertEqual(timestamp, case.timestamp)

    def test_email_codec(self):
        from .verification import _encode_email, _decode_email
        cases = (
            'spencer@tributary.foundation',
            'rodrigo@tributary.foundation',
            '电子邮件@tributary.foundation',
            '',
        )
        for email in cases:
            enc = _encode_email(email)
            dec = _decode_email(enc)
            self.assertEqual(dec, email)

    def test_timestamp_codec(self):
        from .verification import _encode_timestamp, _decode_timestamp
        cases = (
            datetime.datetime(2017, 1, 1, 12, 30, 0),
            datetime.datetime(1971, 1, 1, 12, 30, 0),
        )
        for ts in cases:
            enc = _encode_timestamp(ts)
            dec = _decode_timestamp(enc)
            self.assertEqual(dec, ts)

    def test_parse_invalid_timestamp(self):
        from .verification import _decode_timestamp
        with self.assertRaises(Exception):
            _decode_timestamp(b'MjAxNi0xMC0wMlQxODo0MjoyNC42NzUyNjy=')
