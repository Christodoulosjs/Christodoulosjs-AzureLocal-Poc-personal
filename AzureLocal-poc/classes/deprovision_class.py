from dataclasses import dataclass
from uuid import UUID
from datetime import datetime

@dataclass
class DeprovisionJob:
    request_id: UUID
    operation_id: int
    machine_id: UUID
    poller_url: str
    created_at: datetime
    status_info: str
    status: str
    job_id: UUID
    vps_number: int
    customer_number: int