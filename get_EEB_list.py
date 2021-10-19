"""This scenario list of all EEBs installed on cluster

	Scenario requires below Environment Variables:
	APPLIANCE_ADMIN_USERNAME=""
	APPLIANCE_ADMIN_PASSWORD=""
	API_GATEWAY_IP=""
"""

import logging
import os
import sys
import utils
import log

import pdb

sys.path.append(os.path.realpath('..'))

# Initializing logger
logger = logging.getLogger('get_EEB_list')
logger.addHandler(logging.NullHandler())

log.init_logger()

def main():
	username = os.environ.get("APPLIANCE_ADMIN_USERNAME", None)
	passwd = os.environ.get("APPLIANCE_ADMIN_PASSWORD", None)
	api_gateway = os.environ.get("API_GATEWAY_IP", None)

	# Input parameter validation
	if (not username or not passwd or not api_gateway):
		logger.error("Missing required environment variable/s,"
					"please check doc string for required variables")
		return 1

	# Description: Get List of EEBs
	utils.run_api(api_gateway, "/api/appliance/v1.0/upgrade/eebs",
				username, passwd, req_type='get')

if __name__ == "__main__":
    main()
