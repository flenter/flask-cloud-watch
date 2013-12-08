from app import app

import unittest


class CloudTestCase(unittest.TestCase):

    def setUp(self):
        app.redis.rpush('clouds', 'Altocumulus')
        app.redis.rpush('clouds', 'Altostratus')
        app.redis.rpush('clouds', 'Cumulonimbus')
        app.redis.rpush('clouds', 'Nimbostratus')

    def tearDown(self):
        app.redis.flushdb()

    def test_clouds(self):
        tester = app.test_client(self)

        response = tester.get('/', content_type='application/html')

        self.assertEqual(response.status_code, 200)
        self.assertIn(
            'Altocumulus', response.data, "Altocumulus was not found in the \
html")
        self.assertIn(
            'Altostratus', response.data, "Altostratus was not found in the \
html")
        self.assertIn(
            'Cumulonimbus', response.data, "Cumulonimbus was not found in the \
html")
        self.assertIn(
            'Nimbostratus', response.data, "Nimbostratus was not found in the \
html")

if __name__ == '__main__':
    unittest.main()
