from classes.Jobs_class import PollJob
from dal.db import update_health_check
import json 
import logging

from utils.logging import generic_error_context

logger = logging.getLogger(__name__)
def nodeAndVolumeHandler(health_result, job:PollJob) :
    try:
        volume_summary = []
        for volume in health_result.get("Volumes", []):
        
            if volume["FriendlyName"] == "Infrastructure_1":
                continue
        
            volume_summary.append({
                "name": volume["FriendlyName"],
                "health_status": volume["HealthStatus"],
                "operational_status": volume["OperationalStatus"],
                "size_bytes": volume["Size"],
                "available_bytes": volume["SizeRemaining"]
            })
            
        node_summary = []
        
        for node in health_result.get("ClusterNodes", []):
        
            state = "Up" if node["State"] == 0 else "Down"
        
            node_summary.append({
                "name": node["Name"],
                "state_code": node["State"],
                "status": state
            })
        health_summary = {
            "volumes": volume_summary,
            "nodes": node_summary
        }
        update_health_check(volume_summary, node_summary)
        logger.info(
    "HealthChecks Completed. Continuing with nic creation",
    extra={
        "request_id": str(job.request_id),
        "job_id": str(job.job_id),
        "health_summary": health_summary,
    },
)
        return 
    except Exception as e:
        logger.exception("Failed to handle provision poll job",
                         extra=generic_error_context(e, request_id = str(job.request_id), job_id = str(job.job_id),
                         ),
        )
        raise
