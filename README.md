# OCI Storage exporter

#### 建立config目錄

* 在 oci-storage-exporter路徑之下建立 confige目錄，並放入 oci conifg file與 API Keys



#### Docker run

```bash
docker run -d --name oci-storage-exporter \
-p 8091:8091 \
-e INTERVAl_TIME=30 \
oci-storage-exporter:dev
```



**環境變數 :**

``INTERVAl_TIME`` : 取得資料之隔時間 (秒爲單位, default = 10s)


#### OCI IAM 權限設定

1. Create user
    ```bash
    oci iam user create --name <user name> --description "prometheus exporter use"
    ```

2. Create group**
   ```bash
   oci iam group create --name <group name> --description "prometheus exporter use"
   ```
   
3. Add user to group
   ```bash
   oci iam group add-user --user-id <user OCID> --group-id <group OCID>
   ```

4. Setting IAM  Policy

   ```bash
   oci iam policy create \
   --name ExporterPolicy \
   --description "prometheus exporter use" \
   --compartment-id <tenancy id> \
   --statements '["Allow group ExporterGroup to read buckets in tenancy","Allow group ExporterGroup to inspect volume in tenancy"]'
   ```
#### Grafana Dashboard 
![image](https://github.com/boking7614/oci-storage-exporter_public/blob/main/images/image_1.png)
