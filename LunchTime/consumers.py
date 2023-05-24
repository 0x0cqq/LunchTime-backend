import json

import channels.layers
from asgiref.sync import async_to_sync
from channels.generic.websocket import WebsocketConsumer, AsyncWebsocketConsumer


class ChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.send_user_id = self.scope["url_route"]["kwargs"]["sender_id"]
        self.receive_user_id = self.scope["url_route"]["kwargs"]["receiver_id"]
        # generate a group name determined by the sender and receiver, discarding the order
        self.room_group_name = (
            f"chat_{min(self.send_user_id, self.receive_user_id)}_{max(self.send_user_id, self.receive_user_id)}"
        )
        print(self.send_user_id, self.receive_user_id)
        await self.channel_layer.group_add(
            self.room_group_name, self.channel_name
        )
        await self.accept()

    async def disconnect(self, close_code):
        await self.channel_layer.group_discard(
            self.room_group_name, self.channel_name
        )

    async def receive(self, text_data):
        text_data_json = json.loads(text_data)
        sender_id: int = text_data_json["sender_id"]
        message: str = text_data_json["message"]
        timestamp: int = text_data_json["timestamp"]

        await self.channel_layer.group_send(
            self.room_group_name,
            {
                "type": "chat_message",
                "message": message,
                "sender_id": self.send_user_id,
                "receiver_id": self.receive_user_id,
                "timestamp": timestamp,
            },
        )
    
    async def chat_message(self, event):
        message = event["message"]
        sender_id = event["sender_id"]
        receiver_id = event["receiver_id"]
        timestamp = event["timestamp"]

        if receiver_id == self.send_user_id:
            await self.send(
                text_data=json.dumps(
                    {
                        "message": message,
                        "sender_id": sender_id,
                        "timestamp": timestamp,
                    }
                )
            )
    
    
