
from django.db import models

# Create your models here.

class blog(models.Model):
    id = models.IntegerField(primary_key = True , editable=True)
    name = models.CharField(max_length=50)
    topic = models.CharField(max_length=50)
    discription = models.TextField()
    created_at = models.DateTimeField(auto_now_add = True)
    updated_at = models.DateTimeField(auto_now= True)