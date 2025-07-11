import os
from azure.identity import DefaultAzureCredential
from azure.keyvault.secrets import SecretClient
import logging

#delete in production
#from dotenv import load_dotenv
#load_dotenv()

key_vault_uri=os.getenv("KEYVAULT_URI")

#auth
credential=DefaultAzureCredential()
client=SecretClient(vault_url=key_vault_uri, credential=credential)

#method that request secret

def get_secret(name_secret)->str:
    try:
        return client.get_secret(name=name_secret).value
    except Exception as ex:
        logging.error("ERROR GET SECRET {%s}", ex)

