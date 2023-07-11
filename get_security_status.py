"""This scenario lists STIG and FIPS status of a given cluster
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

logger = logging.getLogger('get_security_status')
logger.addHandler(logging.NullHandler())

log.init_logger()

def main():

    username = os.environ.get("APPLIANCE_ADMIN_USERNAME", None)
    passwd = os.environ.get("APPLIANCE_ADMIN_PASSWORD", None)
    api_gateway = os.environ.get("API_GATEWAY_IP", None)

    # Input parameter validation
    if(not username or not passwd or not api_gateway):
        logger.error("Missing required environment variable/s,"
                    "please check doc string for required variables")
        return 1

    def security_apis(username, passwd, api_gateway):

        # Description: Get FIPS status
        logger.info("Current FIPS status: ")
        res = utils.run_api(api_gateway, "/api/appliance/v1.0/security/fips",
                username, passwd, req_type='get')

        # Description: Get STIG status
        logger.info("Current STIG status: ")
        utils.run_api(api_gateway, "/api/appliance/v1.0/security/stig",
                    username, passwd, req_type='get')

        # Description: Get lockdown-mode
        logger.info("Current Lockdown mode: ")
        utils.run_api(api_gateway, "/api/appliance/v1.0/security/lockdown"
                "-mode", username, passwd, req_type='get')

        # Description: Get certificate(s) on cluster 
        logger.info("All the certificates: ")
        res = utils.run_api(api_gateway, "/api/appliance/v1.0/certificates",
                username, passwd, req_type='get')
        certs_data = res["data"]
        certs_list = [ cert["links"]["self"]["href"].rsplit('/',1)[-1] for cert in certs_data ]
        for cert in certs_list:
            res = utils.run_api(api_gateway, "/api/appliance/v1.0/certificates/" + cert,
                username, passwd, req_type='get')

        # Description: Get certificate signing requests 
        logger.info("CSRS details...")
        utils.run_api(api_gateway, "/api/appliance/v1.0/security/csrs",
                username, passwd, req_type='get')

        # Description: Get default password policies
        logger.info("Default password policies details...")
        utils.run_api(api_gateway, "/api/appliance/v1.0/security/password-policies/default",
                username, passwd, req_type='get')

        # Description: Get current password policies
        logger.info("Current password policies...")
        utils.run_api(api_gateway, "/api/appliance/v1.0/security/password-policies",
                username, passwd, req_type='get')

        # Description: Get login banners
        logger.info("Login banners...")
        utils.run_api(api_gateway, "/api/appliance/v1.0/security/login-banners",
                username, passwd, req_type='get')

        # Description: Get server information
        logger.info("Cluster server details...")
        utils.run_api(api_gateway, "/api/appliance/v1.0/security/server-info",
                username, passwd, req_type='get')

    if os.environ.get("DR") == 'yes':
        logger.info("*** Primary Site Security Settings ***")
        security_apis(username, passwd, api_gateway)
        username = os.environ.get("DR_SITE_ADMIN_USERNAME", None)
        passwd = os.environ.get("DR_SITE_ADMIN_PASSWORD", None)
        api_gateway = os.environ.get("DR_SITE_API_GATEWAY_IP", None)
        if(not username or not passwd or not api_gateway):
            logger.error("Missing required environment variable/s for DR site,"
                        "please check doc string for required variables")
            return 1
        logger.info("*** Secondary Site Security Settings ***")
        security_apis(username, passwd, api_gateway)

    if os.environ.get("DR") == 'no' :
        security_apis(username, passwd, api_gateway)

if __name__ == "__main__":
    main()
