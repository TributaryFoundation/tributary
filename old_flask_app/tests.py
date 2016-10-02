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

    def test_info_received(self):
        response = self.app_client.get('/received')
        self.assertEqual(response.status_code, 200)
        response.close()

    def test_static_assets(self):
        response = self.app_client.get('/static/css/style.css')
        self.assertEqual(response.status_code, 200)
        response.close()


if __name__ == '__main__':
    unittest.main()
