import unittest
from app import create_app
from flask_testing import TestCase


class Test_Unittest(TestCase):
   def create_app(self):
     app = create_app('test')
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
   