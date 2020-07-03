
#import sys
#sys.path.insert(0,r'/eWave')
from app import *
import unittest
import requests
import logging
from flask import jsonify
import json
import time

  
login_data = {
    "userId": 1,
    "login": "Murilo",
    "password": 123,
    "email": "efgs96@gmail.com",
    "confirmed": True,
    "adminconfirmed": False
}
#auth_token= 'numbers'

import ast



class TestHomeView(unittest.TestCase):
    def setUp(self):
        get_points = ['api/v1/products','/api/v1/orders']
        for i in get_points:
            self.get = requests.get('http://127.0.0.1:5000/{}'.format(i))

        login_url = 'http://127.0.0.1:5000/api/v1/login'
        self.post = requests.post(login_url, data=login_data)
        transform = []
        transform.append(self.post.text)
        for x in transform:
            x = ast.literal_eval(x)
            token_a = x
        if "access_token" in token_a:
            self.auth_token = token_a["access_token"]
        

        #self.auth_token = self.post.text
        

    def test_get(self):
        self.assertEqual(200, self.get.status_code) 
    

    def test_post(self):
        self.assertEqual(200, self.post.status_code)
        self.assertIn("access_token", self.post.text)
        
        
        

    def test_logout(self):
        hed = {'Authorization': 'Bearer ' + self.auth_token}
        logout_url = 'http://127.0.0.1:5000/api/v1/logout'
        self.logout = requests.post(logout_url,headers=hed, data=login_data)    
        self.assertEqual(200, self.logout.status_code)
        self.assertIn("Logged out", self.logout.text)
 
        

        

'''
api.add_resource(Products, '/api/v1/products')
api.add_resource(Product, '/api/v1/products/<string:productId>')
api.add_resource(User, '/api/v1/users/<int:userId>')
api.add_resource(UserRegister, '/api/v1/register')
api.add_resource(UserLogin, '/api/v1/login')
api.add_resource(UserLogout, '/api/v1/logout')
api.add_resource(UserConfirmed, '/api/v1/confirm/<int:userId>')
api.add_resource(AdminConfirm, '/api/v1/admin/<int:userId>')
api.add_resource(PriceCheck, '/api/v1/price')
api.add_resource(Order, '/api/v1/orders/<int:orderId>')
api.add_resource(Orders, '/api/v1/orders')
api.add_resource(NewOrder, '/api/v1/buy')
'''
