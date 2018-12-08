"""
Recommendation Service Runner
Start the Pet Service and initializes logging
"""

import os
<<<<<<< HEAD
from app import app, server
=======
from service import app, service
>>>>>>> e01020988b9fb35598c82b84e31c68359596c2e0

# Pull options from environment
DEBUG = (os.getenv('DEBUG', 'False') == 'True')
PORT = os.getenv('PORT', '5000')

######################################################################
#   M A I N
######################################################################
if __name__ == "__main__":
    print "*************************************************************"
    print " R E C O M M E N D A T I O N   S E R V I C E   R U N N I N G"
    print "*************************************************************"

    #server.initialize_logging()
    app.run(host='0.0.0.0', port=int(PORT), debug=DEBUG)
