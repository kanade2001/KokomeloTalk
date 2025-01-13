import sys
# 感情判断
from .emotion_estimate import analyze_emotion
# 音楽推薦
from .music_search import main

def out(input_text):
    # 入力文から８つの感情と数値を辞書型で取得
    out_dict_ud = analyze_emotion(input_text)
    emotion_scores = {item[0]: item[1] for item in out_dict_ud}
    # 音楽推薦情報を辞書型で取得
    recommended_tracks = main(emotion_scores)
    # out_dict2 = A(out_dict)
    return generate_conv(recommended_tracks)

# 会話の生成(返り値：文字列)
def generate_conv(recommended_tracks):
    if not recommended_tracks:
        return "申し訳ありません、適切な音楽を見つけることができませんでした。"
    
    # 得られた音楽情報から曲名，アーティスト名，ID情報を取得し，応答文を生成する
    response = "そんなことがあったんだね。今の君におすすめの曲があるよ！\n"

    for idx, track in enumerate(recommended_tracks[:3], start=1):
        track_name = track.get('name', '不明')
        artist_name = track.get('artists', '不明')
        track_id = track.get('id', 'N/A')
        
        # Spotifyのリンク生成（IDを使用）
        track_url = f"https://open.spotify.com/track/{track_id}" if track_id != 'N/A' else "リンク情報がありません。"
        
        # 応答文に追加
        response += (
            f"\n{idx}. 曲名：{track_name}\n"
            f"   アーティスト：{artist_name}\n"
            f"   曲のリンク：{track_url}\n"
        )
    return response

def system():
    count = 0
    while(True):
        if count == 0: # 会話の最初
            print("\nこんにちは！最近どう？")
            count = 1
        else:
            print("きっと君の助けになると思う！是非聞いてみて！\n")
            print("他には最近何かあった？")
        
        input_text = input(">>")
        # 終了条件
        if input_text == "もう終わります":
            print("またいつでも話しにきてね！")
            sys.exit()
        # フロントからの入力をout関数に
        else:
            response = out(input_text)
            print(response)    

if __name__ == "__main__":
    system()
