import socket
import io
from django_tasks import task
from opendis.dis7 import EntityStatePdu
from opendis.DataInputStream import DataInputStream
from .models import EntityStatePDU

@task()
def listen_for_dis_packets(port: int = 3500):
    """
    A long-running task that listens for UDP DIS packets and persists them.
    """
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.bind(("0.0.0.0", port))
    
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