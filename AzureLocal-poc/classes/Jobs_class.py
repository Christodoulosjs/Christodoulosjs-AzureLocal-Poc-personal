from dataclasses import dataclass
from uuid import UUID

@dataclass
class PollJob:
    job_id: UUID
    request_id: UUID
    azure_job_id: UUID
    vps_id: UUID
    machine_id: UUID
    poller_url: str
    operation_id: int
    customer_number: int
    vps_number: int
    jurisdiction_id: int
    vps_type_id: int
    public_ip : str
    mac_address : str 
    port : str

    @property
    def resource_group(self):
        return f"{self.customer_number}-{self.vps_number}-rg"
    
    @property
    def nic_name(self):
        return f"{self.customer_number}-{self.vps_number}-nic"
    
    @property
    def vm_name(self):
        return f"{self.customer_number}-{self.vps_number}"