from azure.core.exceptions import ClientAuthenticationError
from azure.identity import ClientSecretCredential
from config.settings import settings
import logging

logger = logging.getLogger(__name__)
credential = ClientSecretCredential(
    tenant_id=settings.tenant_id,
    client_id=settings.poller_client_id,
    client_secret=settings.poller_client_secret,
)


def get_poller_headers():
    try:
        access_token = credential.get_token(
            f"{settings.listener_api_audience}/.default"
        )

        return {
            "Authorization": f"Bearer {access_token.token}"
        }

    except ClientAuthenticationError as e:
        logger.exception(
            "Failed to acquire Azure access token",
            extra={
                "operation": "get_auth_token",
                "error_type": type(e).__name__,
                "error_message": str(e),
            },
        )
        raise

    except Exception as e:
        logger.exception(
            "Unexpected error while acquiring Azure access token",
            extra={
                "operation": "get_auth_token",
                "error_type": type(e).__name__,
                "error_message": str(e),
            },
        )
        raise