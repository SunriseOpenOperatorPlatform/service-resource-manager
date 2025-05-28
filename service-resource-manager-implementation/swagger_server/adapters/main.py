# -*- coding: utf-8 -*-
from src import logger
from src.edgecloud.core.edgecloud_factory import EdgeCloudFactory

logger.setup_logger(is_debug=True, file_name="sdk.log")


def create_edgecloud_client(client_name: str, base_url: str):
    """
    Create and return an edgecloud client.

    Args:
        client_name (str): Name of the edge cloud platform. Must be one of:
                          'i2edge', 'aeros', 'piedge'
        base_url (str): The base URL for the client.

    Returns:
        The created edgecloud client.

    Example:
        >>> client = create_edgecloud_client('i2edge', 'http://localhost:8080')
    """
    return EdgeCloudFactory.create_edgecloud_client(client_name, base_url)


# ###########################################
# # Temporal code - Testing purposes
# ###########################################
# if __name__ == "__main__":
#     # Define the client name and base URL
#     client_name = "i2edge"
#     base_url = "http://192.168.123.237:30769/"

#     # Create the edgecloud client
#     sbi = EdgeCloudFactory.create_edgecloud_client(client_name, base_url)

#     # Print the edgecloud client being used and its URL
#     print(f"Using edgecloud client: {sbi}")
#     print(f"Edge Cloud Platform: {client_name}")
#     print(f"URL: {sbi.base_url}")
#     print("")

#     # Get all availability zones
#     print("Running test endpoint: get_edge_cloud_zones:")
#     zones = sbi.get_edge_cloud_zones()
#     print(zones)
# ###########################################
# # End of temporal code
# ###########################################
