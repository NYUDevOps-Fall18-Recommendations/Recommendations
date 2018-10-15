"""
Pet API Service Test Suite
Test cases can be run with the following:
nosetests
"""

import unittest
import logging
import json
import os
from mock import MagicMock, patch
from flask_api import status    # HTTP Status Codes
from models import Recommendation, DataValidationError
import server

# Status Codes
HTTP_200_OK = 200
HTTP_201_CREATED = 201
HTTP_204_NO_CONTENT = 204
HTTP_400_BAD_REQUEST = 400
HTTP_404_NOT_FOUND = 404
HTTP_405_METHOD_NOT_ALLOWED = 405
HTTP_409_CONFLICT = 409

######################################################################
#  T E S T   C A S E S
######################################################################
class TestRecommendationServer(unittest.TestCase):
	""" Recommendation Service tests """

	def setUp(self):
		"""Runs before each test"""
		self.app = server.app.test_client()
		Recommendation(id=1, name='Infinity Gauntlet', suggestion='Soul Stone', category='Comics').save()
		Recommendation(id=2, name='iPhone', suggestion='iphone Case', category='Electronics').save()


	def tearDown(self):
		"""Runs towards the end of each test"""
		Recommendation.remove_all()

	def test_create_recommendation(self):
		""" Create a new recommendation """
		new_recommenation = dict(id=9999, name='Table', suggestion='Chair', category='Home Appliances')
		data = json.dumps(new_recommenation)
		resp = self.app.post('/recommendation', data=data, content_type='application/json')
		self.assertEqual(resp.status_code, status.HTTP_201_CREATED)
		# Make sure location header is set
        #location = resp.headers.get('Location', None)
        #self.assertTrue(location != None)
        # Check the data is correct
        #new_json = json.loads(resp.data)
        #self.assertEqual(new_json['name'], 'Table')
