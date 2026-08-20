from django.urls import path , include

from crud import views

urlpatterns = [
    path('create/', views.create , name= 'create_blog' ),
]
