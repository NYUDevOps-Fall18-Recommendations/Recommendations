
"""
This module contains all of Resources for the Recommendation Shop API
"""
from flask import abort, request
from flask_restful import Resource
from flask_api import status    # HTTP Status Codes
from werkzeug.exceptions import BadRequest
from service import app, api
from service.models import Recommendation, DataValidationError

######################################################################
#  PATH: /recommendations/{id}
######################################################################
class RecommendationResource(Resource):
    """
    RecommendationResource class
    Allows the manipulation of a single Recommendation
    GET /recommendation{id} - Returns a Recommendation with the id
    PUT /recommendation{id} - Update a Recommendation with the id
    DELETE /recommendation{id} -  Deletes a Recommendation with the id
    """

    def get(self, recommendation_id):
        """
        Retrieve a single Recommendation
        This endpoint will return a Recommendation based on it's id
        """
        app.logger.info("Request to Retrieve a recommendation with id [%s]", recommendation_id)
        recommendation = Recommendation.find(recommendation_id)
        if not recommendation:
            abort(status.HTTP_404_NOT_FOUND, "Recommendation with id '{}' was not found.".format(recommendation_id))
        return recommendation.serialize(), status.HTTP_200_OK


    def put(self, recommendation_id):
        """
        Update a Recommendation
        This endpoint will update a Recommendation based the body that is posted
        """
        app.logger.info('Request to Update a recommendation with id [%s]', recommendation_id)
        #check_content_type('application/json')
        recommendation = Recommendation.find(recommendation_id)
        if not recommendation:
            abort(status.HTTP_404_NOT_FOUND, "Recommendation with id '{}' was not found.".format(recommendation_id))

        payload = request.get_json()
        try:
            recommendation.deserialize(payload)
        except DataValidationError as error:
            raise BadRequest(str(error))

        recommendation.id = recommendation_id
        recommendation.update()
        return recommendation.serialize(), status.HTTP_200_OK

    def delete(self, recommendation_id):
        """
        Delete a Recommendation
        This endpoint will delete a Recommendation based the id specified in the path
        """
        app.logger.info('Request to Delete a recommendation with id [%s]', recommendation_id)
        recommendation = Recommendation.find(recommendation_id)
        if recommendation:
            recommendation.delete()
        return '', status.HTTP_204_NO_CONTENT

class ResetRecommendations(Resource):
    def delete(self):
        """ Removes all recommendations from the database """
        # app.logger.info(os.environ)
        Recommendation.remove_all()
        return '', status.HTTP_204_NO_CONTENT
