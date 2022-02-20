from oci.core.models import boot_volume
from identity import list_compartments
from storage import Bucket, Boot, Block
from rich.console import Console
from rich.table import Column, Table
from rich.progress import track
from rich import inspect

console = Console()

bucket_table = Table(show_header=True, header_style="bold magenta")
bucket_table.add_column("Compartment Name")
bucket_table.add_column("Bucket")
bucket_table.add_column("Total Size")
bucket_table.add_column("Object Count")
bucket_table.add_column("Created Time (UTC)", style="dim")

compartments_table = Table(show_header=True, header_style="bold magenta")
compartments_table.add_column("Compartment Name")
compartments_table.add_column("Compartment OCID")
compartments_table.add_column("Created Time (UTC)", style="dim")

boot_table = Table(show_header=True, header_style="bold magenta")
boot_table.add_column("Compartment Name")
boot_table.add_column("Boot_volume")
boot_table.add_column("Size(GB)")
boot_table.add_column("State")
boot_table.add_column("Availability Domain")
boot_table.add_column("Created Time (UTC)", style="dim")

block_table = Table(show_header=True, header_style="bold magenta")
block_table.add_column("Compartment Name")
block_table.add_column("Block_volume")
block_table.add_column("Availability domain")
block_table.add_column("Size(GB)")
block_table.add_column("State")
block_table.add_column("Availability Domain")
block_table.add_column("Created Time (UTC)", style="dim")

compartments = list_compartments()

for i in track(compartments, description="Get Compartments info..."):

    compartments_table.add_row(i["name"], i["id"], i["timeCreated"])

console.print(compartments_table)

bk_list = Bucket.get_list()

for bk in track(bk_list, description="Get bucket info..."):
    info = Bucket.get_info(bk["name"])
    bucket_table.add_row(bk["compartment_name"],info["name"],str(info["approximate_size"] / 1048576) + " MiB",str(info["approximate_count"]), info["time_created"])

console.print(bucket_table)

boot_list = Boot.get_list()

for boot in track(boot_list, description="Get boot volume info..."):
    boot_table.add_row(boot["compartment_name"],boot["name"],str(boot["size_gb"]),boot["state"],boot["availability_domain"],boot["created_time"])

console.print(boot_table)

block_list = Block.get_list()

for block in track(block_list, description="Get block volume info..."):
    block_table.add_row(block["compartment_name"],block["name"],block["ad"],str(block["size_gb"]),block["state"],block["availability_domain"],block["created_time"])

console.print(block_table)