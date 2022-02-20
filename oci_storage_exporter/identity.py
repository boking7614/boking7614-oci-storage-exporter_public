import oci
import json
import logging, os

logging.basicConfig(format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)
logger.setLevel(logging.WARNING)

config = oci.config.from_file("./config/oci_config")

def list_compartments():
    # https://docs.oracle.com/en-us/iaas/api/#/en/identity/20160918/Compartment/ListCompartments
    identity_client = oci.identity.IdentityClient(config)

    compartments = []
    try:
        list_compartments_response = identity_client.list_compartments(
            compartment_id = config["tenancy"],
            compartment_id_in_subtree = True
        )
        jd = json.loads(str(list_compartments_response.data))
        for info in jd:
            if info["lifecycle_state"] != "DELETED":
                compartments.append({
                    "name":info["name"],
                    "id":info["id"],
                    "timeCreated": info["time_created"]
                })
        logger.info("Get compartment list is success")
        return compartments
        # return jd
    except:
        logger.error('Get compartment list error')

def list_ad():
    # https://docs.oracle.com/en-us/iaas/api/#/en/identity/20160918/AvailabilityDomain/ListAvailabilityDomains
    identity_client = oci.identity.IdentityClient(config)
    ad_name = []
    list_availability_domains_response = identity_client.list_availability_domains(
    compartment_id=config["tenancy"]
    )
    jd = json.loads(str(list_availability_domains_response.data))
    for info in jd:
        ad_name.append(info["name"])
    return ad_name

if __name__ == "__main__":
    # print(os.getcwd())
    print(list_compartments())
    # print(list_ad())
