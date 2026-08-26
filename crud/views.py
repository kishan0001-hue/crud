import random

from django.contrib.auth import authenticate
from django.contrib.auth.models import User
from django.core.mail import send_mail
from django.conf import settings
from django.utils import timezone
from django.db.models import Q

from rest_framework.response import Response
from rest_framework.decorators import api_view , permission_classes , throttle_classes
from rest_framework.permissions import IsAuthenticated , AllowAny 
from rest_framework import status
from rest_framework_simplejwt.tokens import RefreshToken , TokenError

from datetime import timedelta
from .pagination import BlogPagination
from .filter import BlogFilter
from .models import blog , EmailOTP
from .serializer import LoginSerializer, blogserializer,Registerationserializer,refreshserialier ,VerifyOTPSerializer
from .throttles import LoginThrottle,BlogCreateThrottle,BlogShowThrottle,RefreshTokenThrottle,RegistrationThrottle


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
@throttle_classes([RegistrationThrottle])
def registration (request):
    serializer = Registerationserializer(data=request.data)
    serializer.is_valid(raise_exception=True)
    user = serializer.save()

    otp = str(random.randint(100000, 999999))

    EmailOTP.objects.update_or_create(
        user=user,
        defaults={'otp': otp,'is_verified': False}
    )

    send_mail(

        subject='Email Verification OTP',
        message=f'''Hello {user.username},
        Your OTP is:{otp}
        This OTP will expire in 5 minutes.
        Please do not share this OTP with anyone.''',

        from_email=settings.DEFAULT_FROM_EMAIL,

        recipient_list=[user.email],
        fail_silently=False
    )

    return Response(
        {
            'message':
            'Registration successful. '
            'OTP has been sent to your email.'
        },

        status=status.HTTP_201_CREATED
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
@throttle_classes([LoginThrottle])
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
@throttle_classes([RefreshTokenThrottle])
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
@throttle_classes([BlogCreateThrottle])
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
@throttle_classes([BlogShowThrottle])
def blog_show(request):

    blogs = blog.objects.all()

    filterset = BlogFilter(request.GET,queryset=blogs)

    if filterset.is_valid():
        blogs = filterset.qs

    # if not blogs.exists():
        # return Response({
        #     "message":" there is no one in this list with that name"
        # },status=status.HTTP_400_BAD_REQUEST
        # )

    search = request.GET.get('search')


    if search:
        blogs = blogs.filter(
            Q(name__icontains = search)|
            Q(topic__icontains = search)|
            Q(discription__icontains = search)|
            Q(id__icontains =  search)|
            Q(author__username__icontains = search)
        )

    paginator = BlogPagination()

    paginated_blogs = paginator.paginate_queryset(blogs , request)
    serializer = blogserializer(paginated_blogs , many = True )

    return paginator.get_paginated_response(
        serializer.data
    )

    serializer = blogserializer(blogs,many=True)
    return Response(serializer.data,status=status.HTTP_200_OK)

@api_view(['POST'])
@permission_classes([AllowAny])
def verify_otp(request):

    serializer = VerifyOTPSerializer(data=request.data)

    serializer.is_valid(
        raise_exception=True
    )

    email = serializer.validated_data['email']
    otp = serializer.validated_data['otp']

    # ======================================
    # FIND USER
    # ======================================

    try:

        user = User.objects.get(
            email=email
        )

    except User.DoesNotExist:

        return Response(
            {
                'error': 'User not found'
            },
            status=status.HTTP_404_NOT_FOUND
        )

    try:

        otp_record = EmailOTP.objects.get(
            user=user
        )

    except EmailOTP.DoesNotExist:

        return Response(
            {
                'error': 'OTP not found'
            },

            status=status.HTTP_400_BAD_REQUEST
        )

    # ======================================
    # CHECK ALREADY VERIFIED
    # ======================================

    if otp_record.is_verified:

        return Response(
            {
                'message':
                'Email is already verified'
            },

            status=status.HTTP_200_OK
        )

    # ======================================
    # CHECK OTP EXPIRY
    # ======================================

    expiry_time = (
        otp_record.created_at
        + timedelta(minutes=5)
    )

    if timezone.now() > expiry_time:

        return Response(
            {
                'error':
                'OTP has expired. '
                'Please request a new OTP.'
            },

            status=status.HTTP_400_BAD_REQUEST
        )

    # ======================================
    # CHECK OTP
    # ======================================

    if otp_record.otp != otp:

        return Response(
            {
                'error': 'Invalid OTP'
            },

            status=status.HTTP_400_BAD_REQUEST
        )

    # ======================================
    # VERIFY EMAIL
    # ======================================

    otp_record.is_verified = True

    otp_record.save(
        update_fields=['is_verified']
    )

    return Response(
        {
            'message':
            'Email verified successfully'
        },

        status=status.HTTP_200_OK
    )