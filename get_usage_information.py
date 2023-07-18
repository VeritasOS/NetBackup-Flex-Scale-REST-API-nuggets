"""This scenario get usage infomation from the cluster

    Scenario requires below Environment Variables:
    APPLIANCE_ADMIN_USERNAME=""
    APPLIANCE_ADMIN_PASSWORD=""
    API_GATEWAY_IP=""
    In case DR is configured,
    DR_SITE_ADMIN_USERNAME=""
    DR_SITE_ADMIN_PASSWORD=""
    DR_SITE_API_GATEWAY_IP=""
    DR='yes'

"""

import logging
import os
import sys
import utils
import log

sys.path.append(os.path.realpath('..'))

# Initializing logger
logger = logging.getLogger('get_usage_information')
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

    def get_cluster_id(username, passwd, api_gateway):
    # Get local cluster ID
        response = utils.run_api(api_gateway,
                             "/api/appliance/v1.0/storage/clusters",
                             username, passwd, req_type='get')
        url = response["data"][0]["links"]["self"]["href"]
        cluster_id = url.rsplit('/', 1)[-1]
        #logger.info("clusterId: {}".format(cluster_id))
        return cluster_id

    def get_storage_utilized(username, passwd, api_gateway):
    # Description: Getting storage utilization in local cluster
        cluster_id = get_cluster_id(username, passwd, api_gateway)
        utils.run_api(api_gateway,
                "/api/appliance/v1.0/storage/clusters/" + cluster_id + "/storage-utilised",
                username, passwd, req_type='get')

    if os.environ.get("DR") == 'yes':
        logger.info("*** Primary Site Storage Utilization ***")
        get_storage_utilized(username, passwd, api_gateway)
        username = os.environ.get("DR_SITE_ADMIN_USERNAME", None)
        passwd = os.environ.get("DR_SITE_ADMIN_PASSWORD", None)
        api_gateway = os.environ.get("DR_SITE_API_GATEWAY_IP", None)
        if(not username or not passwd or not api_gateway):
            logger.error("Missing required environment variable/s for DR site,"
                        "please check doc string for required variables")
            return 1
        logger.info("*** Secondary Site Storage Utilization ***")
        get_storage_utilized(username, passwd, api_gateway)

    if os.environ.get("DR") == 'no' :
        logger.info("*** Cluster Storage Utilization ***")
        get_storage_utilized(username, passwd, api_gateway)


if __name__ == "__main__":
    main()
