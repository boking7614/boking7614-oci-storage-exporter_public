import asyncio
from asyncio import tasks
import aiohttp
import time
from compartment import list_compartments
from storage import Boot
import oci, json

async def get_buck_list(compartment_id):
    object_storage_client = oci.object_storage.ObjectStorageClient(oci.config.from_file())
    list_buckets_response = object_storage_client.list_buckets(
        namespace_name = "nrufhfzjnyx3",
        compartment_id = compartment_id
    )
    jd = json.loads(str(list_buckets_response.data))
    # await asyncio.sleep(1)
    return jd

async def main():
    tasks = []
    for i in list_compartments():
        tasks.append(get_buck_list(i["id"]))

    results = await asyncio.gather(*tasks)
    for result in results:
        print(result)



start_time = time.time()

asyncio.run(main())

end_time = time.time()

print(end_time - start_time)