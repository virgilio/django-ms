from django.db import models
from . import ServiceModel

class AliveHealthCheck(ServiceModel):
   requester = models.CharField(max_length=255,)
   message = models.CharField(max_length=255)


