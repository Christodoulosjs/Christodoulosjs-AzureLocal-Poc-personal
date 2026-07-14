from sqs.sqs_client import send_message


message = {
    "event": "vm_created",
    "vm_name": "test-vm",
    "status": "completed",
}

response = send_message(message)
print("Whole Response:", response)
print(response["MessageId"])