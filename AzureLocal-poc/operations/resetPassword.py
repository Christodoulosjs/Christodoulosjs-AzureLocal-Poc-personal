from classes.Jobs_class import PollJob
from dal.db import insert_poll_log
import logging

from helpers.get_keyvault_secret import get_secret
from sqs.sqs_operation_message import create_sqs_message_success

logger = logging.getLogger(__name__)

def set_reset_password_job_success(job: PollJob):
    statusInfo= "ResetPassword_Completed"
    insert_poll_log(job.job_id, "Succeeded", statusInfo)
    logger.info(
    "ResetPassword Completed",
    extra={
        "request_id": str(job.request_id),
        "job_id": str(job.job_id),
        },
    )
    password = get_secret(f"{job.vm_name}")
    sqs_type = "completeResetPassword"
    sendsqsmessage = create_sqs_message_success(job, sqs_type,{"Password": password})