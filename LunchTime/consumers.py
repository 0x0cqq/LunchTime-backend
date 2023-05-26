from datetime import datetime
import json

import channels.layers
from asgiref.sync import async_to_sync, sync_to_async
from channels.generic.websocket import WebsocketConsumer, AsyncWebsocketConsumer
from channels.db import database_sync_to_async
from .models import User, ChatMessage, UserInfo
from urllib.parse import parse_qsl
from typing import *

from backend.settings import MEDIA_URL, ROOT_URL

class ChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        # 获取
        query_params = dict(parse_qsl(self.scope['query_string'].decode('utf-8')))
        self.send_user_name = query_params['sender_name']
        try:
            self.send_user_id = await self.get_user_id_from_name(self.send_user_name)   
        except User.DoesNotExist:
            print("websocket: user does not exist")
            await self.close()
            return
        self.receive_user_name = query_params['receiver_name']
        try:
            self.receive_user_id = await self.get_user_id_from_name(self.receive_user_name)
        except User.DoesNotExist:
            print("websocket: user does not exist")
            await self.close()
            return
        # print the sender and receiver
        print(self.send_user_name, self.receive_user_name)
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

    @database_sync_to_async
    def get_user_id_from_name(self, user_name: str):
        try:
            user_id = User.objects.get(name=user_name).id
        except User.DoesNotExist:
            user_id = -1
        finally:
            return user_id

    @database_sync_to_async
    def get_user_name_from_id(self, user_id: int):
        try:
            image = User.objects.get(id=user_id).name
        except User.DoesNotExist:
            image = ""
        finally:
            return image
    
    @database_sync_to_async
    def get_user_image_from_id(self, user_id: int):
        try:
            image = UserInfo.objects.get(id=user_id).image
        except UserInfo.DoesNotExist:
            image = ""
        finally:
            return image

    @sync_to_async
    def transform_chat_to_json(self, chat_list: List[ChatMessage]):
        result = []
        for chat in chat_list:
            try:
                sender_name = User.objects.get(id=chat.sender_id).name
            except User.DoesNotExist:
                sender_name = ""
            try:
                sender_image = UserInfo.objects.get(id=chat.sender_id).image
            except UserInfo.DoesNotExist:
                sender_image = ""
            result.append(
                {
                    "user_name": sender_name,
                    "user_avatar": ROOT_URL + MEDIA_URL + "userImage/" + sender_image,
                    "content": chat.message,
                    "timestamp": chat.create_time.timestamp().__floor__(),
                }
            )                
        return result

    @database_sync_to_async
    def get_history(self, sender_id, receiver_id):
        # get all the messages sender_id to receiver_id or receiver_id to sender_id
        # the messages are ordered by create_time, most recent last
        # return a list of messages
        chat_list = ChatMessage.objects.filter(
            sender_id__in=[sender_id, receiver_id],
            receiver_id__in=[sender_id, receiver_id],
        ).order_by("-create_time")
        return chat_list
    

    async def receive(self, text_data):
        text_data_json = json.loads(text_data)
        if text_data_json["type"] == "message":
            message = text_data_json["message"]
            content = message["content"]
            # timestamp is in milliseconds
            time = datetime.now()

            # insert the message into the database

            await self.channel_layer.group_send(
                self.room_group_name,
                {
                    "type": "chat_message",
                    "sender_id": self.send_user_id,
                    "receiver_id": self.receive_user_id,
                    "content": content,
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
        content = event["content"]
        sender_id = event["sender_id"]
        receiver_id = event["receiver_id"]
        timestamp = event["timestamp"]

        if receiver_id == self.send_user_id:
            sender_name = await self.get_user_name_from_id(sender_id)
            sender_image = await self.get_user_image_from_id(sender_id)
            await self.send(
                text_data=json.dumps(
                    {
                        "type": "message",
                        "message": {
                            "user_name": sender_name,
                            "avatar": ROOT_URL + MEDIA_URL + "userImage/" + sender_image,
                            "content": content,
                            "timestamp": timestamp,
                        }
                    }
                )
            )
    
    
