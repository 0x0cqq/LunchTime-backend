# chat/routing.py
from django.urls import re_path

from .consumers import chat_consumer
from .consumers import notice_consumer

websocket_urlpatterns = [
    re_path(r"ws/chat/$", chat_consumer.ChatConsumer.as_asgi()),
    re_path(r"ws/notice/$", notice_consumer.NoticeComsumer.as_asgi()),
]