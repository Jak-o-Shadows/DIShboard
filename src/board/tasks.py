import socket
import io
import time
import random
from django_tasks import task
import opendis.dis7 as dis7
from opendis.DataInputStream import DataInputStream
from opendis.DataOutputStream import DataOutputStream
from django.utils import timezone
from .models import PduHub
from . import pdu_models

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
                pdu = dis7.EntityStatePdu()
                stream = DataInputStream(io.BytesIO(data))
                pdu.parse(stream)
                
                # 1. Create the spoke record
                spoke = pdu_models.EntityStatePdu.objects.create(
                    entityID_siteID=pdu.entityID.siteID,
                    entityID_applicationID=pdu.entityID.applicationID,
                    entityID_entityID=pdu.entityID.entityID,
                    forceId=pdu.forceId,
                    numberOfVariableParameters=pdu.numberOfVariableParameters,
                    entityType_entityKind=pdu.entityType.entityKind,
                    entityType_domain=pdu.entityType.domain,
                    entityType_country=pdu.entityType.country,
                    entityType_category=pdu.entityType.category,
                    entityType_subcategory=pdu.entityType.subcategory,
                    entityType_specific=pdu.entityType.specific,
                    entityType_extra=pdu.entityType.extra,
                    alternativeEntityType_entityKind=pdu.alternativeEntityType.entityKind,
                    alternativeEntityType_domain=pdu.alternativeEntityType.domain,
                    alternativeEntityType_country=pdu.alternativeEntityType.country,
                    alternativeEntityType_category=pdu.alternativeEntityType.category,
                    alternativeEntityType_subcategory=pdu.alternativeEntityType.subcategory,
                    alternativeEntityType_specific=pdu.alternativeEntityType.specific,
                    alternativeEntityType_extra=pdu.alternativeEntityType.extra,
                    entityLinearVelocity_x=pdu.entityLinearVelocity.x,
                    entityLinearVelocity_y=pdu.entityLinearVelocity.y,
                    entityLinearVelocity_z=pdu.entityLinearVelocity.z,
                    entityLocation_x=pdu.entityLocation.x,
                    entityLocation_y=pdu.entityLocation.y,
                    entityLocation_z=pdu.entityLocation.z,
                    entityOrientation_psi=pdu.entityOrientation.psi,
                    entityOrientation_theta=pdu.entityOrientation.theta,
                    entityOrientation_phi=pdu.entityOrientation.phi,
                    entityAppearance=pdu.entityAppearance,
                    deadReckoningParameters_deadReckoningAlgorithm=pdu.deadReckoningParameters.deadReckoningAlgorithm,
                    deadReckoningParameters_parameters=str(pdu.deadReckoningParameters.parameters),
                    deadReckoningParameters_entityLinearAcceleration=str(pdu.deadReckoningParameters.entityLinearAcceleration),
                    deadReckoningParameters_entityAngularVelocity=str(pdu.deadReckoningParameters.entityAngularVelocity),
                    marking_characterSet=pdu.marking.characterSet,
                    marking_characters=str(pdu.marking.characters),
                    capabilities=pdu.capabilities,
                    variableParameters=str(pdu.variableParameters)
                )

                # 2. Create the hub record (the index)
                PduHub.objects.create(
                    timestamp=timezone.now(),
                    pdu_type=pdu_type,
                    site_id=pdu.entityID.siteID,
                    application_id=pdu.entityID.applicationID,
                    entity_id=pdu.entityID.entityID,
                    content_object=spoke,
                    raw_payload=data
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

