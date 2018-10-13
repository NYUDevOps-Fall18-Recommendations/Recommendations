import os
import sys
import logging
from flask import Flask, jsonify, request, url_for, make_response, abort
from models import Recommendation, DataValidationError


# Create Flask application
app = Flask(__name__)
# app.config['LOGGING_LEVEL'] = logging.INFO

# Pull options from environment
DEBUG = (os.getenv('DEBUG', 'False') == 'True')
PORT = os.getenv('PORT', '5000')


######################################################################
# GET INDEX
######################################################################
@app.route('/')
def index():
    """ Send back the home page """
    return 'Hello World'


######################################################################
# DELETE A Recommendation
######################################################################
@app.route('/recommendations/<int:recommendation_id>', methods=['DELETE'])
def delete_recommendations(recommendation_id):
    """
    Delete a Recommendation
    This endpoint will delete a Recommendation based the id specified in the path
    """
    recommendation = Recommendation.find(recommendation_id)
    if recommendation:
        recommendation.delete()
    return make_response('', HTTP_204_NO_CONTENT)


######################################################################
#   M A I N
######################################################################
if __name__ == "__main__":
    # initialize_logging(app.config['LOGGING_LEVEL'])
    app.run(host='0.0.0.0', port=int(PORT), debug=DEBUG)