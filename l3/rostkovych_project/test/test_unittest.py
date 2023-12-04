import unittest
from app import create_app, db
from flask_testing import TestCase
from app.auth.models import User
from flask_login import current_user, login_user
from app.todo.templates.models import Tasks

class Test_Unittest(TestCase):
   def setUp(self): 
      db.create_all() 
      user = User(username='user', email='user@gmail.com', password='password') 
      t = Tasks(title='title', description='Test description') 
      db.session.add_all([user, t]) 
      db.session.commit()
   def tearDown(self):
        db.session.remove()
        db.drop_all()
   def create_app(self):
     app = create_app('test')
     app.config['WTF_CSRF_ENABLED'] = False
     return app

   def test_setup(self): 
      self.assertTrue(self.app is not None) 
      self.assertTrue(self.client is not None) 
      self.assertTrue(self._ctx is not None)
   def test_server(self): 
     url = 'http://localhost:5000/'
     response = self.client.get(url)
     self.assertEqual(response.status_code, 200)

   def test_home_page_loads(self): 
     """Test HomePage view test"""
     with self.client: response = self.client.get('/') 
     self.assertEqual(response.status_code, 200)
     self.assertIn(b'Sofiia', response.data)
   def test_skills_page_loads(self): 
     """Test SkillsPage view test"""
     with self.client: response = self.client.get('/skills') 
     self.assertEqual(response.status_code, 200)
     self.assertIn(b'Soft Skills', response.data)
   def test_education_page_loads(self): 
     """Test EducationPage view test"""
     with self.client: response = self.client.get('/education') 
     self.assertEqual(response.status_code, 200)
     self.assertIn(b'Vasyl Stefanyk', response.data)
   def test_login_page_loads(self): 
     """Test LoginPage view test"""
     with self.client: response = self.client.get('/login') 
     self.assertEqual(response.status_code, 200)
     self.assertIn(b'remember', response.data)
   def test_register_page_loads(self): 
     """Test RegisterPage view test"""
     with self.client: response = self.client.get('/register') 
     self.assertEqual(response.status_code, 200)
     self.assertIn(b'confirm_password', response.data)
   def test_login(self):
        """Test logging in registered user"""
        with self.client:
            response = self.client.post(
                '/login',
                data=dict(name="user", password="password", remember=True),
                follow_redirects=True
            )
            assert response.status_code == 200
            assert response.request.path == '/account'
            self.assertIn(b'About Me', response.data)
            self.assertTrue(current_user.username == "user")
            self.assertTrue(current_user.is_active())
   def test_logout(self):
        """Test logging out """
        with self.client:
            response = self.client.post('/logout',   follow_redirects=True)
            assert response.status_code == 200
            assert response.request.path == '/login'
            self.assertIn(b'Log In', response.data)
            self.assertFalse(current_user.is_authenticated)

   def test_register(self): 
     """Test registering new user"""
     with self.client: 
      response = self.client.post( '/register', data=dict(name='test', email='test@test.com', password='password', confirm_password='password'), follow_redirects=True ) 
     user = User.query.filter_by(email='test@test.com').first() 
     self.assertIsNotNone(user)

   def test_account(self): 
     """Test updating the account info"""
     user = User.query.filter_by(email='user@gmail.com').first() 
     login_user(user)     
     with self.client: 
      response = self.client.post( '/account', data=dict(new_name='test', new_email='test@test.com', about='!!!!'), follow_redirects=True ) 
     self.assertTrue(user.username=="test")
     self.assertTrue(user.email=="test@test.com")
     self.assertTrue(user.about=="!!!!")

   def test_todo_page_loads(self): 
     """Test Tasks view test"""
     with self.client: response = self.client.get('/tasks') 
     self.assertEqual(response.status_code, 200)
     self.assertIn(b'Actions', response.data)

   def test_todo_new(self): 
     """Test creating new task"""
     with self.client: 
        response = self.client.post('/tasks', data=dict(text="test",description="new" ), follow_redirects=True) 
     self.assertEqual(response.status_code, 200)
     t1 = Tasks.query.filter_by(title="test").first()
     self.assertTrue(t1.description=="new")

   def test_todo_update(self): 
     """Test updating status of a task"""
     with self.client: 
        response = self.client.get('/tasks/update/1', follow_redirects=True) 
     t1 = Tasks.query.filter_by(id=1).first()
     print(t1.complete)
     self.assertEqual(response.status_code, 200)
     self.assertTrue(t1.complete==True)
     with self.client: 
        response = self.client.get('/tasks/update/1', follow_redirects=True) 
     self.assertEqual(response.status_code, 200)
     self.assertTrue(t1.complete==False)

   def test_todo_delete(self): 
     """Test deleting a task"""
     with self.client: 
        response = self.client.get('/tasks/delete/1', follow_redirects=True) 
     t1 = Tasks.query.filter_by(id=1).first()
     self.assertEqual(response.status_code, 200)
     self.assertEqual(t1,None)