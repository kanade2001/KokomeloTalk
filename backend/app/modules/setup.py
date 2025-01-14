# 必要なモジュールのインストール/インポート
import torch
import os
import gdown

device = torch.device('cuda:0' if torch.cuda.is_available() else 'cpu')

# フォルダIDを指定
folder_id = "1YmF_3TihtXOEELXUr_ShG1kT4rIIzgef"

# ダウンロード先ディレクトリ
# save_dir = "/content/trained_model"

save_dir = os.path.join(os.getcwd(), "trained_model")

if os.path.exists(save_dir):
    pass # 既にフォルダが存在する場合は何もしない
else:
    os.makedirs(save_dir)
    # gdownを使ってフォルダ全体をダウンロード
    gdown.download_folder(f"https://drive.google.com/drive/folders/{folder_id}", output=save_dir, quiet=False)

# モデルとトークナイザを読み込み
from transformers import AutoModelForSequenceClassification, AutoTokenizer
loaded_model = AutoModelForSequenceClassification.from_pretrained(save_dir)
loaded_tokenizer = AutoTokenizer.from_pretrained(save_dir)

# デバイスを指定
device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
loaded_model.to(device)

