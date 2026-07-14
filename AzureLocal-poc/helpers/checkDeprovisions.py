from dal.db import checkForPendingDeprovisions
from operations.deprovision import startDeprovisionVm
import logging

logger = logging.getLogger(__name__)
def check_deprovisions () :
    try:
         logger.info(
            "Checking for pending deprovisions",
            extra={"operation": "check_deprovisions",},)
         deprovisions = checkForPendingDeprovisions()
         print(deprovisions)
        
         if not deprovisions:
            logger.info("No pending deprovisions", extra = {
                "operation": "check_deprovisions",
                },)
            return
         logger.info(
         "Pending deprovisions found",
         extra={
             "operation": "check_deprovisions",
             "count": len(deprovisions),
         },)        
         for depr in deprovisions:
             startDeprovisionVm(depr)
    except Exception as e:
        logger.exception(
        "Failed when checking pending deprovisions",
        extra = {
            "operation": "check_deprovisions",
            "error_type": type(e).__name__,
            "error_message": str(e),
            },
        )
        raise
