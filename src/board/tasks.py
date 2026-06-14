import socket
import io
import time
import random
from django_tasks import task
import opendis.dis7 as dis7
from opendis.dis7 import EntityStatePdu
from opendis.DataInputStream import DataInputStream
from opendis.DataOutputStream import DataOutputStream
from .models import EntityStatePDU

# @DIS ingestion task, IMPL_DIS_INGESTION_TASK, code_impl, [SPEC_OPEN_DIS_PY, REQ_PERSISTENCE]
@task()
def listen_for_dis_packets(listen_host: str = '0.0.0.0', port: int = 3500):
    """
    A long-running task that listens for UDP DIS packets and persists them.
    """
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.bind((listen_host, port))
    
    print(f"Ingestion started: Listening for DIS traffic on port {port}...")
    
    while True:
        try:
            data, addr = sock.recvfrom(2048)
            
            # Basic PDU Header check
            if len(data) < 12:
                continue
                
            pdu_type = data[2]
            
            # Type 1: Entity State PDU
            if pdu_type == 1:
                pdu = EntityStatePdu()
                stream = DataInputStream(io.BytesIO(data))
                pdu.parse(stream)
                
                EntityStatePDU.objects.create(
                    pdu_type=pdu_type,
                    protocol_version=data[0],
                    exercise_id=data[1],
                    raw_payload=data,
                    site_id=pdu.entityID.siteID,
                    application_id=pdu.entityID.applicationID,
                    entity_id=pdu.entityID.entityID,
                    pos_x=pdu.entityLocation.x,
                    pos_y=pdu.entityLocation.y,
                    pos_z=pdu.entityLocation.z,
                    psi=pdu.entityOrientation.psi,
                    theta=pdu.entityOrientation.theta,
                    phi=pdu.entityOrientation.phi,
                    entity_kind=pdu.entityType.entityKind,
                    entity_domain=pdu.entityType.domain,
                    entity_country=pdu.entityType.country,
                )
        except Exception as e:
            # Use logging in a production scenario
            print(f"Error processing packet: {e}")


# @Playback sender task, IMPL_PLAYBACK_SENDER_TASK, code_impl, [SPEC_PLAYBACK_SELECTION_VIEW]
@task()
def send_test_pdus(duration_seconds: int = 30, destination_host: str = '127.0.0.1', destination_port: int = 3500):
    """Send synthetic DIS PDUs to the target ingestion listener."""
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    destination = (destination_host, destination_port)
    x, y, z = 4500000.0, 500000.0, 4500000.0
    entity_id = 100
    end_time = time.time() + duration_seconds

    while time.time() < end_time:
        pdu = _build_entity_state_pdu(x, y, z, entity_id)
        output = io.BytesIO()
        stream = DataOutputStream(output)
        pdu.serialize(stream)
        sock.sendto(output.getvalue(), destination)

        x += 10.5
        y += 5.2
        if random.random() < 0.02:
            entity_id += 1

        time.sleep(0.005)

    sock.close()

def _build_entity_state_pdu(x, y, z, entity_id):
    pdu = dis7.EntityStatePdu()
    pdu.pduType = 1
    pdu.protocolVersion = 7
    pdu.exerciseID = 1
    pdu.pduStatus = 0
    pdu.protocolFamily = 1
    pdu.timestamp = 0
    pdu.length = 144
    pdu.forceId = 1
    pdu.entityAppearance = 0
    pdu.capabilities = 0
    pdu.entityID.siteID = 1
    pdu.entityID.applicationID = 1
    pdu.entityID.entityID = entity_id
    pdu.entityLocation.x = x
    pdu.entityLocation.y = y
    pdu.entityLocation.z = z
    pdu.psi = 0.0
    pdu.theta = 0.0
    pdu.phi = 0.0
    return pdu
