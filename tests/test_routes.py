import unittest
from app import create_app, db
from app.models import User, BlogPost
from flask_jwt_extended import create_access_token

class APITestCase(unittest.TestCase):
    def setUp(self):
        self.app = create_app()
        self.app.config['TESTING'] = True
        self.app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
        self.client = self.app.test_client()
        with self.app.app_context():
            db.create_all()

    def tearDown(self):
        with self.app.app_context():
            db.session.remove()
            db.drop_all()

    def test_signup(self):
        response = self.client.post('/signup', json={
            'username': 'testuser',
            'email': 'test@example.com',
            'password': 'password'
        })
        self.assertEqual(response.status_code, 201)

    def test_signin(self):
        self.client.post('/signup', json={
            'username': 'testuser',
            'email': 'test@example.com',
            'password': 'password'
        })
        response = self.client.post('/signin', json={
            'username': 'testuser',
            'password': 'password'
        })
        self.assertEqual(response.status_code, 200)

    def test_create_post(self):
        self.client.post('/signup', json={
            'username': 'testuser',
            'email': 'test@example.com',
            'password': 'password'
        })
        response = self.client.post('/signin', json={
            'username': 'testuser',
            'password': 'password'
        })
        token = response.get_json()['token']
        response = self.client.post('/posts', json={
            'title': 'New Post',
            'body': 'This is a new post.'
        }, headers={'Authorization': f'Bearer {token}'})
        self.assertEqual(response.status_code, 201)

if __name__ == '__main__':
    unittest.main()
