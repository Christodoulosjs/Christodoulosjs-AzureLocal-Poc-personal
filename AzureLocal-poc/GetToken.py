import requests
import time
import uuid
from azure.identity import DefaultAzureCredential

subscription_id = "41d3de0e-17f5-488a-879e-734c97c01c15"
resource_group = "hci-we-dev-rg"
machine_name = "HCINODE02"
def extract_job_id(response_json):

    full_id = response_json.get("id", "")

    if not full_id:
        return None

    # Split by "/" and take last segment
    last_segment = full_id.split("/")[-1]

    # Remove prefix "checkhealth-"
    job_id = last_segment.replace("checkhealth-", "")

    return job_id
credential = DefaultAzureCredential()
token = credential.get_token("https://management.azure.com/.default").token
print ("Token:", token)
