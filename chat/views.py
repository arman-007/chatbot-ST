from rest_framework import generics, permissions
from .models import ChatHistory
from .serializers import ChatHistorySerializer
from rest_framework.response import Response
from rest_framework import status
from .rag_service import rag_service_instance


class ChatView(generics.GenericAPIView):
    """
    Endpoint to send a message to the chatbot and get a response. 
    """
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request, *args, **kwargs):
        user_message = request.data.get("message")
        if not user_message:
            return Response({"error": "Message is required"}, status=status.HTTP_400_BAD_REQUEST)

        retrieved_docs = rag_service_instance.retrieve_documents(user_message)

        chatbot_response = rag_service_instance.generate_response(user_message, retrieved_docs)

        ChatHistory.objects.create(
            user=request.user,
            user_message=user_message,
            chatbot_response=chatbot_response
        )

        return Response({"response": chatbot_response}, status=status.HTTP_200_OK)


class ChatHistoryView(generics.ListAPIView):
    """
    Endpoint to retrieve chat history for the logged-in user. 
    """
    serializer_class = ChatHistorySerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return ChatHistory.objects.filter(user=self.request.user).order_by('timestamp')