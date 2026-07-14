from classes.Jobs_class import PollJob
from dal.db import insert_poll_log
from helpers.determine_request import handle_job_completion
import logging

from sqs.sqs_operation_message import create_sqs_message_failed
from sqs.sqs_opeation_types import get_sqs_type

logger = logging.getLogger(__name__)
def handlestatus(job: PollJob, status, data):
    if status in ["Running", "InProgress", "Accepted"]:
        print(f"Status is: '{status}'! Job hasnt finished yet")
        statusInfo = "InProgress"
        insert_poll_log(job.job_id, status, statusInfo)
        return
    elif status == "Succeeded":
        statusInfo = "Succeeded"
        job_handler = handle_job_completion(job, data)
    
    else:
        logger.error(
            "Azure operation failed",
            extra={
                "request_id": str(job.request_id),
                "job_id": str(job.job_id),
                "azure_status": status,
                "operation": "handle_status",
            },
        )
        sqs_type = get_sqs_type(job.operation_id)
        sendsqsmessage = create_sqs_message_failed(job, sqs_type)

        job.status = "Failed"
        job.message = f"Job failed with status: {status}."