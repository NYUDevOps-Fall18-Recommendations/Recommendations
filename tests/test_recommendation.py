"""
Recommendation Test Suite
Test cases can be run with the following:
nosetests -v --with-spec --spec-color
"""

import os
import json
import unittest
from models import Recommendation, DataValidationError

######################################################################
#  T E S T   C A S E S
######################################################################
class TestRecommendations(unittest.TestCase):
	""" Test Cases for Recommendation Model """

	def setUp(self):
		# Recommendation.init_db()
		Recommendation.remove_all()

	def test_delete_a_recommendation(self): 
		recommendation = Recommendation(0, "name", "recommended", "category")
		recommendation.save()
		self.assertEqual(len(Recommendation.all()), 1)
		recommendation.delete()
		self.assertEqual(len(Recommendation.all()), 0)
