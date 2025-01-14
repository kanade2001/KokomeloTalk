import numpy as np
from .setup import loaded_model
from .setup import loaded_tokenizer

# 感情名（日本語）を定義
emotion_names_jp = ['喜び', '悲しみ', '怒り', '恐れ', '嫌悪', '驚き', '信頼', '期待'] # 例として8つの感情を想定

# ソフトマックス関数
def np_softmax(x):
    f_x = np.exp(x) / np.sum(np.exp(x))
    return f_x

def analyze_emotion(text):
    # 推論モードを有効化
    loaded_model.eval()

    # 入力データ変換 + 推論
    tokens = loaded_tokenizer(text, truncation=True, return_tensors="pt")
    tokens.to(loaded_model.device)
    preds = loaded_model(**tokens)
    prob = np_softmax(preds.logits.cpu().detach().numpy()[0])
    out_dict = {n: p for n, p in zip(emotion_names_jp, prob)}
    out_dict_ud = sorted(out_dict.items(), key=lambda x:x[1], reverse=True)

    # print("入力文：", text)
    # print(out_dict_ud)

    return out_dict_ud

# 感情推定する文の入力
# analyze_emotion(input())
