from pydantic import BaseModel
from typing import Optional

class CustomerPayload(BaseModel):
    CustomerNumber: Optional[int] = None
    VPStype: Optional[int] = None
    Juristriction: Optional[int] = None
    Operation: str
    Uuid: str

    def __str__(self):
        return (
            f"CustomerPayload("
            f"CustomerNumber={self.CustomerNumber}, "
            f"VPSTypeId={self.VPStype}, "
            f"JurisdictionId={self.Juristriction}, "
            f"Operation={self.Operation}, "            
            f"MachineId={self.Uuid})"
        )
    def __repr__(self):
        return str(self)