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
        self.recommendations.append(self)

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


######################################################################
#  F I N D E R   M E T H O D S
######################################################################

    @staticmethod
    def find(recommendation_id):
        """ Query that finds Pets by their id """
        for recommendation in Recommendation.recommendations: 
            if recommendation.id == recommendation_id: 
                return recommendation

        return None
