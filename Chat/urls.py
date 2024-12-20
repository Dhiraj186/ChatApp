from django.urls import path, include
from Chat import views as chat_views
from django.contrib.auth.views import LoginView, LogoutView

urlpatterns = [
    path("", chat_views.chatPage, name="chat-page"),

    # authentication section
    path("auth/login/", LoginView.as_view
         (template_name="chat/loginPage.html"), name="login-user"),
    path("auth/logout/", LogoutView.as_view(), name="logout-user"),
    path('sendMessage/', chat_views.SendMessage.as_view(), name='send-message'),
    path('getUsers/', chat_views.GetUsers.as_view(), name='get-users'),
    path('getChatPage/', chat_views.GetChatPage.as_view(), name='user-chat'),
    path('getMessages/', chat_views.GetMessages.as_view(), name='get-messages'),
    path('getSessionMessages/', chat_views.GetSessionMessages.as_view(), name='get-session-messages'),
]