from classes.IPEntry_class import IPEntry
from classes.Jobs_class import PollJob
from classes.request_info import RequestInfo
from classes.deprovision_class import DeprovisionJob
from config.database import get_connection
from datetime import datetime, UTC
import uuid

# Get Info For the request based on the machine id, this will be used for all operations (provisioning, deprovisioning, restart etc...)
def checkForPendingDeprovisions() -> list[DeprovisionJob]: #PollerNeeded
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""        
        SELECT
            j.RequestId,
            r.OperationId,
            r.MachineId,
            j.PollerUrl,
            jl.CreatedAt,
            jl.StatusInfo,
            jl.Status,
            jl.JobId,
            m.VPSNumber,
            m.CustomerNumber
        FROM DevDB.dbo.Requests r
        INNER JOIN DevDB.dbo.Jobs j 
            ON r.RequestId = j.RequestId
        INNER JOIN DevDB.dbo.JobLogs jl 
            ON j.JobId = jl.JobId
        INNER JOIN DevDB.dbo.VPS m
            ON r.MachineId = m.MachineId
        WHERE 
            r.OperationId = 6
            AND jl.StatusInfo = 'Pending_Deprovision'
            AND jl.CreatedAt <= DATEADD(DAY, -7, GETDATE())

            -- ✅ Check cancellation across SAME MACHINE (not same request)
            AND NOT EXISTS (
                SELECT 1
                FROM DevDB.dbo.Requests r2
                INNER JOIN DevDB.dbo.Jobs j2 
                    ON r2.RequestId = j2.RequestId
                INNER JOIN DevDB.dbo.JobLogs jl2 
                    ON j2.JobId = jl2.JobId
                WHERE 
                    r2.MachineId = r.MachineId         
                    AND jl2.StatusInfo IN ('Cancel_Deprovision', 'Deprovision_In_Progress')
                    AND jl2.CreatedAt > jl.CreatedAt
                    )
            """)
    rows = cursor.fetchall()

    columns = [column[0] for column in cursor.description]

    results: list[DeprovisionJob] = []

    for row in rows:
        data = dict(zip(columns, row))

        results.append(
            DeprovisionJob(
                request_id=data["RequestId"],
                operation_id=data["OperationId"],
                machine_id=data["MachineId"],
                poller_url=data["PollerUrl"],
                created_at=data["CreatedAt"],
                status_info=data["StatusInfo"],
                status=data["Status"],
                job_id=data["JobId"],
                vps_number=data["VPSNumber"],
                customer_number=data["CustomerNumber"],
            )
        )

    conn.close()
    return results
def get_running_jobs() -> list[PollJob] : #Poller Needed
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
            WITH LatestLogs AS (
        SELECT 
            jl.JobId,
            jl.Status,
            jl.CreatedAt,
            ROW_NUMBER() OVER (
                PARTITION BY jl.JobId 
                ORDER BY jl.CreatedAt DESC
            ) AS rn
        FROM DevDB.dbo.JobLogs jl
    )
    SELECT 
        j.*,
        r.OperationId,
        v.CustomerNumber,
        v.VPSNumber,
        v.JurisdictionId,
        v.VPSTypeId,
        ip.PublicIP,
        ip.MacAddress,
        ip.Port
    FROM DevDB.dbo.Jobs j
    LEFT JOIN LatestLogs ll 
        ON j.JobId = ll.JobId 
        AND ll.rn = 1
    LEFT JOIN DevDB.dbo.Requests r
        ON j.RequestId = r.RequestId
    LEFT JOIN DevDB.dbo.VPS v
        ON r.MachineId = v.MachineId
    LEFT JOIN DevDB.dbo.Assignments a
        ON v.VPSId = a.VPSId
    LEFT JOIN DevDB.dbo.IPEntries ip
        ON a.IPEntryId = ip.IPEntryId
    WHERE 
        ll.JobId IS NULL
        OR ll.Status IN ('Running', 'Accepted', 'InProgress');

        """)

    rows = cursor.fetchall()
    columns = [column[0] for column in cursor.description]
    poll_jobs = [create_poll_job(row, columns) for row in rows]

    # columns = [column[0] for column in cursor.description]

    # jobs = []
    # for row in rows:
    #     data = dict(zip(columns, row))

    #     jobs.append(
    #         PollJob(
    #             job_id=data["JobId"],
    #             request_id=data["RequestId"],
    #             azure_job_id=data["AzureJobId"],
    #             vps_id=data["VPSId"],
    #             machine_id=data["MachineId"],
    #             poller_url=data["PollerUrl"],
    #             operation_id=data["OperationId"],
    #             customer_number=data["CustomerNumber"],
    #             vps_number=data["VPSNumber"],
    #             jurisdiction_id=data["JurisdictionId"],
    #         )
    #     )

    conn.close()
    return poll_jobs

def create_poll_job(row, columns)->PollJob:
    data = dict(zip(columns, row))
    return PollJob(
        job_id=data["JobId"],
        request_id=data["RequestId"],
        azure_job_id=data["AzureJobId"],
        vps_id=data["VPSId"],
        machine_id=data["MachineId"],
        poller_url=data["PollerUrl"],
        operation_id=data["OperationId"],
        customer_number=data["CustomerNumber"],
        vps_number=data["VPSNumber"],
        jurisdiction_id=data["JurisdictionId"],
        vps_type_id = data["VPSTypeId"],
        public_ip = data["PublicIP"],
        mac_address = data["MacAddress"],
        port = data["Port"]
    )

def insert_poll_log(jobID, status, statusInfo): #Poller Needed
    conn = get_connection()
    cursor = conn.cursor()
    now = datetime.now(UTC)
    logUuid = uuid.uuid4()

    cursor.execute(
        """
        INSERT INTO DevDB.dbo.JobLogs (JobLogId, JobId, Status, CreatedAt, statusInfo)
        VALUES (?, ?, ?, ?, ?)
    """,
        logUuid,
        jobID,
        status,
        now,
        statusInfo
    )

    conn.commit()
    conn.close()

def get_latest_status_info(requestId): #poller Needed
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
    SELECT TOP 1
       jl.StatusInfo
    FROM DevDB.dbo.JobLogs jl
    INNER JOIN DevDB.dbo.Jobs j
            ON j.JobId = jl.JobId
    WHERE j.RequestId = ?
        AND jl.StatusInfo IS NOT NULL
        AND LTRIM(RTRIM(jl.StatusInfo)) <> ''
    ORDER BY jl.CreatedAt DESC;
    """, requestId)

    latest_status_info = str(cursor.fetchval())
    conn.close()

    return latest_status_info

def update_health_check(volume_summary, node_summary): #Poller Needed(Needs adjustments)
    print ("We are inside update_health_check")
    print("Vol", volume_summary, "Nodes:", node_summary)
    conn = get_connection()
    cursor = conn.cursor()

    # Update volumes
    for volume in volume_summary:
        cursor.execute("""
            UPDATE DevDB.dbo.Volumes
            SET HealthStatus = ?,
                OperationalStatus = ?,
                Size = ?,
                SizeRemaining = ?
            WHERE Name = ?
        """,
        volume["health_status"],
        volume["operational_status"],
        volume["size_bytes"],
        volume["available_bytes"],
        volume["name"])

    # Update nodes
    for node in node_summary:
        cursor.execute("""
            UPDATE DevDB.dbo.Nodes
            SET StateCode = ?,
                Status = ?
            WHERE Name = ?
        """,
        node["state_code"],
        node["status"],
        node["name"])

    conn.commit()
    conn.close()
    print("Health checks passed into database!!!")

def registerNodeToVPS(node_name, machineId):             #Poller Needed(Needs adjustments)
    node_number = int(node_name.replace("HCINODE", ""))

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        UPDATE DevDB.dbo.VPS
        SET NodeId = ?
        WHERE MachineId = ?
    """, (node_number, machineId))

    conn.commit()
    conn.close()

def machine_exists(machine_id) -> bool:
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute(
        """
            SELECT CASE
            WHEN EXISTS (
                SELECT 1
                FROM DevDB.dbo.VPS
                WHERE MachineId = ?
            )
            THEN 1
            ELSE 0
        END
        """,
        machine_id,
    )
    exists = bool(cursor.fetchval())
    conn.close()
    return exists > 0

def is_operation_running(machine_id) -> bool:
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute(
        """
        SELECT TOP 1
            CASE 
                WHEN LOWER(jl.Status) IN ('running', 'accepted') THEN CAST(1 AS BIT)
                ELSE CAST(0 AS BIT)
            END AS IsRunning
        FROM DevDB.dbo.JobLogs jl
        JOIN DevDB.dbo.Jobs j ON jl.JobId = j.JobId
        WHERE j.MachineId = ?
        ORDER BY jl.CreatedAt DESC;
        """,
        machine_id,
    )

    result = cursor.fetchval()
    conn.close()

    return bool(result)

def get_IPEntries() -> IPEntry:
    conn = get_connection()
    cursor = conn.cursos()
    cursor.execute(
        """
        SELECT TOP 1
    ie.IpEntryId,
    ie.MACAddress,
    ie.PrivateIP,
    ie.PublicIP,
    ie.Port
FROM DevDB.dbo.IPEntries ie
WHERE NOT EXISTS (
    SELECT 1
    FROM Assignments a
    WHERE a.IPEntryId = ie.IpEntryId
)
ORDER BY NEWID();
""")
    row = cursor.fetchone()

    conn.close()
    if row is None:
        return None
    
    return IPEntry(
        IPEntryId=row.IPEntryId,
        MACAddress=row.MACAddress,
        privateIp=row.PrivateIp,
        publicIp=row.PublicIp,
        port=row.Port
        )

def register_ip_and_vps_assignments(vpsId, IPEntryId): #Maybe this should be executed after poller confirmation!
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute(
        """
        INSERT INTO DevDB.dbo.Assignments (VPSId, IPEntryId)
        VALUES (?, ?);
""",
vpsId,IPEntryId)
def get_request_info(machine_id) -> RequestInfo:

    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute(
        """
            SELECT TOP 1 CustomerNumber, VPSTypeId, JurisdictionId, MachineId, VPSId, VPSNumber, ClusterNumber, Node, Volume FROM DevDB.dbo.VPS
            WHERE MachineId = ?
        """,
        machine_id,
    )
    row = cursor.fetchone()

    conn.close()
    if row is None:
        return None

    return RequestInfo(
        customer_number=row.CustomerNumber,
        machine_id=row.MachineId,
        vps_type=row.VPSTypeId,
        jurisdiction=row.JurisdictionId,
        vpsNumber=row.VPSNumber,
        vpsId=row.VPSId,
        nodeNumber=row.Node,
        clusterNumber=row.ClusterNumber,
        volume=row.Volume,
    )


def insert_job(requestId, azure_job_id, VPSId, machineId, operation_url):
    conn = get_connection()
    cursor = conn.cursor()

    jobId = uuid.uuid4()
    cursor.execute(
        """
        INSERT INTO DevDB.dbo.Jobs
        (   
            JobId,
            RequestId, 
            AzureJobId,
            VPSId,
            MachineId,
            PollerUrl
        )
        VALUES (?, ?, ?, ?, ?, ?)
    """,
        jobId,
        requestId,
        azure_job_id,
        VPSId,
        machineId,
        operation_url,
    )

    conn.commit()
    conn.close()


def store_request(payload: dict, requestId):
    print("We are inside store_request, payload is: ", payload, "requestID:", requestId)
    conn = get_connection()
    cursor = conn.cursor()
    operation_id = get_operation_id(payload.Operation)
    cursor.execute(
        """
        INSERT INTO DevDB.dbo.Requests
        (CustomerNumber, VPSTypeId, JurisdictionId, OperationId, RequestId, MachineId)
        VALUES (?, ?, ?, ?, ?, ?)
    """,
        payload.CustomerNumber,
        payload.VPStype,
        payload.Juristriction,
        operation_id,
        requestId,
        payload.Uuid,
    )
    conn.commit()
    conn.close()


def get_max_vps_number(customer_number: str) -> int:
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute(
        """
        SELECT ISNULL(MAX(VPSNumber), 0)
        FROM [DevDB].[dbo].[VPS]
        WHERE CustomerNumber = ?
    """,
        (customer_number,),
    )

    result = cursor.fetchone()
    conn.close()

    return result[0] if result else 0


# Register a new VPS in the database after provisioning nic
def register_vps(
    VPSId: str,
    machine_id: str,
    customer_number: int,
    vps_type_id: int,
    jurisdiction_id: int,
    vps_number: int,
):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute(
        """
        INSERT INTO DevDB.dbo.VPS
        (
            VPSId,
            MachineId,
            CustomerNumber,
            VPSTypeId,
            JurisdictionId,
            VPSNumber
        )
        VALUES (?, ?, ?, ?, ?, ?)
    """,
        VPSId,
        machine_id,
        customer_number,
        vps_type_id,
        jurisdiction_id,
        vps_number,
    )

    conn.commit()
    conn.close()


def get_best_volume():
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT TOP 1 Name,
                     SizeRemaining
        FROM DevDB.dbo.Volumes
        WHERE HealthStatus = 'Healthy'
          AND OperationalStatus = 'OK'
        ORDER BY SizeRemaining DESC
    """)

    row = cursor.fetchone()

    conn.close()

    if row is None:
        return None

    return {"Name": row[0], "SizeRemaining": row[1]}