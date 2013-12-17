from app import app

app.config['WTF_CSRF_ENABLED'] = False

import unittest


class CloudTestAppCase(unittest.TestCase):

    def setUp(self):
        app.redis.rpush('clouds', 'Altocumulus')
        app.redis.rpush('clouds', 'Altostratus')
        app.redis.rpush('clouds', 'Cumulonimbus')
        app.redis.rpush('clouds', 'Nimbostratus')
        # app.debug = True

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


class CloudTestAddCloudCase(unittest.TestCase):

    def tearDown(self):
        app.redis.flushdb()

    def test_add_cloud(self):
        # print dir(app.config)
        tester = app.test_client(self)
        tester.WTF_CSRF_ENABLED = False

        response = tester.get('/add', content_type='application/html')

        assert 'This field is required.' not in response.data
        assert 'New cloud' in response.data

        response = tester.post(
            '/add',
            content_type='application/html',
            data=dict()
        )

        assert 'This field is required.' in response.data
        assert 'New cloud' in response.data

        response = tester.post(
            '/add',
            data=dict(
                classification="my_special_test_cloud"
            ))

        # print dir(response), response.status_code, dir(response.response)
        db_result = app.redis.lrange("clouds", 0, -1)

        assert "my_special_test_cloud" in db_result
        assert "http://localhost/" == response.location

if __name__ == '__main__':
    unittest.main()
