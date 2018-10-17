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
		recommendation = Recommendation(0, "name", "suggestion", "category")
		self.assertNotEqual(recommendation, None)
		self.assertEqual(recommendation.id, 0)
		self.assertEqual(recommendation.name, "name")
		self.assertEqual(recommendation.suggestion, "suggestion")
		self.assertEqual(recommendation.category, "category")

	def test_delete_a_recommendation(self): 
		recommendation = Recommendation(0, "name", "recommended", "category")
		recommendation.save()
		self.assertEqual(len(Recommendation.all()), 1)
		recommendation.delete()
		self.assertEqual(len(Recommendation.all()), 0)

	def test_serialize_a_recommendation(self):
		recommendation = Recommendation(0, "iPhone", "Pixel", "Digital Prodct")
		data = recommendation.serialize()
		self.assertNotEqual(data, None)
		self.assertEqual(data['id'], 0)
		self.assertEqual(data['name'], "iPhone")
		self.assertEqual(data['suggestion'], "Pixel")
		self.assertEqual(data['category'], "Digital Prodct")

	def test_deserialize_a_recommendation(self):
		data = {"id": 1, "name": "iPhone", "suggestion": "Pixel", "category": "Digital Prodct"}
		recommendation = Recommendation()
		recommendation.deserialize(data)
		self.assertNotEqual(recommendation, None)
		self.assertEqual(recommendation.id, 1) # id should be ignored
		self.assertEqual(recommendation.name, "iPhone")
		self.assertEqual(recommendation.suggestion, "Pixel")
		self.assertEqual(recommendation.category, "Digital Prodct")
		# test with id passed into constructor
		recommendation = Recommendation(1)
		recommendation.deserialize(data)
		self.assertNotEqual(recommendation, None)
		self.assertEqual(recommendation.id, 1) # id should be ignored
		self.assertEqual(recommendation.name, "iPhone")
		self.assertEqual(recommendation.suggestion, "Pixel")
		self.assertEqual(recommendation.category, "Digital Prodct")

	def test_deserialize_with_no_name(self):
		recommendation = Recommendation()
		data = {"id": 1, "suggestion": "Pixel", "category": "Digital Prodct"}
		self.assertRaises(DataValidationError, recommendation.deserialize, data)

	def test_deserialize_with_no_data(self):
		recommendation = Recommendation(0)
		self.assertRaises(DataValidationError, recommendation.deserialize, None)

	def test_deserialize_with_bad_data(self):
		recommendation = Recommendation(0)
		self.assertRaises(DataValidationError, recommendation.deserialize, "string data")

	def test_find_a_recommendation(self):
		self.assertIsNone(Recommendation.find(0))
		recommendation = Recommendation(0, "name", "recommended", "category")
		recommendation.save()
		
		find_result = Recommendation.find(0)
		self.assertNotEqual(find_result, None)
		self.assertEqual(find_result.suggestion, recommendation.suggestion)

	def test_update_a_recommendation(self):
		recommendation = Recommendation(0, "name", "recommended", "category")
		recommendation.save()

		recommendation.category = "newCategory"
		self.assertEqual(Recommendation.find(0).category, "category")
		recommendation.update()
		self.assertEqual(Recommendation.find(0).category, "newCategory")

	def test_find_by_category(self): 
		Recommendation(0, "name1", "recommended1", "category1").save()
		Recommendation(0, "name2", "recommended2", "category2").save()
		recommendations = Recommendation.find_by_category("category1")
		self.assertEqual(len(recommendations), 1)
		self.assertEqual(recommendations[0].category, "category1")

	def test_find_by_suggestion(self): 
		Recommendation(0, "name1", "suggestion1", "category1").save()
		Recommendation(0, "name2", "suggestion2", "category2").save()
		recommendations = Recommendation.find_by_suggestion("suggestion1")
		self.assertEqual(len(recommendations), 1)
		self.assertEqual(recommendations[0].suggestion, "suggestion1")

######################################################################
#   M A I N
######################################################################
if __name__ == '__main__':
    unittest.main()
