from tkinter.font import names

from django.urls import path, include

from . import views

urlpatterns = [

    path('', views.register,name= 'reg'),
    path('login', views.login_view,name='login'),
    path('chat_create', views.chatcreate, name='chatcreate'),
    path('chat-<str:convoid>/', views.chat, name='chat'),
    path('chat/', views.public_chat, name='public_chat'),
    path('chat/send/', views.send_message, name='send_message'),
    path('chat/get_messages/', views.get_messages, name='get_messages'),
    path('shelter/',views.shelter_view,name="shelter"),
    path('distress/',views.distress_view,name='distress'),
    path('dis-delete/<str:did>',views.disdel,name='disdel'),
    path('home/',views.home,name='home'),
    path('earthquake/',views.earthquake,name='earthquake'),
    path('flood/',views.floods,name='flood'),
    path('tsunami/',views.tsunami,name='tsunami'),
    path('submit-distress/', views.submit_distress, name='submit_distress'),
    ]