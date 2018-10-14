"""
Recommendation Service:
POST /recommendation - creates a new recommendation record in the database
"""
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
# ADD A NEW RECOMMENDATION
######################################################################
@app.route('/recommendation', methods=['POST'])
def create_recommendation():
    """
    Creates a Pet
    This endpoint will create a Pet based the data in the body that is posted
    """
    check_content_type('application/json')
    recommendation = recommendation()
    pet.deserialize(request.get_json())
    pet.save()
    message = pet.serialize()
    location_url = url_for('get_pets', pet_id=pet.id, _external=True)
    return make_response(jsonify(message), status.HTTP_201_CREATED,
                         {
                             'Location': location_url
                         })
######################################################################
#   M A I N
######################################################################
if __name__ == "__main__":
    # initialize_logging(app.config['LOGGING_LEVEL'])
    app.run(host='0.0.0.0', port=int(PORT), debug=DEBUG)
