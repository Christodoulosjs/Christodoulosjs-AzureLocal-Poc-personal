OPERATION_TYPES = {
    1: "completeProvisioning",
    2: "completeResizeprovisioning",
    3: "VMRestarted",
    4: "completeResetPassword",
    6: "completeDeprovisioning",
    7: "RDPEnabled",
    8: "DeprovisionTurnedOff"
}
def get_sqs_type(operation_id: int) -> str:
    try:
        return OPERATION_TYPES[operation_id]
    except KeyError:
        raise ValueError(f"Unknown operation_id: {operation_id}")