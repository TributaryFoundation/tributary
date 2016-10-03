from collections import namedtuple
import datetime

from freezegun import freeze_time

from django.test import TestCase

from .verification import EmailTokenVerifier, InvalidTokenException, MAX_TOKEN_AGE


class VerificationTokenTest(TestCase):
    def setUp(self):
        key, salt = 'key', 'salt'
        self.verifier = EmailTokenVerifier(key, salt)

    def test_verify_email_invalid_token(self):
        bad_token = b"c3BlbmNlckB0cmlidXRhcnkuZm91bmRhdGlvbg==:MjAxNi0xMC0wMlQxOToyODo0Ny4wNTE3Mjc=:E9Ys7dUHzgt7dg9_puoJwN_Zr2k="
        self.assertFalse(self.verifier.verify_email('spencer@tributary.foundation', bad_token))

    def test_verify_email_valid_token(self):
        '''Test that verify_email rejects tokens properly if they have the
        wrong email or an old timestamp.

        '''
        Testcase = namedtuple('Testcase', ['email', 'check_time', 'token_email', 'token_timestamp', 'valid'])

        cases = [
            Testcase(
                email='spencer@tributary.foundation',
                token_email='spencer@tributary.foundation',
                check_time=datetime.datetime(2016, 10, 2),
                token_timestamp=datetime.datetime(2016, 10, 2),
                valid=True,
            ),
            Testcase(
                email='spencer@tributary.foundation',
                token_email='rodrigo@tributary.foundation',
                check_time=datetime.datetime(2016, 10, 2),
                token_timestamp=datetime.datetime(2016, 10, 2),
                valid=False,
            ),
            Testcase(
                email='spencer@tributary.foundation',
                token_email='spencer@tributary.foundation',
                check_time=datetime.datetime(2016, 10, 1),
                token_timestamp=datetime.datetime(2016, 10, 2) - MAX_TOKEN_AGE + datetime.timedelta(seconds=1),
                valid=True,
            ),
            Testcase(
                email='spencer@tributary.foundation',
                token_email='spencer@tributary.foundation',
                check_time=datetime.datetime(2016, 10, 2),
                token_timestamp=datetime.datetime(2016, 10, 2) - MAX_TOKEN_AGE - datetime.timedelta(seconds=1),
                valid=False,
            ),

        ]
        for case in cases:
            with freeze_time(case.token_timestamp):
                token = self.verifier.generate_token(case.token_email)
            with freeze_time(case.check_time):
                have = self.verifier.verify_email(case.email, token)
            self.assertEqual(have, case.valid, case)

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
