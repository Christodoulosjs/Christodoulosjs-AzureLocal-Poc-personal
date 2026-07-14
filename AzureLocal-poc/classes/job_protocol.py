from typing import Protocol
from uuid import UUID


class JobContext(Protocol):
    request_id: UUID
    job_id: UUID