from django.db import models

class PDUBase(models.Model):
    """Base metadata for all ingested PDUs."""
    timestamp = models.DateTimeField(auto_now_add=True, db_index=True)
    pdu_type = models.IntegerField(db_index=True)
    protocol_version = models.IntegerField()
    exercise_id = models.IntegerField()
    raw_payload = models.BinaryField(help_text="The original binary message.")

    class Meta:
        abstract = True
        ordering = ['-timestamp']

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