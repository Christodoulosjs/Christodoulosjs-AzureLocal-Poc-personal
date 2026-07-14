from classes.Jobs_class import PollJob
from dal.db import insert_poll_log, get_latest_status_info
from helpers.payload import get_deprovision_payload
from helpers.request_url import craft_listener_url
from classes.deprovision_class import DeprovisionJob
from sqs.sqs_operation_message import create_sqs_message_success
from utils.logging import generic_error_context
import logging 

logger = logging.getLogger(__name__)
def set_deprovision_job_success(job: PollJob):
    
    statusInfo = "Pending_Deprovision"    
    insert_poll_log(job.job_id, "Succeeded", statusInfo) #Get latestStatus from DB and then if Pending_Deprovision then trigger DeprovisionVm and then DeprovisionNic.
    sqs_type = "DeprovisionBegin",
    sendsqsmessage = create_sqs_message_success(job, sqs_type)

def startDeprovisionVm(depr: DeprovisionJob):  
   try:
        payload = get_deprovision_payload(depr)
        endpoint = "deprovisionvm"
        deprovisionVm = craft_listener_url(depr, payload, endpoint)
        insert_poll_log(depr.job_id, "Running", "Deprovision_In_Progress")
   except Exception as e:
        logger.exception("Failed to deprovision after 7 days completed",
                         extra=generic_error_context(e, request_id = str(depr.request_id), job_id = str(depr.job_id)))
        raise

def deprovisionResources(job: PollJob):                                                         
    try:
            payload = get_deprovision_payload(job)                                                     
            latest_status_info = get_latest_status_info(job.request_id)
            match latest_status_info:
                case "Deprovision_In_Progress":
                    statusInfo = "Nic_Deprovision_In_Progress"
                    endpoint = "deprovisionnic"
                    deprovisionNic = craft_listener_url(job, payload, endpoint)
                    insert_poll_log(job.job_id, "Succeeded", statusInfo)
                    
                case "Nic_Deprovision_In_Progress":
                    statusInfo = "Rcg_Deprovision_In_Progress"
                    endpoint = "deprovisionrcg"
                    deprovisionRcg = craft_listener_url(job, payload, endpoint)
                    insert_poll_log(job.job_id, "Succeeded", statusInfo)            

                case "Rcg_Deprovision_In_Progress":
                        statusInfo = "Rcg_Deprovision_Seems_Finished"
                        status = "Succeeded"
                        print("InsertingLog")
                        insert_poll_log(job.job_id, status, statusInfo)
                        sqs_type = "DeprovisionFinallyTerminated",
                        sendsqsmessage = create_sqs_message_success(job, sqs_type)
                        return {
                        "status": "Succeeded",
                        "requestId": job.request_id,
                        "operationId": job.operation_ids
                    } #Send AWS Message that Deprovision is Completed
                    
                case _:
                    raise ValueError(f"Unexpected status info: {latest_status_info}")
    except Exception as e:
        logger.exception("Failed to handle deprovision poll job",
                         extra=generic_error_context(e, request_id = str(job.request_id), job_id = str(job.job_id)))