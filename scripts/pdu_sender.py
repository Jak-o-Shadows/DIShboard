import socket
import time
import io
import random
from django.core.management.base import BaseCommand
import opendis.dis7 as dis7
from opendis.DataOutputStream import DataOutputStream

class Command(BaseCommand):
    help = (
        "Sends dummy DIS PDUs to the ingestion port, primarily Entity State PDUs with occasional "
        "Fire, Detonation, and Collision PDUs."
    )

    def handle(self, *args, **options):
        sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        destination = ("127.0.0.1", 3500)

        x, y, z = 4500000.0, 500000.0, 4500000.0
        entity_id = 100
        counter = 0

        self.stdout.write(self.style.SUCCESS(f"Simulating PDU traffic to {destination}..."))

        try:
            while True:
                counter += 1
                pdu = self._choose_pdu(counter, x, y, z, entity_id)

                output = io.BytesIO()
                stream = DataOutputStream(output)
                pdu.serialize(stream)
                data = output.getvalue()
                sock.sendto(data, destination)

                x += 10.5
                y += 5.2
                if counter % 50 == 0:
                    entity_id += 1

                self.stdout.write(
                    f"Sent {pdu.__class__.__name__}: Pos({x:.1f}, {y:.1f})",
                    ending='\r',
                )
                time.sleep(0.005)
        except KeyboardInterrupt:
            self.stdout.write("\nStopped simulation.")

    def _choose_pdu(self, counter, x, y, z, entity_id):
        roll = random.random()
        if roll < 0.80 or not self._has_alternate_pdus():
            return self._build_entity_state_pdu(x, y, z, entity_id)
        if roll < 0.90 and hasattr(dis7, 'FirePdu'):
            return self._build_fire_pdu(x, y, z, entity_id)
        if roll < 0.95 and hasattr(dis7, 'DetonationPdu'):
            return self._build_detonation_pdu(x, y, z, entity_id)
        if hasattr(dis7, 'CollisionPdu'):
            return self._build_collision_pdu(x, y, z, entity_id)
        return self._build_entity_state_pdu(x, y, z, entity_id)

    def _has_alternate_pdus(self):
        return any(
            hasattr(dis7, pdu_name)
            for pdu_name in ('FirePdu', 'DetonationPdu', 'CollisionPdu')
        )

    def _build_entity_state_pdu(self, x, y, z, entity_id):
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

    def _build_fire_pdu(self, x, y, z, entity_id):
        pdu = dis7.FirePdu()
        pdu.pduType = 2
        pdu.protocolVersion = 7
        pdu.exerciseID = 1
        pdu.pduStatus = 0
        pdu.protocolFamily = 2
        pdu.timestamp = 0
        pdu.length = 192
        pdu.forceId = 1
        pdu.entityAppearance = 0
        pdu.capabilities = 0

        pdu.firingEntityID.siteID = 1
        pdu.firingEntityID.applicationID = 1
        pdu.firingEntityID.entityID = entity_id
        pdu.targetEntityID.siteID = 1
        pdu.targetEntityID.applicationID = 1
        pdu.targetEntityID.entityID = entity_id + 1
        pdu.munitionEntityID.siteID = 1
        pdu.munitionEntityID.applicationID = 1
        pdu.munitionEntityID.entityID = entity_id + 2
        pdu.eventID.siteID = 1
        pdu.eventID.applicationID = 1
        pdu.eventID.entityID = 1
        pdu.fireMissionIndex = 1
        return pdu

    def _build_detonation_pdu(self, x, y, z, entity_id):
        pdu = dis7.DetonationPdu()
        pdu.pduType = 3
        pdu.protocolVersion = 7
        pdu.exerciseID = 1
        pdu.pduStatus = 0
        pdu.protocolFamily = 2
        pdu.timestamp = 0
        pdu.length = 240
        pdu.forceId = 1
        pdu.entityAppearance = 0
        pdu.capabilities = 0

        pdu.firingEntityID.siteID = 1
        pdu.firingEntityID.applicationID = 1
        pdu.firingEntityID.entityID = entity_id
        pdu.targetEntityID.siteID = 1
        pdu.targetEntityID.applicationID = 1
        pdu.targetEntityID.entityID = entity_id + 1
        pdu.munitionEntityID.siteID = 1
        pdu.munitionEntityID.applicationID = 1
        pdu.munitionEntityID.entityID = entity_id + 2
        pdu.eventID.siteID = 1
        pdu.eventID.applicationID = 1
        pdu.eventID.entityID = 1
        pdu.detonationResult = 1
        if hasattr(pdu, 'location'):
            pdu.location.x = x
            pdu.location.y = y
            pdu.location.z = z
        if hasattr(pdu, 'velocity'):
            pdu.velocity.x = 0.0
            pdu.velocity.y = 0.0
            pdu.velocity.z = 0.0
        return pdu

    def _build_collision_pdu(self, x, y, z, entity_id):
        pdu = dis7.CollisionPdu()
        pdu.pduType = 4
        pdu.protocolVersion = 7
        pdu.exerciseID = 1
        pdu.pduStatus = 0
        pdu.protocolFamily = 2
        pdu.timestamp = 0
        pdu.length = 224
        pdu.forceId = 1
        pdu.entityAppearance = 0
        pdu.capabilities = 0

        pdu.issuingEntityID.siteID = 1
        pdu.issuingEntityID.applicationID = 1
        pdu.issuingEntityID.entityID = entity_id
        pdu.collidingEntityID.siteID = 1
        pdu.collidingEntityID.applicationID = 1
        pdu.collidingEntityID.entityID = entity_id + 1
        pdu.collisionType = 1
        if hasattr(pdu, 'location'):
            pdu.location.x = x
            pdu.location.y = y
            pdu.location.z = z
        if hasattr(pdu, 'velocity'):
            pdu.velocity.x = 0.0
            pdu.velocity.y = 0.0
            pdu.velocity.z = 0.0
        return pdu

if __name__ == "__main__":
    # TODO: Put a CLI into this for better control over parameters like port and update rate

    c = Command()
    c.handle()