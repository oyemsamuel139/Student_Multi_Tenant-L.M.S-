import uuid

from django.db import models

# Create your models here.

class TimeStampedModel(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class Tenant(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=150)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.name
    

class TenantAwareModel(TimeStampedModel):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    tenant_id = models.UUIDField()
    tenant = models.ForeignKey('Users.Tenant', on_delete=models.CASCADE)

    class Meta:
        abstract = True


class TenantDomain(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    tenant = models.ForeignKey(Tenant, on_delete=models.CASCADE)
    domain_name = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.domain_name

    
class AuditLog(TimeStampedModel):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    action = models.CharField(max_length=255)
    user = models.ForeignKey('Users.User', on_delete=models.CASCADE)
    payload = models.JSONField(default=dict)

    def __str__(self):
        return f"{self.action} by {self.user.email} on {self.created_at}"