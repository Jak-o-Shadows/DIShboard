from django.db import models
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes.fields import GenericForeignKey

from .pdu_models import *

# @PDU persistence model, IMPL_ENTITY_PDU_MODEL, code_impl, [SPEC_DB_INDEXING, SPEC_BLOB_STORAGE, REQ_PERSISTENCE, REQ_SCHEMA_FLEXIBILITY]
class PduHub(models.Model):
    """
    A lightweight registry that points to specific records in 'spoke' tables.
    """
    timestamp = models.DateTimeField(db_index=True)
    pdu_type = models.IntegerField(db_index=True) # e.g., 1 for EntityState, 2 for Fire
    site_id = models.IntegerField(db_index=True, null=True)
    application_id = models.IntegerField(db_index=True, null=True)
    entity_id = models.IntegerField(db_index=True, null=True)
    
    # These two fields identify the 'spoke' table row
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    object_id = models.PositiveIntegerField()
    content_object = GenericForeignKey('content_type', 'object_id')

    # For the hell of it, store the raw blob
    raw_payload = models.BinaryField(help_text="The original binary message.")

    class Meta:
        ordering = ['-timestamp']

class IngestionState(models.Model):
    listen_host = models.GenericIPAddressField(
        default='0.0.0.0',
        protocol='both',
        unpack_ipv4=False,
        help_text='Local address bound for DIS ingestion.',
    )
    listen_port = models.IntegerField(
        default=3500,
        help_text='UDP port bound for DIS ingestion.',
    )
    running = models.BooleanField(default=False)
    started_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        status = 'running' if self.running else 'stopped'
        return f"DIS ingestion {status} on {self.listen_host}:{self.listen_port}"