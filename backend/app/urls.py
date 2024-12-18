from django.urls import path
from .views import ConversationView

urlpatterns = [
    path('conversation/', ConversationView.as_view(), name="conversation"),
]