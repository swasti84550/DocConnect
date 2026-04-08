from django.urls import path
from .views import register, login, ProfileView, MessageListCreateView, MessageReadUpdateView

urlpatterns = [
    path('register/', register, name='register'),
    path('login/', login, name='login'),
    path('profile/', ProfileView.as_view(), name='profile'),
    path('messages/', MessageListCreateView.as_view(), name='messages-list-create'),
    path('messages/<int:pk>/read/', MessageReadUpdateView.as_view(), name='messages-read'),
]
