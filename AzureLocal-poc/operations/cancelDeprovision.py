from dal.db import insert_poll_log
import logging

from sqs.sqs_operation_message import create_sqs_message_success

logger = logging.getLogger(__name__)

def set_cancel_deprovision_job_success(job):
    statusInfo = "Cancel_Deprovision"
    insert_poll_log(job.job_id, "Succeeded", statusInfo)
    logger.info(
    "CancelDeprovision Completed",
    extra={
        "request_id": str(job.request_id),
        "job_id": str(job.job_id),
        },
    )
    sqs_type = "DeprovisionTurnedOff"
    sendsqsmessage = create_sqs_message_success(job, sqs_type)
