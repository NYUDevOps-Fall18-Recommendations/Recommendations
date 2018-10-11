"""
Recommendation Model
You must initlaize this class before use by calling inititlize().
"""

import os
import json
import logging
import pickle
from redis import Redis
from redis.exceptions import ConnectionError

class DataValidationError(Exception):
    """ Custom Exception with data validation fails """
    pass

class Recommendation(object):
    """ Recommendation interface to database """

    logger = logging.getLogger(__name__)

    def __init__(self, id=0, name=None, suggestion=None, category=None):
        """ Constructor """
        self.id = int(id)
        self.name = name
        self.suggestion = suggestion
        self.category = category