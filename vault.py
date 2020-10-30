# This program is to enable Vault KV access to various KV stores on Vault

import hvac
import os

# Instantiate new Vault CLIENT
client = hvac.Client()
# Capture UNSEAL key we set in Env. Variable
vault_unseal_key = os.getenv('VAULT_UNSEAL_KEY')
# Capture the secret_id and role_id we set in Env. Variable
# vault_client_token = os.environ['VAULT_CLIENT_TOKEN']
vault_secret_id = os.getenv('VAULT_SECRET_ID')
vault_role_id = os.getenv('VAULT_ROLE_ID')
# Define your MOUNT POINT and PATH where your secrets are saved
vault_mount_point = 'kv-v1'
vault_path = '/devnet/dnac/sb1'
meraki_vault_path = '/devnet/meraki/turner'

def vault_auth():
    """
    This function will check if the vault is sealed, unseal it and authenticate against vault
    """
    # Check if vault is sealed
    if client.sys.is_sealed() == True:
        # if the vault is SEALED, UNSEAL IT using the unseal_key
        unseal_response = client.sys.submit_unseal_key(vault_unseal_key)

    # [Uncomment line below only if you want to generate a new API token for the application your ROOT admin registered]
    # Keep in mind you need Application Role ID and Secret ID
    client_data = client.auth_approle(vault_role_id, vault_secret_id)
    # print(client_data['auth']['client_token'])

    # Authenticate against the VAULT using the new CLIENT TOKEN conatained in the new dict object
    client.token = client_data['auth']['client_token']

def vault_r_secret(mount, path):
    """
    This function will read secret from the MOUNT you've created in VAULT and return the secret
    """
    read_secret_result = client.secrets.kv.v1.read_secret(path=vault_path, mount_point=vault_mount_point)
    return read_secret_result

def meraki_vault_r_secret(mount, path):
    """
    This function will read secret from the MOUNT you've created in VAULT and return the secret
    """
    read_secret_result = client.secrets.kv.v1.read_secret(path=meraki_vault_path, mount_point=vault_mount_point)
    api_token = read_secret_result['data']['token']
    return api_token

if __name__ == '__main__':
    vault_auth()
    env_creds = vault_r_secret(vault_mount_point, vault_path)
    print(env_creds['data'])