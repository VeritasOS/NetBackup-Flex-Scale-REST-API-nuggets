""" This scenario set immutability state of cluster

	Scenario requires below Environment Variables:
	APPLIANCE_ADMIN_USERNAME=""
	APPLIANCE_ADMIN_PASSWORD=""
	API_GATEWAY_IP=""
	LOCKDOWN_MODE=""
	    Expected Values: normal/compliance/enterprise
	Optional:
	    MINIMUM_RETENTION=""   Default value is 0
	    MAXIMUM_RETENTION=""   Default value is 0
"""

import logging
import os
import sys
import utils
import log

sys.path.append(os.path.realpath('..'))

logger = logging.getLogger('set_immutability_state')
logger.addHandler(logging.NullHandler())

log.init_logger()

def main():
	username = os.environ["APPLIANCE_ADMIN_USERNAME"]
	passwd = os.environ["APPLIANCE_ADMIN_PASSWORD"]
	api_gateway = os.environ["API_GATEWAY_IP"]
	lockdownMode = os.environ["LOCKDOWN_MODE"]
	min_retention = os.environ.get("MINIMUM_RETENTION", 0)
	max_retention = os.environ.get("MAXIMUM_RETENTION", 0)

	# Input parameter validation
	if(not username or not passwd or not api_gateway):
		logger.error("Missing required environment variable/s,"
					"please check doc string for required variables")
		return 1

	# Description: Set immutability state/lockdown mode
	data = {"lockdownMode": "{}".format(lockdownMode),
			"minimumRetention": "{}".format(min_retention),
			"maximumRetention": "{}".format(max_retention)}
	utils.run_api(api_gateway,
				"/api/appliance/v1.0/security/lockdown-mode",
				username, passwd, req_type='post', data=data)

if __name__ == "__main__":
    main()
