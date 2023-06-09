import json
from ..models import ChatMessage, User, UserInfo, Client
from django.http import HttpRequest, JsonResponse
from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync, sync_to_async



"""
notice_data: {
    "user_id": int,
    "type": "comment" | "love" | "follow" | "chat",
    "target_user_id": int,
    "content": str,
}
"""
def sendSystemNotice(notice_data: str):
    notice_data = json.loads(notice_data)
    # parse the notice_data
    type = notice_data["type"]
    user_id = notice_data["user_id"]
    target_user_id = notice_data["target_user_id"]
    content = notice_data["content"]
    if(type == "comment"):
        content = "评论了你的帖子：" + content
    elif(type == "chat"):
        content = "给你发了一条消息：" + content
    # get user name by user_id
    # get target_user name by target_user_id
    try:
        user_name = User.objects.get(id=user_id).name
        target_user_name = User.objects.get(id=target_user_id).name
        clients = Client.objects.filter(user_id=target_user_id)
        for client in clients:
            channel_layer = get_channel_layer()
            async_to_sync(channel_layer.send)(
                client.channel_name, {
                    "type": "notice.send",
                    "text": json.dumps(
                        {
                            "type": type,
                            "user_name": user_name,
                            "content": content,
                            "url": ""
                        }            
                    )                
                }
            )

    except User.DoesNotExist:
        pass
    except Client.DoesNotExist:
        pass
    finally:
        pass
