
from django.urls import path , include

from crud import views

urlpatterns = [
    path('create/', views.blog_create , name= 'create_blog' ),
    path('update/<str:name>/', views.blog_update , name='update_blog'),
    path('delete/<str:name>/', views.blog_delete , name='delete_blog'),
    path('show/', views.blog_show , name='show_blog'),
    path('registration/' , views.registration , name='register'),
    path('login/' , views.login , name = 'login_blog'),
    path('token/refresh/' , views.referesh_token , name = 'token_refresh' )
]
