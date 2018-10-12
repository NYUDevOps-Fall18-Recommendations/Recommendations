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