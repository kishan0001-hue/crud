from .models import blog
from .serializer import serializer

class blogserializer(serializer.Modelserializer):
    class Meta:
        model = blog
        field = "__all__" 