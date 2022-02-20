from contextlib import nullcontext
import json
from oci.core.models import boot_volume
from oci.object_storage.models import bucket
import requests
import logging
import oci
from identity import list_compartments, list_ad

logging.basicConfig(format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)
logger.setLevel(logging.WARNING)

config = oci.config.from_file("./config/oci_config")

class Bucket:
    def get_list():
        # 帶入Tenancy ID取得此Tenancy Bucket清單
        # https://docs.oracle.com/en-us/iaas/api/#/en/objectstorage/20160918/Bucket/ListBuckets
        object_storage_client = oci.object_storage.ObjectStorageClient(config)
        try:
            buckets = []
            compartments = list_compartments()
            for compartment in compartments:
                list_buckets_response = object_storage_client.list_buckets(
                    namespace_name = "nrufhfzjnyx3",
                    compartment_id = compartment["id"]
                )
                jd = json.loads(str(list_buckets_response.data))
                
                for info in jd:
                    buckets.append({
                        "name": info["name"],
                        "compartment_name": compartment["name"],
                        "created_time": info["time_created"]
                    })
            return buckets
        except: 
            logger.error(f'Get "{compartment["id"]}" bucket error')

    def get_info(bucketname):
        # 帶入各 Bucket Name取得各 Bucket詳細資訊
        # https://docs.oracle.com/en-us/iaas/api/#/en/objectstorage/20160918/Bucket/GetBucket
        object_storage_client = oci.object_storage.ObjectStorageClient(config)
        try:
            get_bucket_response = object_storage_client.get_bucket(
                namespace_name = "nrufhfzjnyx3",
                bucket_name = bucketname,
                fields = ["approximateSize","approximateCount"]
                )
            jd = json.loads(str(get_bucket_response.data))
            logger.info(f'Get "{bucketname}" bucket info is success')
            return jd
        except:
            logger.error(f'Get "{bucketname}" bucket info Error')


class Boot:
    def get_list():
        # 帶入Tenancy ID取得此Tenancy Boot volume清單
        # https://docs.oracle.com/en-us/iaas/api/#/en/iaas/20160918/BootVolume/ListBootVolumes
        core_client = oci.core.BlockstorageClient(config)
        try:
            boot_list = []
            compartments = list_compartments()
            ads = list_ad()

            for compartment in compartments:
                for ad in ads:
                    boot_volume = core_client.list_boot_volumes(
                        availability_domain = ad,
                        compartment_id = compartment["id"]
                    )

                    jd = json.loads(str(boot_volume.data))
                    for info in jd:
                        boot_list.append({
                            "compartment_name": compartment["name"],
                            "name": info["display_name"],
                            "size_gb": info["size_in_gbs"],
                            "state": info["lifecycle_state"],
                            "availability_domain": ad,
                            "created_time": info["time_created"]
                        })
            return (boot_list)
        except:
            logger.error(f'Get "{compartment["name"]}" boot_volume info Error')

class Block:
    def get_list():
        core_client = oci.core.BlockstorageClient(config)
        try:
            block_list = []
            compartments = list_compartments()
            ads = list_ad()
            for compartment in compartments:
                for ad in ads:
                    list_volumes_response = core_client.list_volumes(
                        availability_domain=ad,
                        compartment_id= compartment["id"]
                        )
                    jd = json.loads(str(list_volumes_response.data))
                    for info in jd:
                        block_list.append({
                            "compartment_name": compartment["name"],
                            "name": info["display_name"],
                            "ad": info["availability_domain"],
                            "size_gb": info["size_in_gbs"],
                            "state": info["lifecycle_state"],
                            "availability_domain": ad,
                            "created_time": info["time_created"]
                        })
            return block_list
        except:
            logger.error(f'Get "{compartment["id"]}" boot_volume info Error')            

if __name__ == "__main__":
    import time

    start_time = time.time()

    print(Block.get_list())
    # for i in block.get_list():
        # volume_name = (i["name"].split(' '))[0]
        # print(volume_name)
        # print(i)
    end_time = time.time()
    print(end_time - start_time)