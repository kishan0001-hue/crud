
from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework import status
from .serializer import blogserializer


# Create your views here.

@api_view (['POST'])
def blog_create (request):

    Value = blogserializer( data = request.data)
    if Value.is_valid():
        Value.save()
        return Response( Value.data , status= status.HTTP_200_OK)
    return Response(Value.error , status=status.HTTP_400_BAD_REQUEST)


