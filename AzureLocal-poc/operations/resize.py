from dal.db import insert_poll_log
from helpers.payload import get_node_payload
from helpers.urlHelper import url_parser
from helpers.cleanNodeName import get_node_name
import requests
from classes.Jobs_class import PollJob
from sqs.sqs_operation_message import create_sqs_message_success
from utils.logging import generic_error_context
import logging

logger = logging.getLogger(__name__)

def handleResize(job: PollJob, data):
    try:
        properties = data.get("properties") or {}
        run_command_name = properties.get("name", "")
        match run_command_name:
            case "":
                logger.info(
                    "CPU and RAM resize completed, triggering node disk expansion",
                    extra={
                        "request_id": str(job.request_id),
                        "job_id": str(job.job_id),
                    },
                )
                statusInfo = "ResizedCpuAndRam"
                node_name = get_node_name(data)
                payload = get_node_payload(job, node_name)
                response = requests.post("http://127.0.0.1:8000/expandnode", json=payload)
                if response.status_code not in (200, 202):
                    raise RuntimeError(f"Expand node disk size request failed", f"({response.status_code}): {response.text}")
                insert_poll_log(job.job_id, "Succeeded", statusInfo)
                return
            case resource if resource.startswith("expand-disk-node"):
                statusInfo = "DiskExpandedFromNode_AwaitingPartitionExpand"
                node_name = get_node_name(data) 
                payload = get_node_payload(job, node_name)
                response = requests.post("http://127.0.0.1:8000/expandpartition", json=payload)
                if response.status_code not in (200, 202):
                    raise RuntimeError(f"Expand partition request failed, ({response.status_code}): {response.text}")
                insert_poll_log(job.job_id, "Succeeded", statusInfo)
                return
            case resource if resource.startswith("expand-partition-vm"):
                statusInfo = "PartitionOnVPSExpanded"
                node_name = get_node_name(data)
                payload = get_node_payload(job, node_name) #info log here
                logger.info(
                    "Resize completed! Sending Aws Message",
                    extra={
                        "request_id": str(job.request_id),
                        "job_id": str(job.job_id),
                    },
                )
                sqs_type = "completeResize"
                sendsqsmessage = create_sqs_message_success(job, sqs_type,{"VPSType": job.vps_type_id}) #Check if new vps_type_id is updated in database(Vps Table)
                #HERE WE SHOULD SEND THE AWS MESSAGE IMO WE HAVE EXPANDED THE PARTITION EVERYTHING IS DONE!
            case _:
                raise ValueError(
                f"Unknown run command name: {run_command_name}")
    except Exception as e:
        logger.exception("Failed to handle resize poll job",
                     extra=generic_error_context(e, request_id = str(job.request_id), job_id = str(job.job_id)))
        raise