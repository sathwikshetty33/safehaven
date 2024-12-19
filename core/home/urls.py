from tkinter.font import names

from django.urls import path, include

from . import views

urlpatterns = [

    path('', views.register,name= 'reg'),
    path('login', views.login_view,name='login'),
    path('chat_create-<int:userid>', views.chatcreate, name='chatcreate'),
    path('chat-<str:convoid>/', views.chat, name='chat'),
    ]