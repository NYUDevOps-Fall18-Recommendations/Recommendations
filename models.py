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

    def __init__(self, id=0, name=None, suggestion=None, category=None):
        """ Constructor """
        self.id = int(id)
        self.name = name
        self.suggestion = suggestion
        self.category = category

    def save(self):
        """ 
        Saves a Recommendation
        Uses a list to store recommendations. 
        Will switch to databse for persitant storage. 
        """
        if self.name is None:   # name is the only required field
            raise DataValidationError('name attribute is not set')
        self.recommendations.append(Recommendation(self.id, self.name, self.suggestion, self.category))

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

    def find(targetId): 
        for recommendation in Recommendation.recommendations: 
            if (recommendation.id == targetId): 
                return recommendation
        return None

    def update(self): 
        for recommendation in Recommendation.recommendations: 
            if recommendation.id == self.id: 
                recommendation.name = self.name
                recommendation.suggestion = self.suggestion
                recommendation.category = self.category
            return
        Recommendation.logger.info('Unable to locate Recommendation with id %s for update', self.id)


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
    def __find_by(attribute, value):
        """ Generic Query that finds a key with a specific value """
        # return [recommendation for recommendation in recommendation.__data
        # if recommendation.category == category]
        Recommendation.logger.info('Processing %s query for %s', attribute, value)
        if isinstance(value, str):
            search_criteria = value.lower() # make case insensitive
        else:
            search_criteria = value
        results = []

        for recommendation in Recommendation.recommendations: 
            if attribute == "category": 
                if recommendation.category == value: 
                    results.append(recommendation)
            elif attribute == "suggestion": 
                if recommendation.suggestion == value: 
                    results.append(recommendation)
            else: 
                return results

        return results

    @staticmethod
    def find_by_category(category): 
        return Recommendation.__find_by("category", category)

    @staticmethod
    def find_by_suggestion(suggestion): 
        return Recommendation.__find_by("suggestion", suggestion)
