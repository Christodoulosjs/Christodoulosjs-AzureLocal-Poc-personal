from typing import Any


def generic_error_context(exception: Exception, request_id: str, job_id: str, **kwargs: Any) -> dict:
    return {
        "request_id": request_id,
        "job_id": job_id,
        "error_type": type(exception).__name__,
        "error_message": str(exception),
        **kwargs,
    }
#Only generic_error_context is used!

def azure_node_error_context(
    exception: Exception,
    request_id: str,
    job_id: str,
    node_name: str,
    **kwargs: Any,
) -> dict:
    azure_error = getattr(exception, "error", None)

    return {
        "request_id": request_id,
        "job_id": job_id,
        "azure_error_code": getattr(azure_error, "code", None),
        "azure_error_message": getattr(exception, "message", str(exception)),
        "resource_type": f"node, {node_name}",
        **kwargs,
    }


def azure_vm_error_context(
    exception: Exception,
    request_id: str,
    job_id: str,
    vm_name: str,
    **kwargs: Any,
) -> dict:
    azure_error = getattr(exception, "error", None)

    return {
        "request_id": request_id,
        "job_id": job_id,
        "azure_error_code": getattr(azure_error, "code", None),
        "azure_error_message": getattr(exception, "message", str(exception)),
        "resource_type": f"virtual_machine, {vm_name}",
        **kwargs,
    }