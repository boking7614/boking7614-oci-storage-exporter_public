from oci.core.models import boot_volume
from prometheus_client import start_http_server, Gauge
from storage import Bucket, Boot, Block
import os, logging, time

# Create logger
logging.basicConfig(format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)

# Metrics
metric_bucket_size = Gauge('bucket_size', 'Approximate total size of all objects in the bucket', ['cptm_name','bucket_name'])
metric_bucket_object_count = Gauge('bucket_object_count', 'Approximate number of objects in the bucket', ['cptm_name','bucket_name'])
metric_boot_volume_size = Gauge('boot_volume_size', 'Boot volume size', ['cptm_name','volume'])
metric_block_volume_size = Gauge('block_volume_size', 'Block volume size', ['cptm_name','volume'])

if __name__ == '__main__':
    start_http_server(8091)
    logger.info("Start OCI Storage exporter server at http://0.0.0.0:8091")

    # 設定 interval預設值,若無抓取到 INTERVAl_TIME此環境變數, interval的值既為10
    if os.environ.get("INTERVAl_TIME") != None:
        interval = int(os.environ['INTERVAl_TIME'])
    else:
        interval = 10

    while True:
        start_time = time.time()
        
        for bk in Bucket.get_list():
            data = Bucket.get_info(bk["name"])
            metric_bucket_size.labels(cptm_name=bk["compartment_name"],bucket_name=data["name"]).set(data["approximate_size"])
            metric_bucket_object_count.labels(cptm_name=bk["compartment_name"],bucket_name=data["name"]).set(data["approximate_count"])
        
        for boot in Boot.get_list():
            boot_name = boot["name"].split(' ')[0]
            metric_boot_volume_size.labels(cptm_name=boot["compartment_name"],volume=(boot_name)).set(boot["size_gb"])

        for block in Block.get_list():
            metric_block_volume_size.labels(cptm_name=block["compartment_name"],volume=(block["name"])).set(block["size_gb"])

        process_time = time.time() - start_time
        logger.info(f"Updated {len(Bucket.get_list()) + len(Boot.get_list()) + len(Block.get_list())} metrics in {process_time:.3f} seconds")

        time.sleep(interval)
