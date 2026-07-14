from classes.Jobs_class import PollJob
from dal.db import insert_poll_log
import logging

from sqs.sqs_operation_message import create_sqs_message_success

logger = logging.getLogger(__name__)
def set_enable_rdp_job_success(job: PollJob):
    statusInfo= "EnableRDP_Completed"
    insert_poll_log(job.job_id, "Succeeded", statusInfo)
    logger.info(
    "EnableRdp Completed",
    extra={
        "request_id": str(job.request_id),
        "job_id": str(job.job_id),
        },
    )
    sqs_type = "RDPEnabled"
    sendsqsmessage = create_sqs_message_success(job, sqs_type,{"Username": job.vm_name})
