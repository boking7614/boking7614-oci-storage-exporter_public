from oci.config import from_file
from oci.signer import Signer

def oci_auth():
    config = from_file("./config/oci_config")
    auth = Signer(
        tenancy=config['tenancy'],
        user=config['user'],
        fingerprint=config['fingerprint'],
        private_key_file_location=config['key_file'],
        pass_phrase=config['pass_phrase']
    )
    return auth

if __name__ == "__main__":
    config = from_file("./config/oci_config")
    print(config["tenancy"])