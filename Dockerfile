FROM ubuntu:20.04
LABEL type="oci-exporter"

ARG DEBIAN_FRONTEND=noninteractive

RUN apt-get update && apt-get install -y python3.9-dev python3-pip && apt-get clean
COPY oci_storage_exporter/ /opt/oci_storage_exporter
RUN pip install --no-cache-dir -r /opt/oci_storage_exporter/requirements.txt


EXPOSE 8091

WORKDIR /opt/oci_storage_exporter

CMD ["python3","exporter.py"]