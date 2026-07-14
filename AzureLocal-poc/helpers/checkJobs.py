from dal.db import get_running_jobs
from helpers.auth import get_auth_headers
from helpers.job_polling import poll_job
import logging

logger = logging.getLogger(__name__)
def check_jobs():
    headers = get_auth_headers()
    jobs = get_running_jobs()

    for job in jobs:
        try:
            poll_job(job, headers)
        except Exception as e:
            logger.exception(f"Polling failed for {job.job_id}: {e}")
