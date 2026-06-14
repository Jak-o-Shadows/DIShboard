from django.db import models

# @PDU persistence model, IMPL_ENTITY_PDU_MODEL, code_impl, [SPEC_DB_INDEXING, SPEC_BLOB_STORAGE, REQ_PERSISTENCE, REQ_SCHEMA_FLEXIBILITY]
class PDUBase(models.Model):
    """Base metadata for all ingested PDUs."""
    timestamp = models.DateTimeField(auto_now_add=True, db_index=True)
    pdu_type = models.IntegerField(db_index=True)
    protocol_version = models.IntegerField()
    exercise_id = models.IntegerField()
    raw_payload = models.BinaryField(help_text="The original binary message.")

    @property
    def pdu_name(self):
        return self.__class__.__name__

    @property
    def pdu_type_name(self):
        return self.__class__.__name__

    class Meta:
        abstract = True
        ordering = ['-timestamp']

# @Entity State PDU model, IMPL_ENTITY_STATE_PDU, code_impl, [SPEC_DIS_TRANSLATION_LAYER, SPEC_MESSAGES_PAGE, REQ_PERSISTENCE]
class EntityStatePDU(PDUBase):
    """Specific table for Entity State PDUs (Type 1)."""
    # Entity ID
    site_id = models.IntegerField()
    application_id = models.IntegerField()
    entity_id = models.IntegerField()
    
    # Position (Geocentric coordinates)
    pos_x = models.FloatField()
    pos_y = models.FloatField()
    pos_z = models.FloatField()
    
    # Orientation (Euler angles)
    psi = models.FloatField()
    theta = models.FloatField()
    phi = models.FloatField()

    # Entity Appearance/Type
    entity_kind = models.IntegerField()
    entity_domain = models.IntegerField()
    entity_country = models.IntegerField()

    def __str__(self):
        return f"EntityState [{self.site_id}:{self.application_id}:{self.entity_id}]"


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


# COPILOT DID THE FOLLOWING

class FirePDU(PDUBase):
    firing_site_id = models.IntegerField(null=True, blank=True)
    firing_application_id = models.IntegerField(null=True, blank=True)
    firing_entity_id = models.IntegerField(null=True, blank=True)

    target_site_id = models.IntegerField(null=True, blank=True)
    target_application_id = models.IntegerField(null=True, blank=True)
    target_entity_id = models.IntegerField(null=True, blank=True)

    munition_site_id = models.IntegerField(null=True, blank=True)
    munition_application_id = models.IntegerField(null=True, blank=True)
    munition_entity_id = models.IntegerField(null=True, blank=True)

    event_site_id = models.IntegerField(null=True, blank=True)
    event_application_id = models.IntegerField(null=True, blank=True)
    event_id = models.IntegerField(null=True, blank=True)

    fire_mission_index = models.IntegerField(null=True, blank=True)

    def __str__(self):
        return f"Fire [{self.firing_site_id}:{self.firing_application_id}:{self.firing_entity_id}]"

class DetonationPDU(PDUBase):
    firing_site_id = models.IntegerField(null=True, blank=True)
    firing_application_id = models.IntegerField(null=True, blank=True)
    firing_entity_id = models.IntegerField(null=True, blank=True)

    target_site_id = models.IntegerField(null=True, blank=True)
    target_application_id = models.IntegerField(null=True, blank=True)
    target_entity_id = models.IntegerField(null=True, blank=True)

    munition_site_id = models.IntegerField(null=True, blank=True)
    munition_application_id = models.IntegerField(null=True, blank=True)
    munition_entity_id = models.IntegerField(null=True, blank=True)

    event_site_id = models.IntegerField(null=True, blank=True)
    event_application_id = models.IntegerField(null=True, blank=True)
    event_id = models.IntegerField(null=True, blank=True)

    detonation_result = models.IntegerField(null=True, blank=True)
    location_x = models.FloatField(null=True, blank=True)
    location_y = models.FloatField(null=True, blank=True)
    location_z = models.FloatField(null=True, blank=True)
    velocity_x = models.FloatField(null=True, blank=True)
    velocity_y = models.FloatField(null=True, blank=True)
    velocity_z = models.FloatField(null=True, blank=True)

    def __str__(self):
        return f"Detonation [{self.event_site_id}:{self.event_application_id}:{self.event_id}]"

class CollisionPDU(PDUBase):
    issuing_site_id = models.IntegerField(null=True, blank=True)
    issuing_application_id = models.IntegerField(null=True, blank=True)
    issuing_entity_id = models.IntegerField(null=True, blank=True)

    colliding_site_id = models.IntegerField(null=True, blank=True)
    colliding_application_id = models.IntegerField(null=True, blank=True)
    colliding_entity_id = models.IntegerField(null=True, blank=True)

    collision_type = models.IntegerField(null=True, blank=True)
    location_x = models.FloatField(null=True, blank=True)
    location_y = models.FloatField(null=True, blank=True)
    location_z = models.FloatField(null=True, blank=True)
    velocity_x = models.FloatField(null=True, blank=True)
    velocity_y = models.FloatField(null=True, blank=True)
    velocity_z = models.FloatField(null=True, blank=True)

    def __str__(self):
        return f"Collision [{self.issuing_site_id}:{self.issuing_application_id}:{self.issuing_entity_id}]"
