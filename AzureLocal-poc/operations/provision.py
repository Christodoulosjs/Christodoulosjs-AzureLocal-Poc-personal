from classes.Jobs_class import PollJob
from dal.db import insert_poll_log, registerNodeToVPS
from helpers.cleanNodeName import get_node_name
from helpers.get_keyvault_secret import get_secret
from helpers.payload import get_node_payload, get_payload
from helpers.request_url import craft_listener_url
from helpers.urlHelper import url_parser
import json
from operations.healthCheck import nodeAndVolumeHandler
import requests
import logging
from sqs.sqs_operation_message import create_sqs_message_success
from utils.logging import generic_error_context

logger = logging.getLogger(__name__)

def handleProvision(job: PollJob, data):
    try:
        logger.info("Handling provision poll job",
                    extra={
                        "request_id": str(job.request_id),
                        "job_id": str(job.job_id)
                        },
                    )
        if "/deployments/" in job.poller_url: #Deployments will only be Vm Provision Or NicProvision!!!
            resource_name = job.poller_url.split("/deployments/", 1)[1].split("/operationStatuses/", 1)[0]
            match resource_name:
                case resource if resource.startswith("deploy-nic"):
                    statusInfo = "NIC_Provisioned"
                    payload = get_payload(job)
                    craft_listener_url(job, payload, "provisionvm")
                    insert_poll_log(job.job_id, "Succeeded", statusInfo)
                    return 
                case resource if resource.startswith("deploy-vm"):
                    statusInfo = "VPSProvisioned_AwaitingNodeDetection"
                    payload = get_payload(job)
                    #executeapicall
                    craft_listener_url(job, payload, "detectnode")
                    insert_poll_log(job.job_id, "Succeeded", statusInfo)
                    return 
                case _:
                    raise ValueError (f"Unknown resource name: {resource_name}")
    
        else :
            path = url_parser(job.poller_url) #Not Needed (I think) but we can use it to get the resource azurejobid from url)
            properties = data.get("properties") or {}
            run_command_name = properties.get("name", "")
            print(f"Run Command Name: {run_command_name}")
            if run_command_name.startswith("checkhealth"):
                health_output=data["properties"]["properties"]["instanceView"]["output"]
                health_result = json.loads(health_output)
                handleNodesAndVolumes = nodeAndVolumeHandler(health_result, job)
                payload=get_payload(job)
                craft_listener_url(job, payload, "provisionnic")
                insert_poll_log(job.job_id, "Succeeded", "HealthCheckCompleted")
                return  
            
            match run_command_name:
                case resource if resource.startswith("find-hosting-node"):
                    statusInfo = "ParentNodeHasBeenDetected"
                    node_name = get_node_name(data)
                    print("We have found the hosting node", node_name)
                    registerNodeToVPS(node_name, job.machine_id)
                    payload = get_node_payload(job, node_name)
                    craft_listener_url(job, payload, "expandnode")
                    insert_poll_log(job.job_id, "Succeeded", statusInfo)
                                
                case resource if resource.startswith("expand-disk-node"):
                    statusInfo = "DiskExpandedFromNode_AwaitingPartitionExpand"
                    node_name = get_node_name(data)
                    payload = get_node_payload(job, node_name)
                    craft_listener_url(job, payload, "expandpartition")
                    insert_poll_log(job.job_id, "Succeeded", statusInfo)
  
                case resource if resource.startswith("expand-partition-vm"):
                    statusInfo = "PartitionOnVPSExpanded"
                    insert_poll_log(job.job_id, "Succeeded", statusInfo)
                    password = get_secret(f"{job.vm_name}")
                    sqs_type = "completeProvisioning"
                    sendsqsmessage = create_sqs_message_success(job, sqs_type,{"Ip": f"{job.public_ip}:{job.port}","Password": password, "ServerLocation": "New York", "Username": job.vm_name})
                    return
                case _:
                    raise ValueError(f"Unknown run command name: {run_command_name}")
    except Exception as e:
        logger.exception("Failed to handle provision poll job",
                         extra=generic_error_context(e, request_id = str(job.request_id), job_id = str(job.job_id),
                         ),
        )
        raise
