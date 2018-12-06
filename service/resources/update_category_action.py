
"""
This module contains routes without Resources
"""
from flask import abort, request, jsonify
from flask_api import status
from flask_restful import Resource
from service.models import Recommendation

######################################################################
# Update category of recommendations
######################################################################
class UpdateCategoryAction(Resource):
    """ Resource to Purchase a Pet """
    def put(self, categoryId):

        """
        Update a recommendation category
        This end point will update a recommendation category for all RELEVANT RECOMMENDATIONS
        based on the data in the body
        """
        results = Recommendation.find_by_categoryId(categoryId)
        if(len(results) == 0):
               # message = {'error' : 'Recommendation with categoryId: %s was not found' % str(categoryId)}
               return_code = status.HTTP_404_NOT_FOUND
               return '', return_code

        data = request.get_json()
        i = 0
        sizeOfResults = len(results)
        while i < sizeOfResults:
            recommendation = Recommendation.find(results[i].id)
            recommendation.categoryId = data['categoryId']
            recommendation.update()
            i += 1
        # message = {'success' : 'RECOMMENDATIONS category updated'}
        return '', status.HTTP_200_OK
        # return make_response('success', status.HTTP_200_OK)

        # """ Purchase a Pet """
        # pet = Pet.find(pet_id)
        # if not pet:
        #     abort(status.HTTP_404_NOT_FOUND, "Pet with id '{}' was not found.".format(pet_id))
        # if not pet.available:
        #     abort(status.HTTP_400_BAD_REQUEST, "Pet with id '{}' is not available.".format(pet_id))
        # pet.available = False
        # pet.save()
        # return pet.serialize(), status.HTTP_200_OK