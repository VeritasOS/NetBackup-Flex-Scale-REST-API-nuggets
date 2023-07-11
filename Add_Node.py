"""This scenario adds a node in existing cluster

    Scenario requires below Environment Variables:
    APPLIANCE_ADMIN_USERNAME=""
    APPLIANCE_ADMIN_PASSWORD=""
    API_GATEWAY_IP=""
    MEDIA_SERVER_FQDN=""
    MEDIA_SERVER_IP=""
    NETWORK=""
    NETMASK=""
    STORAGE_SERVER_FQDN=""
    STORAGE_SERVER_IP=""
    NODE_NAME=""
    MANAGEMENT_FQDN=""
    MANAGEMENT_IP=""
    INTERFACE_NAME=""
    IS_BONDED=""

    if Data n/w is bonded,
    INTERFACE_NAME="bond0"
    IS_BONDED="yes"
"""

import logging
import os
import sys
import utils
import log

sys.path.append(os.path.realpath('..'))

# Initializing logger
logger = logging.getLogger('Add_Node')
logger.addHandler(logging.NullHandler())

log.init_logger()

def main():
    # Write function to Validate required parameter
    username = os.environ.get("APPLIANCE_ADMIN_USERNAME", None)
    passwd = os.environ.get("APPLIANCE_ADMIN_PASSWORD", None)
    api_gateway = os.environ.get("API_GATEWAY_IP", None)

    # Add node specific inputs
    media_fqdn = os.environ.get("MEDIA_SERVER_FQDN", None)
    media_ip = os.environ.get("MEDIA_SERVER_IP", None)
    network = os.environ.get("NETWORK", None)
    netmask = os.environ.get("NETMASK", None)

    storage_fqdn = os.environ.get("STORAGE_SERVER_FQDN", None)
    storage_ip = os.environ.get("STORAGE_SERVER_IP", None)

    new_node_name = os.environ.get("NODE_NAME", None)
    management_fqdn = os.environ.get("MANAGEMENT_FQDN", None)
    management_ip = os.environ.get("MANAGEMENT_IP", None)
    interface_name = os.environ.get("INTERFACE_NAME", None)
    if os.environ.get("IS_BONDED", None) == 'yes':
        is_bonded = True
    else:
        is_bonded = False

    # Input parameter validation
    if (not username or not passwd or not api_gateway or
        not media_fqdn or not media_ip or not network or
        not netmask or not storage_fqdn or not storage_ip
        or not new_node_name or not management_fqdn or
        not management_ip or not interface_name):
        logger.error("Missing required environment variable/s,"
         "please check doc string for required variables")
        return 1

    # Description: Discover new nodes
    response = utils.run_api(api_gateway,
                            "/api/appliance/v1.0/storage/new-nodes",
                            username, passwd, req_type='get')
    # Get Avahi IPs
    avahi_ip_list = []
    if response["data"]:
        for urls in response["data"]:
            node_addr = urls['links']['self']['href']
            final_node = node_addr.split("/")[-1]
            avahi_ip_list.append(final_node)
    else:
        logger.error("Unable to get new node information")
        sys.exit()

    # Sync patch upgrade on new nodes
    data = {"avahiIpAddress": avahi_ip_list[0]}
    utils.run_api(api_gateway,
                "/api/appliance/v1.0/upgrade",
                username, passwd, req_type='post', data=data)

    # Payload for add node
    add_node_details = {
        "isformValid": True,
        "rebalancingPriority": "overall",
        "nodeList": [
            {
                "dataNetworkInterface": {
                    "mediaServerList": [
                        {
                            "hostName": media_fqdn,
                            "index": 0,
                            "prefix": "",
                            "ipAddress": media_ip,
                            "isBonded": is_bonded,
                            "network": network,
                            "subnetMask": netmask
                        }
                    ],
                    "storageServerList": [
                        {
                            "interfaceName": interface_name,
                            "hostName": storage_fqdn,
                            "index": 0,
                            "prefix": "",
                            "ipAddress": storage_ip,
                            "isBonded": is_bonded,
                            "network": network,
                            "subnetMask": netmask
                        }
                    ]
                },
                "discoveredNodeDetails": {
                    "avahiIpAddress": avahi_ip_list[0],
                    "discoveredNodeHostName": "nbfs"
                },
                "newNodeHostDetails": {
                    "hostName": new_node_name,
                    "index": 0
                },
                "ipmiInterface": {
                    "ipAddress": ""
                },
                "managementInterface": {
                    "hostName": management_fqdn,
                    "index": 0,
                    "ipAddress": management_ip,
                }
            }
        ]
    }
    # Add new node
    utils.run_api(api_gateway,
                "/api/appliance/v1.0/storage/nodes",
                username, passwd, req_type='post', data=add_node_details)

    # Rebalancing data on nodes
    utils.run_api(api_gateway,
                "/api/appliance/v1.0/storage/rebalance",
                username, passwd, req_type='post')

    # Adding backup engine on new node
    utils.run_api(api_gateway,
                "/api/appliance/v1.0/netbackup/add",
                username, passwd, req_type='post', data=add_node_details)

    # Syncing data EEBs on new node
    data = {"avahiIpAddress": avahi_ip_list[0], "eebType": "data"}
    utils.run_api(api_gateway,
                "/api/appliance/v1.0/upgrade",
                username, passwd, req_type='post', data=data)

if __name__ == "__main__":
    main()
