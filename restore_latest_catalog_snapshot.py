""" This scenario restores latest catalog snapshot

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

sys.path.append(os.path.realpath('..'))

logger = logging.getLogger('restore_latest_catalog_snapshot')
logger.addHandler(logging.NullHandler())

log.init_logger()

def main():
    username = os.environ["APPLIANCE_ADMIN_USERNAME"]
    passwd = os.environ["APPLIANCE_ADMIN_PASSWORD"]
    api_gateway = os.environ["API_GATEWAY_IP"]
    
    # Input parameter validation
    if(not username or not passwd or not api_gateway):
        logger.error("Missing required environment variable/s,"
                    "please check doc string for required variables")
        return 1

    # Description: Get catalog Snapshots
    response = utils.run_api(api_gateway,
                            "/api/appliance/v1.0/netbackup/checkpoints",
                            username, passwd, req_type="get")

    # Get latest snapshot
    latest_snapshot = response["data"][0]["links"]["self"]["href"].split("/")[-1]

    # Restore latest catalog snapshot
    utils.run_api(api_gateway,
                "/api/appliance/v1.0/netbackup/checkpoints/restore"
                "-catalog/{}".format(latest_snapshot), username,
                passwd,  req_type="post")

if __name__ == "__main__":
    main()
