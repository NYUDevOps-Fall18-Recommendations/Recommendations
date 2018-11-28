"""
Pet API Service Test Suite
Test cases can be run with the following:
nosetests
"""

import unittest
import logging
import json
import os
from time import sleep # use for rate limiting Cloudant Lite :(
from flask_api import status    # HTTP Status Codes
from models import Recommendation, DataValidationError
import service

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
class TestRecommendationService(unittest.TestCase):
    """ Recommendation Service tests """

    logger = logging.getLogger(__name__)

    def setUp(self):
        """Runs before each test"""
        self.app = service.app.test_client()
        Recommendation.init_db("tests")
        sleep(0.5)
        Recommendation.remove_all()
        sleep(0.5)
        Recommendation(productId='Infinity Gauntlet', suggestionId='Soul Stone', categoryId='Comics').save()
        sleep(0.5)
        Recommendation(productId='iPhone', suggestionId='iphone Case', categoryId='Electronics').save()
        sleep(0.5)

    def tearDown(self):
        """Runs towards the end of each test"""
        Recommendation.remove_all()


    def tearDown(self):
        """Runs towards the end of each test"""
        Recommendation.remove_all()

    def test_index(self):
        resp = self.app.get('/')
        self.assertEqual(resp.status_code, HTTP_200_OK)
        self.assertIn('', resp.data)

    def test_get_recommendation(self):
        self.assertEqual(self.get_recommendation_count(), 2)
        recommendation = self.get_recommendation('iPhone')[0]
        resp = self.app.get('/recommendations/{}'.format(recommendation['_id']))
        self.assertEqual(resp.status_code, HTTP_200_OK)
        data = json.loads(resp.data)
        self.assertEqual(data['suggestionId'], 'iphone Case')

    def test_get_nonexisting_recommendation(self):
        resp = self.app.get('/recommendations/{}'.format("abc"))
        self.assertEqual(resp.status_code, HTTP_404_NOT_FOUND)

    def test_create_recommendation(self):
        new_recommenation = dict(productId='Table', suggestionId='Chair', categoryId='Home Appliances')
        data = json.dumps(new_recommenation)
        resp = self.app.post('/recommendations', data=data, content_type='application/json')
        self.assertEqual(resp.status_code, status.HTTP_201_CREATED)

    def test_create_recommendation_no_content_type(self):
        new_recommedation = {'categoryId': 'Sports'}
        data = json.dumps(new_recommedation)
        resp = self.app.post('/recommendations', data=data)
        self.assertEqual(resp.status_code, HTTP_400_BAD_REQUEST)

    def test_call_recommendation_with_an_id(self):
        new_reco = {'productId': 'Car', 'categoryId': 'Automobile'}
        data = json.dumps(new_reco)
        resp = self.app.post('/recommendations/7', data=data)
        self.assertEqual(resp.status_code, HTTP_405_METHOD_NOT_ALLOWED)

    def test_list_all_recommendations(self):
        resp = self.app.get('/recommendations')
        self.assertEqual(resp.status_code, HTTP_200_OK)
        data = json.loads(resp.data)
        self.assertEqual(len(data), 2)

    def test_update_recommendation(self):
        recommendation = self.get_recommendation('iPhone')[0]
        new_recommedation = dict(productId='iPhone', suggestionId='iphone pop ups', categoryId='Electronics')
        data = json.dumps(new_recommedation)
        resp = self.app.put('/recommendations/{}'.format(recommendation['_id']), data=data, content_type='application/json')
        self.assertEqual(resp.status_code, status.HTTP_200_OK)
        new_json = json.loads(resp.data)
        self.assertEqual(new_json['suggestionId'], 'iphone pop ups')

    def test_update_recommendation_not_found(self):
        new_reco = dict(productId='samsung', suggestionId='samsung pop ups', categoryId='Electronocs')
        data = json.dumps(new_reco)
        invalidId = "123"
        recommendation = self.get_recommendation('iPhone')[0]
        resp = self.app.put('/recommendations/{}'.format(invalidId), data=data, content_type='application/json')
        self.assertEqual(resp.status_code, HTTP_404_NOT_FOUND)

    def test_query_recommendation_by_productId(self):
        resp = self.app.get('/recommendations', query_string='productId=iPhone')
        data = json.loads(resp.data)
        self.assertEqual(resp.status_code, status.HTTP_200_OK)
        self.assertEqual(len(data), 1)
        self.assertIn('iphone Case', resp.data)
        self.assertNotIn('Infinity Gauntlet', resp.data)
        data = json.loads(resp.data)
        query_item = data[0]
        self.assertEqual(query_item['categoryId'], 'Electronics')

    def test_query_recommendation_by_categoryId(self):
        resp = self.app.get('/recommendations', query_string='categoryId=Electronics')
        self.assertEqual(resp.status_code, status.HTTP_200_OK)
        self.assertGreater(len(resp.data), 0)
        self.assertIn('iphone Case', resp.data)
        self.assertNotIn('Infinity Gauntlet', resp.data)
        data = json.loads(resp.data)
        query_item = data[0]
        self.assertEqual(query_item['categoryId'], 'Electronics')

    def test_delete_recommendation(self):
        # save the current number of pets for later comparrison
        recommendation_count = self.get_recommendation_count()
        # delete a pet
        recommendation = self.get_recommendation('iPhone')[0]
        resp = self.app.delete('/recommendations/{}'.format(recommendation['_id']), content_type='application/json')
        self.assertEqual(resp.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(len(resp.data), 0)
        new_count = self.get_recommendation_count()
        self.assertEqual(new_count, recommendation_count - 1)

    def test_update_recommendationCategory(self):
         new_category = { 'categoryId': 'vehilceInsurance'}
         data = json.dumps(new_category)
         resp = self.app.put('/recommendations/category/Electronics', data=data, content_type='application/json')
         self.assertEqual(resp.status_code, status.HTTP_200_OK)

    def test_update_recommendationCategory_not_found(self):
         dataToUpdate = dict(categoryId='vehicleInsurance')
         resp = self.app.put('/recommendations/category/Mechanics', data=dataToUpdate, content_type='application/json')
         self.assertEqual(resp.status_code, status.HTTP_404_NOT_FOUND)

######################################################################
# Utility functions
######################################################################
    def get_recommendation(self, productId):
        """ retrieves a pet for use in other actions """
        resp = self.app.get('/recommendations',
                            query_string='productId={}'.format(productId))
        self.assertEqual(resp.status_code, HTTP_200_OK)
        self.assertGreater(len(resp.data), 0)
        self.assertIn(productId, resp.data)
        data = json.loads(resp.data)
        return data

    def get_recommendation_count(self):
        """ save the current number of recommendations """
        resp = self.app.get('/recommendations')
        self.assertEqual(resp.status_code, status.HTTP_200_OK)
        data = json.loads(resp.data)
        return len(data)

 ######################################################################
 #   M A I N
 ######################################################################
if __name__ == '__main__':
    unittest.main()
