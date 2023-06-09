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
def sendSystemNotice(notice_data: json):
    notice_data = json.loads(notice_data)
    # parse the notice_data
    type = notice_data["type"]
    user_id = notice_data["user_id"]
    target_user_id = notice_data["target_user_id"]
    content = notice_data["content"]
    # get user name by user_id
    # get target_user name by target_user_id
    try:
        user_name = User.objects.get(id=user_id).name
        target_user_name = User.objects.get(id=target_user_id).name
        channel_names = Client.objects.filter(user_name=target_user_name)
        for channel_name in channel_names:
            channel_layer = get_channel_layer()
            async_to_sync(channel_layer.send)(
                channel_name, {
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
    