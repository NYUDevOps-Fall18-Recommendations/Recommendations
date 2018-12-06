"""
This module contains the Recommendation Collection Resource
"""
from flask import request, abort
from flask_restful import Resource
from flask_api import status    # HTTP Status Codes
from werkzeug.exceptions import BadRequest
from service import app, api
from service.models import Recommendation, DataValidationError
from . import RecommendationResource

class RecommendationCollection(Resource):
    """ Handles all interactions with collections of Recommendations """

    def get(self):
        """ Returns all of the Recommendations """
        app.logger.info('Listing recommendations')
        recommendations = []
        categoryId = request.args.get('categoryId')
        productId = request.args.get('productId')
        suggestionId = request.args.get('suggestionId')
        if categoryId:
            recommendations = Recommendation.find_by_categoryId(categoryId)
        elif productId:
            recommendations = Recommendation.find_by_productId(productId)
        elif suggestionId:
            recommendations = Recommendation.find_by_suggestionId(suggestionId)
        else:
            recommendations = Recommendation.all()

        app.logger.info('[%s] Recommendations returned', len(recommendations))
        results = [recommendation.serialize() for recommendation in recommendations]
        return results, status.HTTP_200_OK

    def post(self):
        """
        Creates a Recommendation
        This endpoint will create a Recommendation based the data in the body that is posted
        or data that is sent via an html form post.
        """
        app.logger.info('Request to Create a Recommendation')
        content_type = request.headers.get('Content-Type')
        if not content_type:
            abort(status.HTTP_400_BAD_REQUEST, "No Content-Type set")

        data = {}
        # Check for form submission data
        if content_type == 'application/x-www-form-urlencoded':
            app.logger.info('Processing FORM data')
            app.logger.info(type(request.form))
            app.logger.info(request.form)
            data = {
                'name': request.form['name'],
                'category': request.form['category'],
                'available': request.form['available'].lower() in ['yes', 'y', 'true', 't', '1']
            }
        elif content_type == 'application/json':
            app.logger.info('Processing JSON data')
            data = request.get_json()
        else:
            message = 'Unsupported Content-Type: {}'.format(content_type)
            app.logger.info(message)
            abort(status.HTTP_400_BAD_REQUEST, message)

        recommendation = Recommendation()
        try:
            recommendation.deserialize(data)
        except DataValidationError as error:
            raise BadRequest(str(error))
        recommendation.save()
        app.logger.info('Recommendation with new id [%s] saved!', recommendation.id)
        location_url = api.url_for(RecommendationResource, recommendation_id=recommendation.id, _external=True)
        app.logger.info('Location url [%s]', location_url)
        return recommendation.serialize(), status.HTTP_201_CREATED, {'Location': location_url}