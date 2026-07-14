import requests
from helpers.error_extractor import extract_deep_error_message
from helpers.statushandler import handlestatus
from dal.db import insert_poll_log
from classes.Jobs_class import PollJob
from operations.deprovision import deprovisionResources
from utils.logging import generic_error_context
import logger

def poll_job (job: PollJob, headers)  :
    
    try:
        response = requests.get(job.poller_url, headers=headers)
        print(f"[{job.job_id} HTTP {response.status_code}")
        if not response.text.strip():
            deprovisionResources(job)
            return
        if response.status_code not in (200, 201, 202):
            return

        data = response.json()
        print(f"data: {data}")
        status = data.get("status", "Unknown")
        if status not in ["Succeeded", "Running", "InProgress", "Accepted"]:
            error_message = extract_deep_error_message(data, job.job_id, status)
            raise RuntimeError(
            f"Azure operation failed: {error_message}"
            )
        handlestatus(job, status, data)
    except Exception as e:
        logger.exception(f"failed to poll job",
            extra = generic_error_context(
            e, request_id = str(job.request_id),
            job_id=str(job.job_id),
            operation=job.operation_id,
            ),)