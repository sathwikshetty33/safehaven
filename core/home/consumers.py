from asgiref.sync import sync_to_async
from channels.generic.websocket import AsyncWebsocketConsumer
import json
from .models import ngo, ChatMessage
from django.contrib.auth.models import User

class ChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.room_name = "public"
        self.room_group_name = "chat_%s" % self.room_name

        # Join room group
        await self.channel_layer.group_add(
            self.room_group_name,
            self.channel_name
        )
        await self.accept()

    async def disconnect(self, close_code):
        # Leave room group
        await self.channel_layer.group_discard(
            self.room_group_name,
            self.channel_name
        )

    async def receive(self, text_data):
        text_data_json = json.loads(text_data)
        message = text_data_json["message"]
        username = self.scope["user"]

        # Ensure the user is authenticated and verified as part of the NGO
        if not username.is_authenticated:
            await self.send(text_data=json.dumps({"error": "Authentication required"}))
            return

        ngo_user = await sync_to_async(ngo.objects.filter)(
            username=username, verified=True
        )

        if not await sync_to_async(ngo_user.exists)():
            await self.send(text_data=json.dumps({"error": "Access denied"}))
            return

        # Save message to the database
        await sync_to_async(ChatMessage.objects.create)(
            user=username, message=message
        )

        # Broadcast message to the group
        await self.channel_layer.group_send(
            self.room_group_name,
            {
                "type": "chat_message",
                "message": message,
                "user": username.username,
            }
        )

    async def chat_message(self, event):
        message = event["message"]
        user = event["user"]

        # Send message to WebSocket
        await self.send(text_data=json.dumps({
            "message": message,
            "user": user,
        }))
