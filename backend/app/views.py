from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from app.modules import out

class ConversationView(APIView):
    def post(self, request):
        print(request.data['text'])
        out(request.data['text'])
        
        output = out(request.data['text'])
        print(output)
        # serializer = ConversationSerializer(data=request.data)
        # if serializer.is_valid(): 
        # debug = [{"type": "server", "text": "感情が観測されました"}, {"type": "music", "text": "おすすめの曲"}]
        text = [{"type": "server", "text": output}]
        if True:
            return Response(text, status=status.HTTP_201_CREATED)
        return Response(status=status.HTTP_400_BAD_REQUEST)