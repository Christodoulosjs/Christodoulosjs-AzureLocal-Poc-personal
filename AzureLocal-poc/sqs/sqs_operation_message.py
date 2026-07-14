from classes.Jobs_class import PollJob
from sqs.sqs_client import send_message

def create_sqs_message_success(job: PollJob, sqs_type: str, extra_data: dict | None = None):
    
    message = {
        "$type": f"{sqs_type}",
        "Status": "1",
        "Uuid": f"{job.machine_id}",
    }
    
    if extra_data:
        message.update(extra_data)

    response = send_message(message, job)
    print("Whole Response:", response)
    print(response["MessageId"])
    return response

def create_sqs_message_failed(job: PollJob, sqs_type: str, extra_data: dict | None = None):
    
    message = {
        "$type": f"{sqs_type}",
        "Status": "2",
        "Uuid": f"{job.machine_id}",
    }
    
    if extra_data:
        message.update(extra_data)

    response = send_message(message, job)
    print("Whole Response:", response)
    print(response["MessageId"])
    return response