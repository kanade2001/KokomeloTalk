from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

class ConversationView(APIView):
    def post(self, request):
        # serializer = ConversationSerializer(data=request.data)
        # if serializer.is_valid(): 
        debug = [{"type": "server", "text": "感情が観測されました"}, {"type": "music", "text": "おすすめの曲"}]
        if True:
            return Response(debug, status=status.HTTP_201_CREATED)
        return Response(status=status.HTTP_400_BAD_REQUEST)