from uuid import UUID
from pydantic import BaseModel

class ItemResponse(BaseModel):
    requestId: UUID
    description: str

    def __str__(self):
        return (
            f"ItemResponse("
            f"requestId={self.requestId}, "
            f"description={self.description})"
        )

    def __repr__(self):
        return str(self)
