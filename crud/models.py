import uuid
from django.contrib.auth.models import User
from django.db import models

# Create your models here.

class blog(models.Model):
    author = models.ForeignKey(User , on_delete= models.CASCADE , blank=True ,null=True , related_name='blogs' )
    id = models.UUIDField(primary_key = True , default= uuid.uuid4)
    name = models.CharField(max_length=50)
    topic = models.CharField(max_length=50 , unique=True)
    discription = models.TextField()
    image = models.ImageField(upload_to='blog_images/',blank=True,null=True)
    created_at = models.DateTimeField(auto_now_add = True)
    updated_at = models.DateTimeField(auto_now= True)

    def __str__(self):
        return self.topic

class EmailOTP(models.Model):

    user = models.OneToOneField(User,on_delete=models.CASCADE,related_name='email_otp')
    otp = models.CharField(max_length=6)
    created_at = models.DateTimeField(auto_now_add=True)
    is_verified = models.BooleanField(default=False)
    def __str__(self):
        return self.user.email