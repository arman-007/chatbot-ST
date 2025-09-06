from datetime import timedelta
from django.utils import timezone
from .models import ChatHistory


def delete_old_chat_history():
    """
    Deletes chat history older than 30 days. 
    """
    thirty_days_ago = timezone.now() - timedelta(days=30)
    old_chats = ChatHistory.objects.filter(timestamp__lt=thirty_days_ago)
    count = old_chats.count()
    old_chats.delete()
    print(f"Deleted {count} old chat history records.")