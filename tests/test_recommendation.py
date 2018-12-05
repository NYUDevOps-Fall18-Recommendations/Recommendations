"""
Recommendation Test Suite
Test cases can be run with the following:
nosetests -v --with-spec --spec-color
"""

import os
import json
import logging
import unittest
from time import sleep # use for rate limiting Cloudant Lite :(
from service.models import Recommendation, DataValidationError

######################################################################
#  T E S T   C A S E S
######################################################################
class TestRecommendations(unittest.TestCase):
	""" Test Cases for Recommendation Model """
	logger = logging.getLogger(__name__)

	def setUp(self):
		# sleep(0.5)
		Recommendation.init_db()
		# sleep(0.5)
		Recommendation.remove_all()
		# sleep(0.5)

	def test_create_a_recommendation(self): 
		recommendation = Recommendation("productId", "suggestionId", "categoryId")
		self.assertNotEqual(recommendation, None)
		self.assertEqual(recommendation.id, None)
		self.assertEqual(recommendation.productId, "productId")
		self.assertEqual(recommendation.suggestionId, "suggestionId")
		self.assertEqual(recommendation.categoryId, "categoryId")

	def test_delete_a_recommendation(self): 
		recommendation = Recommendation("productId", "recommended", "categoryId")
		recommendation.save()
		self.assertEqual(len(Recommendation.all()), 1)
		recommendation.delete()
		self.assertEqual(len(Recommendation.all()), 0)

	def test_serialize_a_recommendation(self):
		recommendation = Recommendation("iPhone", "Pixel", "Digital Prodct")
		data = recommendation.serialize()
		self.assertNotEqual(data, None)
		self.assertNotIn('_id', data)
		self.assertEqual(data['productId'], "iPhone")
		self.assertEqual(data['suggestionId'], "Pixel")
		self.assertEqual(data['categoryId'], "Digital Prodct")

	def test_deserialize_a_recommendation(self):
		data = {"productId": "iPhone", "suggestionId": "Pixel", "categoryId": "Digital Prodct"}
		recommendation = Recommendation()
		recommendation.deserialize(data)
		self.assertNotEqual(recommendation, None)
		self.assertEqual(recommendation.id, None) 
		self.assertEqual(recommendation.productId, "iPhone")
		self.assertEqual(recommendation.suggestionId, "Pixel")
		self.assertEqual(recommendation.categoryId, "Digital Prodct")

	def test_deserialize_with_no_productId(self):
		recommendation = Recommendation()
		data = {"suggestionId": "Pixel", "categoryId": "Digital Prodct"}
		self.assertRaises(DataValidationError, recommendation.deserialize, data)

	def test_deserialize_with_no_data(self):
		recommendation = Recommendation(0)
		self.assertRaises(DataValidationError, recommendation.deserialize, None)

	def test_deserialize_with_bad_data(self):
		recommendation = Recommendation(0)
		self.assertRaises(DataValidationError, recommendation.deserialize, "string data")

	def test_find_a_recommendation(self):
		saved_recommendation = Recommendation("productId", "recommended", "categoryId")
		saved_recommendation.save()
		recommendation = Recommendation.find(saved_recommendation.id)
		self.assertEqual(recommendation.productId, "productId")
		self.assertIsNot(recommendation, None)
		self.assertEqual(recommendation.id, saved_recommendation.id)
		self.assertEqual(recommendation.productId, "productId")

	def test_update_a_recommendation(self):
		recommendation = Recommendation("productId", "recommended", "categoryId")
		recommendation.save()

		recommendation.categoryId = "newcategoryId"
		recommendation.save()
		recommendations = Recommendation.all()
		self.assertEqual(recommendations[0].categoryId, "newcategoryId")

	def test_find_by_categoryId(self): 
		Recommendation("productId1", "recommended1", "categoryId1").save()
		Recommendation("productId2", "recommended2", "categoryId2").save()
		recommendations = Recommendation.find_by_categoryId("categoryId1")
		self.assertEqual(len(recommendations), 1)
		self.assertEqual(recommendations[0].categoryId, "categoryId1")

	def test_find_by_suggestionId(self): 
		Recommendation("productId1", "suggestionId1", "categoryId1").save()
		Recommendation("productId2", "suggestionId2", "categoryId2").save()
		recommendations = Recommendation.find_by_suggestionId("suggestionId1")
		self.assertEqual(len(recommendations), 1)
		self.assertEqual(recommendations[0].suggestionId, "suggestionId1")

######################################################################
#   M A I N
######################################################################
if __name__ == '__main__':
    unittest.main()
