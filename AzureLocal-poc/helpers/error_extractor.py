from dal.db import insert_poll_log

def extract_deep_error_message(data, jobId, status):
    error = data.get("error", {})
    if not error:
        return None

    try:
        details = error.get("details")
        error_code = error.get("code", "Unknown")
        error_message = error.get("message", "No error message returned")
    
        status_info = f"Error: {error_code} - {error_message}"
    
        if details and isinstance(details, list):
            status_info += f" | Nested Error: {details[0]}"
        insert_poll_log(jobId, status, status_info)
        return status_info
    
    except Exception as e:
        raise RuntimeError(f"Failed to extract Azure error details: {e}") from e

