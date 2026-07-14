import boto3
from botocore.exceptions import BotoCoreError, ClientError
from config.settings import settings
import json
import logging

from dal.db import PollJob 

logger = logging.getLogger(__name__)

def get_sqs_client():
    try:
        return boto3.client(
            "sqs",
            region_name=settings.aws_region,
            aws_access_key_id=settings.aws_access_key_id,
            aws_secret_access_key=settings.aws_secret_access_key,
        )
    except (BotoCoreError, ClientError) as e:
        raise RuntimeError(f"Failed to create SQS client: {e}") from e

def send_message(message: dict, job:PollJob):
    try:
        client = get_sqs_client()

        response = client.send_message(
            QueueUrl=settings.sqs_queue_url,
            MessageBody=json.dumps(message),
        )
        logger.info(
        "SQS message sent successfully",
        extra={
            "request_id": job.request_id,
            "job_id": job.job_id,
            "machine_id": job.machine_id,
            "message_type": message.get("$type"),
            "message_id": response.get("MessageId"),
            },
        )
        return response

    except (ClientError, BotoCoreError) as e:
        logger.exception(
            "Failed to send SQS message",
            extra={
                "request_id": job.request_id,
                "job_id": job.job_id,
                "machine_id": job.machine_id,
                "queue_url": settings.sqs_queue_url,
                "message_type": message.get("$type"),
                "error_type": type(e).__name__,
                "error_message": str(e),
            },
        )
        raise