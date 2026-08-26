import uuid

from django.db import models
from django.db.models.functions import UUID4

# Create your models here.

class blog(models.Model):
    id = models.UUIDField(primary_key = True , default= uuid.uuid4)
    name = models.CharField(max_length=50)
    topic = models.CharField(max_length=50 , unique=True)
    discription = models.TextField()
    created_at = models.DateTimeField(auto_now_add = True)
    updated_at = models.DateTimeField(auto_now= True)