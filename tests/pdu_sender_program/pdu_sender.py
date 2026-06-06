import socket
import time
import io
from django.core.management.base import BaseCommand
from opendis.dis7 import EntityStatePdu
from opendis.DataOutputStream import DataOutputStream

class Command(BaseCommand):
    help = "Sends dummy Entity State PDUs to the ingestion port"

    def handle(self, *args, **options):
        # Setup UDP socket
        sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        destination = ("127.0.0.1", 3500)
        
        # Initialize a PDU
        pdu = EntityStatePdu()
        pdu.pduType = 1  # Entity State
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
        pdu.entityID.entityID = 100
        
        # Starting coordinates (Geocentric)
        x, y, z = 4500000.0, 500000.0, 4500000.0
        
        self.stdout.write(self.style.SUCCESS(f"Simulating entity movement to {destination}..."))
        
        try:
            while True:
                # Update position slightly to simulate movement
                pdu.entityLocation.x = x
                pdu.entityLocation.y = y
                pdu.entityLocation.z = z
                
                # Serialize to binary
                output = io.BytesIO()
                stream = DataOutputStream(output)
                pdu.serialize(stream)
                data = output.getvalue()
                
                # Send over UDP
                sock.sendto(data, destination)
                
                x += 10.5
                y += 5.2
                
                self.stdout.write(f"Sent PDU: Pos({x:.1f}, {y:.1f})", ending='\r')
                time.sleep(0.005)  # Send at 200 Hz
        except KeyboardInterrupt:
            self.stdout.write("\nStopped simulation.")

if __name__ == "__main__":
    # TODO: Put a CLI into this for better control over parameters like port and update rate

    c = Command()
    c.handle()