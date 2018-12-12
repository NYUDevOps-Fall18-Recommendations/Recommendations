"""
Package: app
Package for the application models and services
This module also sets up the logging to be used with gunicorn
"""
# RESTful Doc links:
# https://flask-restful.readthedocs.io/en/0.3.6/intermediate-usage.html
# https://flask-restful.readthedocs.io/en/0.3.6/quickstart.html
import os
import sys
import logging
from flask import Flask
from flask_restful import Api
from .models import Recommendation, DataValidationError

app = Flask(__name__)
app.config['SECRET_KEY'] = 'please, tell nobody... Shhhh'
app.config['LOGGING_LEVEL'] = logging.INFO

api = Api(app)

from .resources import RecommendationResource
from .resources import RecommendationCollection
from .resources import ResetRecommendations
from .resources import UpdateCategoryAction
from .resources import HomePage

api.add_resource(HomePage, '/')
api.add_resource(RecommendationCollection, '/recommendations')
api.add_resource(RecommendationResource, '/recommendations/<recommendation_id>')
api.add_resource(UpdateCategoryAction, '/recommendations/category/<string:categoryId>')
api.add_resource(ResetRecommendations, '/recommendations/reset')

# Set up logging for production
print('Setting up logging for {}...'.format(__name__))
if __name__ != '__main__':
    gunicorn_logger = logging.getLogger('gunicorn.error')
    if gunicorn_logger:
        app.logger.handlers = gunicorn_logger.handlers
        app.logger.setLevel(gunicorn_logger.level)

app.logger.info('************************************************************')
app.logger.info('        R E C O M D A T I O N   R E S T   A P I   S E R V I C E ')
app.logger.info('************************************************************')
app.logger.info('Logging established')


@app.before_first_request
def init_db(dbname="recommendations"):
    """ Initlaize the model """
    Recommendation.init_db(dbname)
