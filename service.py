import os
import sys
import logging
from flask import Flask, jsonify, request, url_for, make_response, abort
from flask_api import status    # HTTP Status Codes
from models import Recommendation, DataValidationError


# Create Flask application
app = Flask(__name__)
app.config['LOGGING_LEVEL'] = logging.INFO

# Pull options from environment
DEBUG = (os.getenv('DEBUG', 'False') == 'True')
PORT = os.getenv('PORT', '5000')

# Status Codes
HTTP_200_OK = 200
HTTP_201_CREATED = 201
HTTP_204_NO_CONTENT = 204
HTTP_400_BAD_REQUEST = 400
HTTP_404_NOT_FOUND = 404
HTTP_409_CONFLICT = 409

######################################################################
# Error Handlers
######################################################################
@app.errorhandler(DataValidationError)
def request_validation_error(error):
    """ Handles Value Errors from bad data """
    return bad_request(error)

@app.errorhandler(400)
def bad_request(error):
    """ Handles bad reuests with 400_BAD_REQUEST """
    message = error.message or str(error)
    app.logger.info(message)
    return jsonify(status=400, error='Bad Request', message=message), 400

@app.errorhandler(404)
def not_found(error):
    """ Handles resources not found with 404_NOT_FOUND """
    message = error.message or str(error)
    app.logger.info(message)
    return jsonify(status=404, error='Not Found', message=message), 404

@app.errorhandler(405)
def method_not_supported(error):
    """ Handles unsuppoted HTTP methods with 405_METHOD_NOT_SUPPORTED """
    message = error.message or str(error)
    app.logger.info(message)
    return jsonify(status=405, error='Method not Allowed', message=message), 405

@app.errorhandler(415)
def mediatype_not_supported(error):
    """ Handles unsuppoted media requests with 415_UNSUPPORTED_MEDIA_TYPE """
    message = error.message or str(error)
    app.logger.info(message)
    return jsonify(status=415, error='Unsupported media type', message=message), 415

@app.errorhandler(500)
def internal_server_error(error):
    """ Handles unexpected server error with 500_SERVER_ERROR """
    message = error.message or str(error)
    app.logger.info(message)
    return jsonify(status=500, error='Internal Server Error', message=message), 500


######################################################################
# GET INDEX
######################################################################
@app.route('/')
def index():
    """ Send back the home page """
    return 'Hello World, from Recommendation microservice'

######################################################################
# LIST ALL RECOMMENDATIONS
######################################################################
@app.route('/recommendations', methods=['GET'])
def list_recommendations():
    """ Retrieves a list of pets from the database """
    app.logger.info('Listing pets')
    results = []
    categoryId = request.args.get('categoryId')
    productId = request.args.get('productId')
    suggestionId = request.args.get('suggestionId')
    if categoryId:
        results = Recommendation.find_by_categoryId(categoryId)
    elif productId: 
        results = Recommendation.find_by_productId(productId)
    elif suggestionId: 
        results = Recommendation.find_by_suggestionId(suggestionId)
    else:
        results = Recommendation.all()

    return jsonify([rec.serialize() for rec in results]), HTTP_200_OK

######################################################################
# RETRIEVE A RECOMMENDATION BY ID
######################################################################
@app.route('/recommendations/<string:id>', methods=['GET'])
def get_recommendation(id):
    """
    Retrieve a single recommendation
    This endpoint will return a recommendation based on it's id
    """
    app.logger.info('Finding a Recommendation with id [{}]'.format(id))
    recommendation = Recommendation.find(id)
    if not recommendation:
        abort(HTTP_404_NOT_FOUND, "recommendation with id '{}' was not found.".format(id))
    return make_response(jsonify(recommendation.serialize()), HTTP_200_OK)

######################################################################
# CREATE RECOMMENDATION
######################################################################
@app.route('/recommendations', methods=['POST'])
def create_recommendation():
    """
    Creates a recommendations
    This end point will create a recommendation based on the data in the body
    """
    recommendation = Recommendation()
    recommendation.deserialize(request.get_json())
    recommendation.save()
    message = recommendation.serialize()
    return make_response(jsonify(message), status.HTTP_201_CREATED)

######################################################################
# DELETE A Recommendation
######################################################################
@app.route('/recommendations/<string:recommendation_id>', methods=['DELETE'])
def delete_recommendations(recommendation_id):
    """ Removes a Recommendation from the database that matches the id """
    app.logger.info('Deleting a Recommendation with id [{}]'.format(recommendation_id))
    recommendation = Recommendation.find(recommendation_id)
    if recommendation:
        recommendation.delete()
    else: 
        app.logger.info('Unable to find Recommendation for deletion with id [{}]'.format(recommendation_id))
    return make_response('', HTTP_204_NO_CONTENT)

######################################################################
# UPDATE RECOMMENDATION
######################################################################
@app.route('/recommendations/<string:id>', methods=['PUT'])
def update_recommendation(id):
    """
    Update a recommendation
    This end point will update a recommendation based on the data in the body
    """
    recommendation = Recommendation.find(id)
    if not recommendation:
        abort(HTTP_404_NOT_FOUND, "recommendation with id '{}' was not found.".format(id))
        # raise NotFound("recommendation with id '{}' was not found.".format(id))
    recommendation.deserialize(request.get_json())
    recommendation.id = id
    recommendation.update()
    return make_response(jsonify(recommendation.serialize()), status.HTTP_200_OK)

######################################################################
#   M A I N
######################################################################
if __name__ == "__main__":
    # initialize_logging(app.config['LOGGING_LEVEL'])
    app.run(host='0.0.0.0', port=int(PORT), debug=DEBUG)
