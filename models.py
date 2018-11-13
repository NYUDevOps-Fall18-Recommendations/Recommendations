"""
Recommendation Model
You must initlaize this class before use by calling inititlize().
"""

import os
import json
import logging
import pickle

class DataValidationError(Exception):
    """ Custom Exception with data validation fails """
    pass

class Recommendation(object):
    """ Recommendation interface to database """

    logger = logging.getLogger(__name__)

    recommendations = []

    def __init__(self, id=0, productId=None, suggestionId=None, categoryId=None):
        """ Constructor """
        self.id = int(id)
        self.productId = productId
        self.suggestionId = suggestionId
        self.categoryId = categoryId

    def save(self):
        """ 
        Saves a Recommendation
        Uses a list to store recommendations. 
        Will switch to databse for persitant storage. 
        """
        if self.productId is None:   # productId is the only required field
            raise DataValidationError('productId attribute is not set')
        self.recommendations.append(Recommendation(self.id, self.productId, self.suggestionId, self.categoryId))

    def delete(self):
        """ Deletes a Recommendation from the database """
        target_index = -1
        for i in range(len(self.recommendations)): 
            if (self.recommendations[i].id == self.id): 
                target_index = i
                break

        if target_index == -1: 
            Recommendation.logger.info('Unable to delete Recommendation with id %s', self.id)
        else: 
            del self.recommendations[target_index]

    def update(self): 
        for recommendation in Recommendation.recommendations: 
            if recommendation.id == self.id: 
                recommendation.productId = self.productId
                recommendation.suggestionId = self.suggestionId
                recommendation.categoryId = self.categoryId
            return
        Recommendation.logger.info('Unable to locate Recommendation with id %s for update', self.id)

    def serialize(self):
        """ Serializes a Recommendation into a dictionary """
        return {"id": self.id, "productId": self.productId, "suggestionId": self.suggestionId, "categoryId": self.categoryId}

    def deserialize(self, data):
        """
        Deserializes a Recommendation from a dictionary
        Args:
            data (dict): A dictionary containing the Recommendation data
        """
        if not isinstance(data, dict):
            raise DataValidationError('Invalid recommendation: body of request contained bad or no data')
        try:
            self.id = data['id']
            self.productId = data['productId']
            self.suggestionId = data['suggestionId']
            self.categoryId = data['categoryId']
        except KeyError as err:
            raise DataValidationError('Invalid pet: missing ' + err.args[0])
        return


######################################################################
#  S T A T I C   D A T A B S E   M E T H O D S
######################################################################

    @staticmethod
    def remove_all():
        """ Removes all Recommendations """
        Recommendation.recommendations = list()


    @staticmethod
    def all():
        """ Query that returns all recommendations """
        return Recommendation.recommendations


    @staticmethod
    def find(targetId): 
        for recommendation in Recommendation.recommendations: 
            if (recommendation.id == targetId): 
                return recommendation
        return None


    @staticmethod
    def __find_by(attribute, value):
        """ Generic Query that finds a key with a specific value """
        # return [recommendation for recommendation in recommendation.__data
        # if recommendation.categoryId == categoryId]
        Recommendation.logger.info('Processing %s query for %s', attribute, value)
        if isinstance(value, str):
            search_criteria = value.lower() # make case insensitive
        else:
            search_criteria = value
        results = []

        for recommendation in Recommendation.recommendations: 
            if attribute == "categoryId": 
                if recommendation.categoryId == value: 
                    results.append(recommendation)
            elif attribute == "suggestionId": 
                if recommendation.suggestionId == value: 
                    results.append(recommendation)
            else: 
                return results

        return results

    @staticmethod
    def find_by_categoryId(categoryId): 
        return Recommendation.__find_by("categoryId", categoryId)

    @staticmethod
    def find_by_suggestionId(suggestionId): 
        return Recommendation.__find_by("suggestionId", suggestionId)
