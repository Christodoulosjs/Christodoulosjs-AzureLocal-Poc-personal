from constants.statuses import DEPROVISION_IN_PROGRESS_STATUSES
from classes.Jobs_class import PollJob
from dal.db import get_latest_status_info, insert_poll_log
from operations import provision , resize, deprovision, restart, resetPassword, enableRDP, cancelDeprovision
from utils.logging import generic_error_context 
import logging 

logger = logging.getLogger(__name__)
def handle_job_completion(job: PollJob, data):
    try:        
        match job.operation_id :
            case 1:
                print("Determine Provision stage")
                provision.handleProvision(job, data)
            case 2:
                print("Determine Resize stage")
                resize.handleResize(job, data)
            case 3:
                print("Restart(One stage Operation)")
                restart.set_restart_job_success(job)
            case 4:
                print("ResetPassword(One stage operation)")
                resetPassword.set_reset_password_job_success(job)
            case 6:
                latest_status = get_latest_status_info(job.request_id)
                if latest_status in DEPROVISION_IN_PROGRESS_STATUSES: # have to check that shutdown doesnt take status or status is included in expected deprovisions
                    deprovision.deprovisionResources(job)
                else :
                    print("Determine deprovision(multistep stage)")
                    deprovision.set_deprovision_job_success(job) #NotCompleted yet
            case 7:
                print("EnableRDP(Onestep Process)")
                enableRDP.set_enable_rdp_job_success(job)
            case 8:
                print("CancelDeprovision(Onestep Process)")
                cancelDeprovision.set_cancel_deprovision_job_success(job)
            case _:
                raise ValueError(f"Unknown operation_id: {job.operation_id}")
    except Exception as e:
        logger.exception("Failed to handle operation_id",
                         extra=generic_error_context(e, request_id = str(job.request_id), job_id = str(job.job_id),
                         ),
        )
        raise
