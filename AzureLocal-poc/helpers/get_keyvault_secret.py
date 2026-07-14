from azure.core.exceptions import HttpResponseError, ResourceNotFoundError
from azure.identity import DefaultAzureCredential
from azure.keyvault.secrets import SecretClient
from config.settings import settings

credential = DefaultAzureCredential()

client = SecretClient(vault_url=settings.keyvault_url,credential=credential,)



def get_secret(name: str) -> str:
    try:
        return client.get_secret(name).value
    except ResourceNotFoundError:
        raise ValueError(f"Secret '{name}' was not found in Key Vault")
    except HttpResponseError as e:
        raise RuntimeError(f"Failed retrieving secret '{name}': {e.message}")