from channels.generic.websocket import WebsocketConsumer, AsyncWebsocketConsumer
from ..models import User, Client
from urllib.parse import parse_qsl

class NoticeComsumer(WebsocketConsumer):
    def connect(self):
        query_params = dict(parse_qsl(self.scope['query_string'].decode('utf-8')))
        user_name = query_params['user_name']
        user_id = User.objects.get(name=user_name).id
        this_client = Client(user_id=user_id, channel_name=self.channel_name)
        this_client.save()
        self.accept()
    
    def disconnect(self, close_code):
        Client.objects.filter(channel_name=self.channel_name).delete()
    
    def notice_send(self, event):
        self.send(text_data=event['text'])