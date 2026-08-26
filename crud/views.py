from django_filters.rest_framework import DjangoFilterBackend
from django.contrib.auth import authenticate

from rest_framework.response import Response
from rest_framework.decorators import api_view , permission_classes
from rest_framework.permissions import IsAuthenticated , AllowAny 
from rest_framework import status

from rest_framework_simplejwt.tokens import RefreshToken , TokenError
from .filter import BlogFilter
from .models import blog  
from .serializer import LoginSerializer, blogserializer,Registerationserializer,refreshserialier


# @api_view (['POST'])
# @permission_classes ([AllowAny])
# def registration (request):
#     username = request.data.get('username')
#     password = request.data.get('password') 
#     if not username or not password:
#         return Response({"error":"enter username and password"}, status= status.HTTP_400_BAD_REQUEST)

#     if User.objects.filter(username = username).exists():
#         return Response({"error":"user already existed"})

#     user = User.objects.create_user(username=username)
#     user.set_password(password)
#     user.save()
#     return Response("User created successfully" , status=status.HTTP_201_CREATED)

@api_view (['POST'])
@permission_classes ([AllowAny])
def registration (request):
    serializer = Registerationserializer(data=request.data)
    serializer.is_valid(raise_exception=True)
    user = serializer.save()
    return Response(
        {
            "message":"user created successfully",
            "user": user.username
        }, status=status.HTTP_201_CREATED
    )

# @api_view (['POST'])
# @permission_classes ([AllowAny])
# def login(request):
#     username = request.data.get('username')
#     password = request.data.get('password')

#     User  = authenticate(
#         username = username,
#         password = password
#     )

#     if User is None:
#         return Response(
#             {"ERROR":"invalid username and passwprd"},
#             status=status.HTTP_401_UNAUTHORIZED
#         )

#     Refresh = RefreshToken.for_user(User)

#     return Response(
#         {
#             "REFRESH TOKEN": str(Refresh),
#             "ACCESS TOKEN" : str(Refresh.access_token)
#         },
#         status=status.HTTP_200_OK
#     )


@api_view (['POST'])
@permission_classes ([AllowAny])
def login(request):
    serializer = LoginSerializer(data= request.data)
    serializer.is_valid(raise_exception=True)
    username = serializer.validated_data["username"]
    password = serializer.validated_data["password"]
    user = authenticate(username=username,password=password)
    if user is None:
        return Response({
            "error":"Invalid username and password"
        },status=status.HTTP_401_UNAUTHORIZED
        )
    refresh_token = RefreshToken.for_user(user=user)
    return Response({"message" : "user login successfull",
                     "username": user.username,
                     "is_superuser":user.is_superuser,
                     "access_token":f"{refresh_token.access_token}","refresh_token":f"{refresh_token}"})


# @api_view (['POST'])
# @permission_classes ([AllowAny])
# def referesh_token(request):

#     refresh = request.data["refresh"]

#     if not refresh:
#         return Response(
#             {
#             "error":"enter refresh token"
#             }, status=status.HTTP_400_BAD_REQUEST
#         )
    
#     # breakpoint()

#     try:
#         token = RefreshToken(refresh)
#         return Response(
#             {
#                 "access_Token": str(token.access_token)
#             },status=status.HTTP_200_OK
#         ) 
    
#     except TokenError:
#         return Response(
#             {
#                 "access_token":"access token invalid"
#             },status=status.HTTP_401_UNAUTHORIZED
#         )

@api_view (['POST'])
@permission_classes ([AllowAny])
def referesh_token(request):
    serializer = refreshserialier(data = request.data)

    if serializer.is_valid():
        return Response(
            {
                "access_token": serializer.validated_data["access"]
            },
            status=status.HTTP_200_OK
        )
    return Response(
        {
            "ERROR":"refresh token is invalid"
        },
        status=status.HTTP_400_BAD_REQUEST
    )

@api_view (['POST'])
@permission_classes([IsAuthenticated])
def blog_create (request):

    serializer = blogserializer( data = request.data)
    if serializer.is_valid():
        blog_object = serializer.save(
            author =  request.user
        )
        
        return Response( blogserializer(blog_object).data , status= status.HTTP_201_CREATED)
    return Response(serializer.errors , status=status.HTTP_400_BAD_REQUEST)

@api_view (['PUT','PATCH'])
def blog_update (request , name):
    try:
        blog_object = blog.objects.get( name = name)

    except blog.DoesNotExist:
        return Response( {
            "message" : "blog does not exist"
        } , status=status.HTTP_400_BAD_REQUEST)

    if (
        not request.user.is_superuser
        and blog_object.author != request.user
    ):
        return Response({
            "message":"you can only update your blog"
        },status=status.HTTP_403_FORBIDDEN
        )

    serializer = blogserializer(
        blog_object , data = request.data , partial = True
    )

    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data ,status=status.HTTP_200_OK)
    return Response(serializer.errors , status=status.HTTP_400_BAD_REQUEST)

@api_view (['DELETE'])
def blog_delete (request , name ):
    try:
        blog_object = blog.objects.get(name= name)

    except blog.DoesNotExist:
        return Response({"error : the blog not exist"} , status=status.HTTP_400_BAD_REQUEST)

    if(
        not request.user.is_superuser
        and blog_object.author != request.user 
    ):
        return Response({
            "message":"you can only delete your blog"
        },status=status.HTTP_403_FORBIDDEN
        )

    blog_object.delete()

    return Response({"message" :f"{name} is deleted"} , status=status.HTTP_200_OK)

@api_view (['GET']) 
@permission_classes([IsAuthenticated])
def blog_show(request):

    blogs = blog.objects.all()

    filterset = BlogFilter(request.GET,queryset=blogs)

    if filterset.is_valid():
        blogs = filterset.qs

    if not blogs.exists():
        return Response({
            "message":" there is no one in this list with that name"
        },status=status.HTTP_400_BAD_REQUEST
        )

    serializer = blogserializer(blogs,many=True)

    return Response(serializer.data,status=status.HTTP_200_OK)

