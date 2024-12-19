from tkinter.font import names

from django.urls import path, include

from . import views

urlpatterns = [

    path('', views.register,name= 'reg'),
    path('login', views.login_view,name='login'),
    path('chat_create-<int:userid>', views.chatcreate, name='chatcreate'),
    path('chat-<str:convoid>/', views.chat, name='chat'),
    path('chat/', views.public_chat, name='public_chat'),
    path('chat/send/', views.send_message, name='send_message'),
    path('chat/get_messages/', views.get_messages, name='get_messages'),
    ]