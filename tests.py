import unittest

from app import app


class TestAppRouting(unittest.TestCase):
    def setUp(self):
        self.app_client = app.test_client()

    def test_index(self):
        response = self.app_client.get('/')
        self.assertEqual(response.status_code, 200)

        body = response.get_data(as_text=True)
        self.assertIn("Tributary", body)


if __name__ == '__main__':
    unittest.main()
