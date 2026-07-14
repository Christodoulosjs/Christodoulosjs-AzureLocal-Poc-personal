from pydantic import BaseModel

class IPEntry(BaseModel) :
        IPEntryId : int
        MACAddress : str
        privateIp : str
        publicIp : str
        port : str

        def __str__(self):
            return (
            f"IPEntry("
            f"IPEntryId={self.IPEntryId}, "
            f"MACAddress={self.MACAddress}, "
            f"privateIp={self.privateIp}, "
            f"publicIp={self.publicIp}, "
            f"port={self.port})"
        )
        def __repr__(self):
            return str(self)
