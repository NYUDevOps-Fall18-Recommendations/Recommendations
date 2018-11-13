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

	def test_create_a_recommendation(self): 
		recommendation = Recommendation(0, "productId", "suggestionId", "categoryId")
		self.assertNotEqual(recommendation, None)
		self.assertEqual(recommendation.id, 0)
		self.assertEqual(recommendation.productId, "productId")
		self.assertEqual(recommendation.suggestionId, "suggestionId")
		self.assertEqual(recommendation.categoryId, "categoryId")

	def test_delete_a_recommendation(self): 
		recommendation = Recommendation(0, "productId", "recommended", "categoryId")
		recommendation.save()
		self.assertEqual(len(Recommendation.all()), 1)
		recommendation.delete()
		self.assertEqual(len(Recommendation.all()), 0)

	def test_serialize_a_recommendation(self):
		recommendation = Recommendation(0, "iPhone", "Pixel", "Digital Prodct")
		data = recommendation.serialize()
		self.assertNotEqual(data, None)
		self.assertEqual(data['id'], 0)
		self.assertEqual(data['productId'], "iPhone")
		self.assertEqual(data['suggestionId'], "Pixel")
		self.assertEqual(data['categoryId'], "Digital Prodct")

	def test_deserialize_a_recommendation(self):
		data = {"id": 1, "productId": "iPhone", "suggestionId": "Pixel", "categoryId": "Digital Prodct"}
		recommendation = Recommendation()
		recommendation.deserialize(data)
		self.assertNotEqual(recommendation, None)
		self.assertEqual(recommendation.id, 1) # id should be ignored
		self.assertEqual(recommendation.productId, "iPhone")
		self.assertEqual(recommendation.suggestionId, "Pixel")
		self.assertEqual(recommendation.categoryId, "Digital Prodct")
		# test with id passed into constructor
		recommendation = Recommendation(1)
		recommendation.deserialize(data)
		self.assertNotEqual(recommendation, None)
		self.assertEqual(recommendation.id, 1) # id should be ignored
		self.assertEqual(recommendation.productId, "iPhone")
		self.assertEqual(recommendation.suggestionId, "Pixel")
		self.assertEqual(recommendation.categoryId, "Digital Prodct")

	def test_deserialize_with_no_productId(self):
		recommendation = Recommendation()
		data = {"id": 1, "suggestionId": "Pixel", "categoryId": "Digital Prodct"}
		self.assertRaises(DataValidationError, recommendation.deserialize, data)

	def test_deserialize_with_no_data(self):
		recommendation = Recommendation(0)
		self.assertRaises(DataValidationError, recommendation.deserialize, None)

	def test_deserialize_with_bad_data(self):
		recommendation = Recommendation(0)
		self.assertRaises(DataValidationError, recommendation.deserialize, "string data")

	def test_find_a_recommendation(self):
		self.assertIsNone(Recommendation.find(0))
		recommendation = Recommendation(0, "productId", "recommended", "categoryId")
		recommendation.save()
		
		find_result = Recommendation.find(0)
		self.assertNotEqual(find_result, None)
		self.assertEqual(find_result.suggestionId, recommendation.suggestionId)

	def test_update_a_recommendation(self):
		recommendation = Recommendation(0, "productId", "recommended", "categoryId")
		recommendation.save()

		recommendation.categoryId = "newcategoryId"
		self.assertEqual(Recommendation.find(0).categoryId, "categoryId")
		recommendation.update()
		self.assertEqual(Recommendation.find(0).categoryId, "newcategoryId")

	def test_find_by_categoryId(self): 
		Recommendation(0, "productId1", "recommended1", "categoryId1").save()
		Recommendation(0, "productId2", "recommended2", "categoryId2").save()
		recommendations = Recommendation.find_by_categoryId("categoryId1")
		self.assertEqual(len(recommendations), 1)
		self.assertEqual(recommendations[0].categoryId, "categoryId1")

	def test_find_by_suggestionId(self): 
		Recommendation(0, "productId1", "suggestionId1", "categoryId1").save()
		Recommendation(0, "productId2", "suggestionId2", "categoryId2").save()
		recommendations = Recommendation.find_by_suggestionId("suggestionId1")
		self.assertEqual(len(recommendations), 1)
		self.assertEqual(recommendations[0].suggestionId, "suggestionId1")

######################################################################
#   M A I N
######################################################################
if __name__ == '__main__':
    unittest.main()
