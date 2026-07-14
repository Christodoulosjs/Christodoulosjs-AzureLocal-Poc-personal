from pydantic import BaseModel

class ProvisionVmPayload(BaseModel):
    RequestId: str
    VPSId: str 
    MachineId: str
    JurisdictionId: int
    VPSTypeId: int
    CustomerNumber: str
    VPSNumber: int
    def __str__(self):
        return (
            f"ProvisionVmPayload("
            f"RequestId={self.RequestId}, "
            f"VPSId={self.VPSId}, "
            f"MachineId={self.MachineId}, "
            f"JurisdictionId={self.JurisdictionId}, "
            f"VPSTypeId={self.VPSTypeId}, "
            f"CustomerNumber={self.CustomerNumber}, "
            f"VPSNumber={self.VPSNumber})"
        )

    def __repr__(self):
        return (
            f"ProvisionVmPayload("
            f"RequestId={self.RequestId!r}, "
            f"VPSId={self.VPSId!r}, "
            f"MachineId={self.MachineId!r}, "
            f"JurisdictionId={self.JurisdictionId!r}, "
            f"VPSTypeId={self.VPSTypeId!r}, "
            f"CustomerNumber={self.CustomerNumber!r}, "
            f"VPSNumber={self.VPSNumber!r})"
        )
class ProvisionNicPayload(BaseModel):
    RequestId: str
    VPSId: str
    Uuid: str
    JurisdictionId: int
    VPSTypeId: int
    CustomerNumber: str
    VPSNumber: int
    def __str__(self):
        return (
            f"ProvisionNicPayload("
            f"RequestId={self.RequestId}, "
            f"VPSId={self.VPSId}, "
            f"MachineId={self.Uuid}, "
            f"JurisdictionId={self.JurisdictionId}, "
            f"VPSTypeId={self.VPSTypeId}, "
            f"CustomerNumber={self.CustomerNumber}, "
            f"VPSNumber={self.VPSNumber})"
        )
    def __repr__(self):
        return (
            f"ProvisionNicPayload("
            f"RequestId={self.RequestId!r}, "
            f"VPSId={self.VPSId!r}, "
            f"MachineId={self.Uuid!r}, "
            f"JurisdictionId={self.JurisdictionId!r}, "
            f"VPSTypeId={self.VPSTypeId!r}, "
            f"CustomerNumber={self.CustomerNumber!r}, "
            f"VPSNumber={self.VPSNumber!r})"
        )
class DetectNodePayload(BaseModel):
    RequestId: str
    VPSId: str
    Uuid: str
    JurisdictionId: int
    VPSTypeId: int
    CustomerNumber: str
    VPSNumber: int
    def __str__(self):
        return (
            f"DetectNodePayload("
            f"RequestId={self.RequestId}, "
            f"VPSId={self.VPSId}, "
            f"MachineId={self.Uuid}, "
            f"JurisdictionId={self.JurisdictionId}, "
            f"VPSTypeId={self.VPSTypeId}, "
            f"CustomerNumber={self.CustomerNumber}, "
            f"VPSNumber={self.VPSNumber})"
        )
    def __repr__(self):
        return (
            f"DetectNodePayload("
            f"RequestId={self.RequestId!r}, "
            f"VPSId={self.VPSId!r}, "
            f"MachineId={self.Uuid!r}, "
            f"JurisdictionId={self.JurisdictionId!r}, "
            f"VPSTypeId={self.VPSTypeId!r}, "
            f"CustomerNumber={self.CustomerNumber!r}, "
            f"VPSNumber={self.VPSNumber!r})"
        )
class ExpandNodePayload(BaseModel):
    RequestId: str
    VPSId: str
    Uuid: str
    JurisdictionId: int
    VPSTypeId: int
    CustomerNumber: str
    VPSNumber: int
    NodeName: str
    def __str__(self):
        return (
            f"ExpandNodePayload("
            f"RequestId={self.RequestId}, "
            f"VPSId={self.VPSId}, "
            f"MachineId={self.Uuid}, "
            f"JurisdictionId={self.JurisdictionId}, "
            f"VPSTypeId={self.VPSTypeId}, "
            f"CustomerNumber={self.CustomerNumber}, "
            f"VPSNumber={self.VPSNumber}, "
            f"NodeName={self.NodeName})"
        )
    def __repr__(self):
        return (
            f"ExpandNodePayload("
            f"RequestId={self.RequestId!r}, "
            f"VPSId={self.VPSId!r}, "
            f"MachineId={self.Uuid!r}, "
            f"JurisdictionId={self.JurisdictionId!r}, "
            f"VPSTypeId={self.VPSTypeId!r}, "
            f"CustomerNumber={self.CustomerNumber!r}, "
            f"VPSNumber={self.VPSNumber!r}, "
            f"NodeName={self.NodeName!r})"
        )

class ExpandPartitionPayload(BaseModel):
    RequestId: str
    VPSId: str
    Uuid: str
    JurisdictionId: int
    VPSTypeId: int
    CustomerNumber: str
    VPSNumber: int
    NodeName: str

    def __str__(self):
        return (
            f"ExpandPartitionPayload("
            f"RequestId={self.RequestId}, "
            f"VPSId={self.VPSId}, "
            f"MachineId={self.Uuid}, "
            f"JurisdictionId={self.JurisdictionId}, "
            f"VPSTypeId={self.VPSTypeId}, "
            f"CustomerNumber={self.CustomerNumber}, "
            f"VPSNumber={self.VPSNumber}, "
            f"NodeName={self.NodeName})"
        )
    def __repr__(self):
        return (
            f"ExpandPartitionPayload("
            f"RequestId={self.RequestId!r}, "
            f"VPSId={self.VPSId!r}, "
            f"MachineId={self.Uuid!r}, "
            f"JurisdictionId={self.JurisdictionId!r}, "
            f"VPSTypeId={self.VPSTypeId!r}, "
            f"CustomerNumber={self.CustomerNumber!r}, "
            f"VPSNumber={self.VPSNumber!r}, "
            f"NodeName={self.NodeName!r})"
        )
class DeprovisionVmPayload(BaseModel):
    RequestId: str
    MachineId: str
    CustomerNumber: str
    VPSNumber: int
    def __str__(self):
        return (
            f"DeprovisionVmPayload("
            f"RequestId={self.RequestId}, "
            f"MachineId={self.MachineId}, "
            f"CustomerNumber={self.CustomerNumber}, "
            f"VPSNumber={self.VPSNumber})"
        )
    def __repr__(self):
        return (
            f"DeprovisionVmPayload("
            f"RequestId={self.RequestId!r}, "
            f"MachineId={self.MachineId!r}, "
            f"CustomerNumber={self.CustomerNumber!r}, "
            f"VPSNumber={self.VPSNumber!r})"
        )

    
class DeprovisionNicPayload(BaseModel):
    RequestId: str
    MachineId: str
    CustomerNumber: str
    VPSNumber: int
    
    def __str__(self):
        return (
            f"DeprovisionNicPayload("
            f"RequestId={self.RequestId}, "
            f"MachineId={self.MachineId}, "
            f"CustomerNumber={self.CustomerNumber}, "
            f"VPSNumber={self.VPSNumber})"
        )
    def __repr__(self):
        return (
            f"DeprovisionNicPayload("
            f"RequestId={self.RequestId!r}, "
            f"MachineId={self.MachineId!r}, "
            f"CustomerNumber={self.CustomerNumber!r}, "
            f"VPSNumber={self.VPSNumber!r})"
        )

class DeleteRcg(BaseModel):
    RequestId: str
    MachineId: str
    CustomerNumber: str
    VPSNumber: int
    def __str__(self):
        return (
            f"DeleteRcg("
            f"RequestId={self.RequestId}, "
            f"MachineId={self.MachineId}, "
            f"CustomerNumber={self.CustomerNumber}, "
            f"VPSNumber={self.VPSNumber})"
        )
    def __repr__(self):
        return (
            f"DeleteRcg("
            f"RequestId={self.RequestId!r}, "
            f"MachineId={self.MachineId!r}, "
            f"CustomerNumber={self.CustomerNumber!r}, "
            f"VPSNumber={self.VPSNumber!r})"
        )
