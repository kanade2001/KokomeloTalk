from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from app.modules import analyze_emotion
from app.modules import music_search

class ConversationView(APIView):
    def post(self, request):
        response_body = []
        
        request_text = request.data['text'] # フロントからの入力
        
        out_dict_ud = analyze_emotion(request_text)
        emotion_scores = {item[0]: item[1] for item in out_dict_ud}
        max_emotion_str = max(emotion_scores, key = emotion_scores.get)
        
        response_body.append({"type": "server", "text":  f"\"{max_emotion_str}\"の感情を感じられたよ"})
        response_body.append({"type": "server", "text": "今おすすめの曲はこれ！"})
        
        recommended_tracks = music_search(emotion_scores)
        
        for i in range(3):
            response_body.append({
                "type": "music",
                "id": recommended_tracks[i]['id'],
                "text": recommended_tracks[i]['name'],
                "music_artist": recommended_tracks[i]['artists'],
                "music_url": f"https://open.spotify.com/track/{recommended_tracks[i]['id']}"
            })
        
        # debug = [{"type": "server", "text": "感情が観測されました"}, {"type": "music", "text": "おすすめの曲"}]

        if True:
            return Response(response_body, status=status.HTTP_201_CREATED)
        return Response(status=status.HTTP_400_BAD_REQUEST)