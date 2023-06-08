from rest_framework.views import APIView
from django.http import HttpRequest, JsonResponse
from ..models import ChatMessage, User, UserInfo

from backend.settings import ROOT_URL, MEDIA_URL

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
        # calculate the number of unread messages for each person
        unread_num = []
        for person in persons:
            unread_num.append(ChatMessage.objects.filter(sender_id=person, receiver_id=user_id, isRead=False).count())    
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
                'user_avatar': ROOT_URL + MEDIA_URL + "userImage/" + persons_user_image[i],
                'content': messages[i],
                'timestamp': timestamp[i],
                'unread_num': unread_num[i],
            } for i in range(len(persons))
        ]}
        return JsonResponse(chat_list)
    
    def post(self, request: HttpRequest):
        # get user name and target user name
        user_name = request.POST.get('user_name')
        target_user_name = request.POST.get('target_user_name')
        # get user id and target user id
        try:
            user = User.objects.get(name=user_name)
            target_user = User.objects.get(name=target_user_name)
        except User.DoesNotExist:
            return JsonResponse({'status': False, 'message': 'user does not exist'})
        user_id = user.id
        target_user_id = target_user.id
        # get all chat messages from target user to user
        chat_list = ChatMessage.objects.filter(sender_id=target_user_id, receiver_id=user_id)
        # set all chat messages to read
        for chat in chat_list:
            chat.isRead = True
            chat.save()
        return JsonResponse({'status': True})
