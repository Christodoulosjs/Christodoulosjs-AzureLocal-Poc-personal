from azure.identity import DefaultAzureCredential
from azure.core.exceptions import ClientAuthenticationError

def get_auth_headers():
    try:
        credential = DefaultAzureCredential()
        token = credential.get_token("https://management.azure.com/.default").token
        headers = {"Authorization": f"Bearer {token}", "Content-Type": "application/json"}
        return headers
    except ClientAuthenticationError as e:
        raise RuntimeError(f"Azure authentication failed: {e}") from e
    except Exception as e:
        raise RuntimeError(f"Unexpected error while getting auth headers: {e}") from e