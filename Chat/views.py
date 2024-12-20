import datetime
from django.shortcuts import render, redirect
from rest_framework.views import APIView
from rest_framework.response import Response
from .models import Message
from rest_framework.status import HTTP_200_OK, HTTP_400_BAD_REQUEST
from django.contrib.auth.models import User

def chatPage(request, *args, **kwargs):
    if not request.user.is_authenticated:
        return redirect("login-user")
    context = {}
    return render(request, "chat/chatPage.html", context)

class GetChatPage(APIView):
    def post(self, request, *args, **kwargs):
        username = request.data.get("username")
        print(username)
        if not request.user.is_authenticated:
            return redirect("login-user")
        to_userId = User.objects.get(username=username).id
        toMessages = Message.objects.filter(toUser=request.user.id).values()
        fromMessages = Message.objects.filter(fromUser=request.user.id).values()
        context = {"userId": request.user.id, "to_userId": to_userId, "userName": username.capitalize(), "toMessages": toMessages, "fromMessages": fromMessages}
        return render(request, "chat/userChat.html", context)

class SendMessage(APIView):
    def post(self, request, *args, **kwargs):
        data = request.data
        print(data)
        userId = request.user.id
        print(userId)
        to_user = User.objects.get(id=int(data['toUser']))
        from_user = User.objects.get(id=userId)
        timeStamp = datetime.datetime.strptime(data['timeStamp'], "%d/%m/%Y, %H:%M:%S")
        print(timeStamp)
        try:
            newMessage = Message.objects.create(fromUser=from_user, toUser=to_user, message=data["message"], date=timeStamp)
            print('created')
        except Exception as e:
            print(e)
            return Response({"status": "error", "exception":e}, status=HTTP_400_BAD_REQUEST)
        return Response({"status": "success"}, status=HTTP_200_OK)

class GetSessionMessages(APIView):
    def post(self, request, *args, **kwargs):
        selfUser = request.user
        toUserId = request.data.get('toUserId','')
        if selfUser.id == int(toUserId):
            return Response([], status=HTTP_200_OK)
        time = request.data.get('time','')
        time = datetime.datetime.strptime(time, "%d/%m/%Y, %H:%M:%S")
        toMessages = Message.objects.filter(toUser=selfUser, fromUser=toUserId, date__gte = time).values('message', 'date', 'fromUser__username', 'toUser__username').order_by('date')
        return Response(list(toMessages), status=HTTP_200_OK)

class GetMessages(APIView):
    def post(self, request, *args, **kwargs):
        selfUser = request.user
        toUserId = request.data.get('toUserId','')
        print(selfUser.id, toUserId)
        if selfUser.id == int(toUserId):
            messages = Message.objects.filter(fromUser=selfUser, toUser=toUserId).values('message', 'date', 'fromUser__username', 'toUser__username').order_by('date')
            return Response(list(messages), status=HTTP_200_OK)
        toMessages = Message.objects.filter(toUser=selfUser, fromUser=toUserId).values('message', 'date', 'fromUser__username', 'toUser__username').order_by('date')
        fromMessages = Message.objects.filter(fromUser=selfUser, toUser=toUserId).values('message', 'date', 'fromUser__username', 'toUser__username').order_by('date')
        allMessages = sorted(
            list(toMessages) + list(fromMessages),
            key=lambda x: x['date']
        )
        print(allMessages)
        # messages = {"toMessages": list(toMessages), "fromMessages": list(fromMessages)}
        return Response(allMessages, status=HTTP_200_OK)

class GetUsers(APIView):
    def get(self, request, *args, **kwargs):
        users = User.objects.all().values('id', 'username', 'email')
        users = list(users)
        return Response(users, status=HTTP_200_OK)