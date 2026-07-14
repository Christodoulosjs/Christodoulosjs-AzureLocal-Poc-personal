import logging
from azure.monitor.opentelemetry import configure_azure_monitor
from config.settings import settings

logger = logging.getLogger(__name__)
def configure_monitoring():
    # Application logs
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s %(levelname)s %(name)s %(message)s",
    )

    # Silence Azure SDK internals
    logging.getLogger("azure").setLevel(logging.WARNING)
    logging.getLogger("azure.core.pipeline.policies.http_logging_policy").setLevel(logging.WARNING)
    logging.getLogger("azure.monitor.opentelemetry").setLevel(logging.WARNING)

    try:
            configure_azure_monitor(
                connection_string=settings.application_insights_connection_string,
            )
            logger.info("Application Insights monitoring configured")
    
    except Exception as e:
            logger.exception(
                "Failed to configure Application Insights monitoring",
                extra={
                    "operation": "configure_monitoring",
                    "error_type": type(e).__name__,
                    "error_message": str(e),
                },
            )