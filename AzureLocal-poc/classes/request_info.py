class RequestInfo:

    def __init__(
        self,
        customer_number,
        machine_id,
        vps_type,
        jurisdiction,
        vpsNumber,
        vpsId,
        nodeNumber,
        clusterNumber,
        volume
    ):
        self.customer_number = customer_number
        self.machine_id = machine_id
        self.vps_type = vps_type
        self.jurisdiction = jurisdiction
        self.vpsNumber= vpsNumber
        self.vpsId= vpsId
        self.nodeNumber = nodeNumber
        self.clusterNumber = clusterNumber
        self.volume = volume
    @property
    def resource_group(self):
        return f"{self.customer_number}-{self.vpsNumber}-rg"

    @property
    def nic_name(self):
        return f"{self.customer_number}-{self.vpsNumber}-nic"

    @property
    def vm_name(self):
        return f"{self.customer_number}-{self.vpsNumber}"
    
    def __str__(self):
        return (
            f"RequestInfo("
            f"VM={self.vm_name}, "
            f"VPSId={self.vpsId}, "
            f"MachineId={self.machine_id}, "
            f"Customer={self.customer_number}, "
            f"Node={self.nodeNumber}, "
            f"Cluster={self.clusterNumber}, "
            f"Volume={self.volume}, "
            f"NicName={self.nic_name}, "
            f"ResourceGroup={self.resource_group})"
        )

    def __repr__(self):
        return str(self)