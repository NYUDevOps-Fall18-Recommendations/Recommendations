"""
Recommendation Model that uses Redis
You must initlaize this class before use by calling inititlize().
This class looks for an environment variable called VCAP_SERVICES
to get it's database credentials from. If it cannot find one, it
tries to connect to Redis on the localhost. If that fails it looks
for a server name 'redis' to connect to.
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
    redis = None

    def __init__(self, id=0, name=None, suggestion=None, category=None):
        """ Constructor """
        self.id = int(id)
        self.name = name
        self.suggestion = suggestion
        self.category = category

    def save(self):
        """ Saves a Recommendation in the database """
        if self.name is None:   # name is the only required field
            raise DataValidationError('name attribute is not set')
        if self.id == 0:
            self.id = Recommendation.__next_index()
        Recommendation.redis.set(self.id, pickle.dumps(self.serialize()))

    def delete(self):
        """ Deletes a Recommendation from the database """
        Recommendation.redis.delete(self.id)

    def serialize(self):
        """ serializes a Recommendation into a dictionary """
        return {
            "id": self.id,
            "name": self.name,
            "suggestion": self.suggestion,
            "category": self.category
        }

    def deserialize(self, data):
        """ deserializes a Recommendation my marshalling the data """
        try:
            self.name = data['name']
            self.suggestion = data['suggestion']
            self.category = data['category']
        except KeyError as error:
            raise DataValidationError('Invalid Recommendation: missing ' + error.args[0])
        except TypeError as error:
            raise DataValidationError('Invalid Recommendation: body of request contained bad or no data')
        return self


######################################################################
#  S T A T I C   D A T A B S E   M E T H O D S
######################################################################

    @staticmethod
    def __next_index():
        """ Increments the index and returns it """
        return Recommendation.redis.incr('index')

    @staticmethod
    def remove_all():
        """ Removes all Recommendations from the database """
        Recommendation.redis.flushall()

    @staticmethod
    def all():
        """ Query that returns all Recommendations """
        # results = [Recommendation.from_dict(redis.hgetall(key)) for key in redis.keys() if key != 'index']
        results = []
        for key in Recommendation.redis.keys():
            if key != 'index':  # filer out our id index
                data = pickle.loads(Recommendation.redis.get(key))
                Recommendation = Recommendation(data['id']).deserialize(data)
                results.append(Recommendation)
        return results

######################################################################
#  F I N D E R   M E T H O D S
######################################################################

    @staticmethod
    def find(Recommendation_id):
        """ Query that finds Recommendations by their id """
        if Recommendation.redis.exists(Recommendation_id):
            data = pickle.loads(Recommendation.redis.get(Recommendation_id))
            Recommendation = Recommendation(data['id']).deserialize(data)
            return Recommendation
        return None

    @staticmethod
    def __find_by(attribute, value):
        """ Generic Query that finds a key with a specific value """
        # return [Recommendation for Recommendation in Recommendation.__data if Recommendation.suggestion == suggestion]
        Recommendation.logger.info('Processing %s query for %s', attribute, value)
        if isinstance(value, str):
            search_criteria = value.lower() # make case insensitive
        else:
            search_criteria = value
        results = []
        for key in Recommendation.redis.keys():
            if key != 'index':  # filer out our id index
                data = pickle.loads(Recommendation.redis.get(key))
                # perform case insensitive search on strings
                if isinstance(data[attribute], str):
                    test_value = data[attribute].lower()
                else:
                    test_value = data[attribute]
                if test_value == search_criteria:
                    results.append(Recommendation(data['id']).deserialize(data))
        return results

    @staticmethod
    def find_by_name(name):
        """ Query that finds Recommendations by their name """
        return Recommendation.__find_by('name', name)

    @staticmethod
    def find_by_suggestion(suggestion):
        """ Query that finds Recommendations by their suggestion """
        return Recommendation.__find_by('suggestion', suggestion)

    @staticmethod
    def find_by_category(category):
        """ Query that finds Recommendations by their availability """
        return Recommendation.__find_by('category', category)

######################################################################
#  R E D I S   D A T A B A S E   C O N N E C T I O N   M E T H O D S
######################################################################

    @staticmethod
    def connect_to_redis(hostname, port, password):
        """ Connects to Redis and tests the connection """
        Recommendation.logger.info("Testing Connection to: %s:%s", hostname, port)
        Recommendation.redis = Redis(host=hostname, port=port, password=password)
        try:
            Recommendation.redis.ping()
            Recommendation.logger.info("Connection established")
        except ConnectionError:
            Recommendation.logger.info("Connection Error from: %s:%s", hostname, port)
            Recommendation.redis = None
        return Recommendation.redis

    @staticmethod
    def init_db(redis=None):
        """
        Initialized Redis database connection
        This method will work in the following conditions:
          1) In Bluemix with Redis bound through VCAP_SERVICES
          2) With Redis running on the local server as with Travis CI
          3) With Redis --link in a Docker container called 'redis'
          4) Passing in your own Redis connection object
        Exception:
        ----------
          redis.ConnectionError - if ping() test fails
        """
        if redis:
            Recommendation.logger.info("Using client connection...")
            Recommendation.redis = redis
            try:
                Recommendation.redis.ping()
                Recommendation.logger.info("Connection established")
            except ConnectionError:
                Recommendation.logger.error("Client Connection Error!")
                Recommendation.redis = None
                raise ConnectionError('Could not connect to the Redis Service')
            return
        # Get the credentials from the Bluemix environment
        if 'VCAP_SERVICES' in os.environ:
            Recommendation.logger.info("Using VCAP_SERVICES...")
            vcap_services = os.environ['VCAP_SERVICES']
            services = json.loads(vcap_services)
            creds = services['rediscloud'][0]['credentials']
            Recommendation.logger.info("Conecting to Redis on host %s port %s",
                            creds['hostname'], creds['port'])
            Recommendation.connect_to_redis(creds['hostname'], creds['port'], creds['password'])
        else:
            Recommendation.logger.info("VCAP_SERVICES not found, checking localhost for Redis")
            Recommendation.connect_to_redis('127.0.0.1', 6379, None)
            if not Recommendation.redis:
                Recommendation.logger.info("No Redis on localhost, looking for redis host")
                Recommendation.connect_to_redis('redis', 6379, None)
        if not Recommendation.redis:
            # if you end up here, redis instance is down.
            Recommendation.logger.fatal('*** FATAL ERROR: Could not connect to the Redis Service')
            raise ConnectionError('Could not connect to the Redis Service')