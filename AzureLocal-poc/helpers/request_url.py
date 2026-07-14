import requests
from requests.exceptions import RequestException
from classes.job_protocol import JobContext
from helpers.auth_for_listener import get_poller_headers
import logging
from utils.logging import generic_error_context

logger= logging.getLogger(__name__)

def craft_listener_url(job: JobContext, payload, endpoint):
    headers = get_poller_headers()
    
    try:        
        response = requests.post(f"http://127.0.0.1:8000/{endpoint}", headers=headers, json=payload)
        if response.status_code not in (200, 202):
            print(f"Calling {endpoint} Failed! :", response.status_code, response.text)
            raise RuntimeError(
                f"Listener endpoint {endpoint} returned "
                f"{response.status_code}: {response.text}"
            )
        logger.info(
            "Listener endpoint invoked successfully",
            extra={
                "request_id": job.request_id,
                "job_id": job.job_id,
                "endpoint": endpoint,
                "status_code": response.status_code,
            },)
    except RequestException as e:
        logger.exception(
            "Unexpected error while calling listener endpoint",
            extra={
                "request_id": job.request_id,
                "job_id": job.job_id,
                "endpoint": endpoint,
                "error_type": type(e).__name__,
                "error_message": str(e),
            },
        )
        raise
    except Exception as e:
       logger.exception(
        "Unexpected error while calling listener endpoint",
        extra=generic_error_context(
            e,
            job.request_id,
            job.job_id,
            endpoint=endpoint,
            ),
        )
       raise