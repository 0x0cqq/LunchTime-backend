from rest_framework.views import APIView
from django.http import HttpRequest, JsonResponse
from ..models import ChatMessage, User, UserInfo

# Persons chat with someone
class ChatListView(APIView):
    # Input: person username (str)
    # Output: list of chated persons and a most recent message (list of (username, message)))
    def get(self, request: HttpRequest):
        username = request.GET.get('user_name')
        try:
            user = User.objects.get(name=username)
        except User.DoesNotExist:
            return JsonResponse({'status': False, 'message': 'user does not exist'})
        user_id = user.id
        # use user to filter all chat messages, in receiver or sender field
        chat_list = ChatMessage.objects.filter(sender_id=user_id)
        chat_list = chat_list | ChatMessage.objects.filter(receiver_id=user_id)
        chat_list = chat_list.order_by('-create_time')
        # get all persons chated with
        persons, messages, timestamp = [], [], []
        for chat in chat_list:
            if chat.sender_id == user_id:
                if chat.receiver_id not in persons:
                    persons.append(chat.receiver_id)
                    messages.append(chat.message)
                    timestamp.append(chat.create_time.timestamp().__floor__())
            else:
                if chat.sender_id not in persons:
                    persons.append(chat.sender_id)
                    messages.append(chat.message)
                    timestamp.append(chat.create_time.timestamp().__floor__())
        # get all persons' username & image by id
        persons_user_name = [
            User.objects.get(id=person_id).name for person_id in persons
        ]
        persons_user_image = [
            UserInfo.objects.get(id=person_id).image for person_id in persons
        ]
        # combine all information into a dict
        chat_list = {
            'status': True,
            'chat_list': [ {
                'user_name': persons_user_name[i],
                'user_avatar': persons_user_image[i],
                'content': messages[i],
                'timestamp': timestamp[i]
            } for i in range(len(persons))
        ]}
        return JsonResponse(chat_list)
