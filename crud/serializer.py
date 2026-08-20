from .models import blog
from rest_framework import serializers

class blogserializer(serializers.ModelSerializer):
    class Meta:
        model = blog
        field = "__all__" 