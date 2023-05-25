from datetime import datetime
import json

import channels.layers
from asgiref.sync import async_to_sync, sync_to_async
from channels.generic.websocket import WebsocketConsumer, AsyncWebsocketConsumer
from channels.db import database_sync_to_async
from .models import User, ChatMessage

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
    
    @database_sync_to_async
    def insert_message(self, chat_message: ChatMessage):
        chat_message.save()

    @sync_to_async
    def transform_chat_to_json(self, chat_list):
        return [
            {
                "sender_id": chat.sender_id,
                "message": chat.message,
                "timestamp": chat.create_time.timestamp().__floor__(),
            }
            for chat in chat_list
        ]

    @database_sync_to_async
    def get_history(self, sender_id, receiver_id):
        # get all the messages between the sender and receiver, both way
        # the messages are ordered by create_time, most recent last
        # return a list of messages
        return ChatMessage.objects.filter(
            sender_id__in=[sender_id, receiver_id],
            receiver_id__in=[sender_id, receiver_id],
        ).order_by("create_time")
    

    async def receive(self, text_data):
        text_data_json = json.loads(text_data)
        if text_data_json["type"] == "message":
            message = text_data_json["message"]
            content = message["message"]
            # timestamp is in milliseconds
            time = datetime.now()

            # insert the message into the database

            await self.channel_layer.group_send(
                self.room_group_name,
                {
                    "type": "chat_message",
                    "sender_id": self.send_user_id,
                    "receiver_id": self.receive_user_id,
                    "message": content,
                    "timestamp": time.timestamp().__floor__(),
                },
            )
            
            await self.insert_message(ChatMessage(
                sender_id=self.send_user_id,
                receiver_id=self.receive_user_id,
                message=content,
                create_time=time,
            ))
        elif text_data_json["type"] == "history":
            chat_list = await self.get_history(self.send_user_id, self.receive_user_id)
            chat_list = await self.transform_chat_to_json(chat_list)
            await self.send(
                text_data=json.dumps(
                    {
                        "type": "history",
                        "history": chat_list 
                    }
                )
            )
        else:
            return


    
    async def chat_message(self, event):
        message = event["message"]
        sender_id = event["sender_id"]
        receiver_id = event["receiver_id"]
        timestamp = event["timestamp"]

        if receiver_id == self.send_user_id:
            await self.send(
                text_data=json.dumps(
                    {
                        "type": "message",
                        "message": {
                            "sender_id": sender_id,
                            "message": message,
                            "timestamp": timestamp,
                        }
                    }
                )
            )
    
    
