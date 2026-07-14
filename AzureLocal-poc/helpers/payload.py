from classes.Jobs_class import PollJob


def get_payload(job: PollJob):
    payload = {
        "RequestId": job.request_id,
        "VPSId": job.vps_id,
        "MachineId": job.machine_id,
        "JurisdictionId": job.jurisdiction_id,
        "VPSTypeId": job.vps_type_id,
        "CustomerNumber": job.customer_number,
        "VPSNumber": job.vps_number,
    }
    return payload


def get_node_payload(job: PollJob, node_name):
    payload = {
        "RequestId": job.request_id,
        "VPSId": job.vps_id,
        "MachineId": job.machine_id,
        "JurisdictionId": job.jurisdiction_id,
        "VPSTypeId": job.vps_type_id,
        "CustomerNumber": job.customer_number,
        "VPSNumber": job.vps_number,
        "NodeName": node_name,
    }
    return payload


def get_deprovision_payload(job: PollJob):
    payload = {
        "RequestId": job.request_id,
        "MachineId": job.machine_id,
        "CustomerNumber": job.customer_number,
        "VPSNumber": job.vps_number,
    }
    return payload
