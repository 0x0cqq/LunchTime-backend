import json
from ..models import ChatMessage, User, UserInfo
from django.http import HttpRequest, JsonResponse

"""
    notice_data: {
        "type": "comment" | "love" | "follow" | "chat",
        "user_id": int,
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
    except User.DoesNotExist:
        return JsonResponse({'status': False, 'message': 'user does not exist'})

    print("type: " + type + " user_name: " + str(user_name) + " target_user_name: " + str(target_user_name) + " content: " + content)
    pass