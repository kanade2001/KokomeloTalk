import sqlite3
import math
import csv
import os

# 感情と対応する音響特徴量のマッピング (目標値、重み)
EMOTION_FEATURES = {
    "喜び": {
        'genre': ['k-pop', 'pop'],
        'features': {
            'danceability': {'value': 0.7, 'weight': 1.0},
            'energy': {'value': 0.7, 'weight': 1.0},
            'valence': {'value': 0.7, 'weight': 1.0},
            # 'tempo': {'value': 140, 'weight': 1.0}  # オプション
        }
    },
    "悲しみ": {
        'genre': ['classical', 'blues', 'slow_pop'],
        'features': {
            'danceability': {'value': 0.0, 'weight': 0.4},
            'energy': {'value': 0.0, 'weight': 0.4},
            'valence': {'value': 0.0, 'weight': 0.4},
            # 'tempo': {'value': 80, 'weight': 1.0}  # オプション
        }
    },
    "怒り": {
        'genre': ['rock', 'metal', 'hip-hop'],
        'features': {
            'danceability': {'value': 0.5, 'weight': 1.0},
            'energy': {'value': 0.8, 'weight': 1.0},
            'valence': {'value': 0.0, 'weight': 0.3},
            # 'tempo': {'value': 140, 'weight': 1.0}  # オプション
        }
    },
    "恐れ": {
        'genre': ['ambient', 'dark_electronic', 'jazz'],
        'features': {
            'danceability': {'value': 0.0, 'weight': 0.3},
            'energy': {'value': 0.3, 'weight': 0.6},
            'valence': {'value': 0.0, 'weight': 0.4},
            # 'tempo': {'value': 90, 'weight': 1.0}  # オプション
        }
    },
    "嫌悪": {
        'genre': ['hard_rock', 'industrial', 'trap'],
        'features': {
            'danceability': {'value': 0.5, 'weight': 1.0},
            'energy': {'value': 0.8, 'weight': 1.0},
            'valence': {'value': 0.0, 'weight': 0.3},
            # 'tempo': {'value': 140, 'weight': 1.0}  # オプション
        }
    },
    "驚き": {
        'genre': ['electronic', 'experimental', 'jazz'],
        'features': {
            'danceability': {'value': 0.4, 'weight': 0.8},
            'energy': {'value': 0.5, 'weight': 0.9},
            'valence': {'value': 0.3, 'weight': 0.7},
            # 'tempo': {'value': 120, 'weight': 1.0}  # オプション
        }
    },
    "信頼": {
        'genre': ['soul', 'r&b', 'soft_pop'],
        'features': {
            'danceability': {'value': 0.5, 'weight': 0.8},
            'energy': {'value': 0.5, 'weight': 0.8},
            'valence': {'value': 0.5, 'weight': 0.8},
            # 'tempo': {'value': 110, 'weight': 1.0}  # オプション
        }
    },
    "期待": {
        'genre': ['pop', 'dance', 'synthwave'],
        'features': {
            'danceability': {'value': 0.6, 'weight': 1.0},
            'energy': {'value': 0.6, 'weight': 1.0},
            'valence': {'value': 0.6, 'weight': 1.0},
            # 'tempo': {'value': 130, 'weight': 1.0}  # オプション
        }
    },
}

def download_database(workspace, database_name):
    database_path = f'{workspace}/{database_name}.db'

    if database_name == "full_dataset": #全曲版
        file_id = "1qk8HswEoFL1jDkO_tIQpa0BuGbDgVWTb"
    elif database_name == "filtered_dataset": #一部日本アーティストの曲のみ抽出
        file_id = "1TCYICRkTvct-e7Kahk6VwHpjZHQtez9N"
    elif database_name == "filtered_v3_dataset": #一部日本アーティストの曲+多様なジャンルの曲から抽出
        file_id = "1CwnGQZZnOu-u623ysB12vlpj2mzjUBRa"
    else:
        raise ValueError("無効なデータベース名です。")

    if os.path.exists(database_path):
        # print(f"データベース '{database_name}' は既に存在します。")
        return database_path
    else:
        # print(f"データベース '{database_name}' は存在しません。ダウンロードを開始します。")
        os.makedirs(workspace, exist_ok=True)
        # ダウンロード処理
        os.system(f'gdown "https://drive.google.com/uc?export=download&id={file_id}" -O "{database_path}"')
        return database_path

def initialize_and_save_database(database_path, database_name, csv_paths):
    if os.path.exists(database_path):
        # print(f"データベース '{database_name}' は既に存在します。初期化と保存をスキップします。")
        return

    conn = sqlite3.connect(database_path)
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS tracks (
            id TEXT PRIMARY KEY,
            name TEXT,
            artists TEXT,
            album TEXT,
            duration_ms INTEGER,
            popularity INTEGER,
            acousticness REAL,
            danceability REAL,
            energy REAL,
            instrumentalness REAL,
            key INTEGER,
            liveness REAL,
            loudness REAL,
            mode INTEGER,
            speechiness REAL,
            tempo REAL,
            time_signature INTEGER,
            valence REAL,
            genre TEXT
        )
    ''')

    tracks = read_tracks_from_csv(csv_paths)
    if not tracks:
        print("CSVからトラック情報を取得できませんでした。")
        conn.close()
        return

    for track in tracks:
        cursor.execute('''
            INSERT OR REPLACE INTO tracks (
                id, name, artists, album, duration_ms,
                popularity, acousticness, danceability, energy, instrumentalness, key,
                liveness, loudness, mode, speechiness, tempo, time_signature, valence, genre
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        ''', (
            track['id'],
            track['name'],
            track['artists'],
            track['album'],
            track['duration_ms'],
            track['popularity'],
            track['acousticness'],
            track['danceability'],
            track['energy'],
            track['instrumentalness'],
            track['key'],
            track['liveness'],
            track['loudness'],
            track['mode'],
            track['speechiness'],
            track['tempo'],
            track['time_signature'],
            track['valence'],
            track['track_genre']
        ))
    conn.commit()
    conn.close()
    # print(f"データベースに {len(tracks)} 曲を保存しました。")

def read_tracks_from_csv(csv_paths):
    tracks = []
    for csv_path in csv_paths:
        try:
            with open(csv_path, 'r', encoding='utf-8') as file:
                reader = csv.DictReader(file)
                for row in reader:
                    track = {
                        'id': row['track_id'],
                        'name': row['track_name'],
                        'artists': row['artists'],
                        'album': row['album_name'],
                        'duration_ms': int(row['duration_ms']) if row['duration_ms'] else None,
                        'popularity': int(row['popularity']) if row['popularity'] else None,
                        'acousticness': float(row['acousticness']) if row['acousticness'] else None,
                        'danceability': float(row['danceability']) if row['danceability'] else None,
                        'energy': float(row['energy']) if row['energy'] else None,
                        'instrumentalness': float(row['instrumentalness']) if row['instrumentalness'] else None,
                        'key': int(row['key']) if row['key'] else None,
                        'liveness': float(row['liveness']) if row['liveness'] else None,
                        'loudness': float(row['loudness']) if row['loudness'] else None,
                        'mode': int(row['mode']) if row['mode'] else None,
                        'speechiness': float(row['speechiness']) if row['speechiness'] else None,
                        'tempo': float(row['tempo']) if row['tempo'] else None,
                        'time_signature': int(row['time_signature']) if row['time_signature'] else None,
                        'valence': float(row['valence']) if row['valence'] else None,
                        'track_genre': row['track_genre'] if 'track_genre' in row else None
                    }
                    tracks.append(track)
        except FileNotFoundError:
            print(f"CSVファイル '{csv_path}' が見つかりません。")
        except Exception as e:
            print(f"CSVの読み込み中にエラーが発生しました: {e}")
    return tracks

def load_tracks_from_database(database_path, database_name, limit=100000, genres=None):
    if not os.path.exists(database_path):
        print(f"データベース '{database_name}' が存在しません。")
        return []

    conn = sqlite3.connect(database_path)
    cursor = conn.cursor()
    if genres:
        placeholders = ' OR '.join(['genre LIKE ?' for _ in genres])
        query = f'SELECT * FROM tracks WHERE {placeholders}'
        params = [f'%{genre}%' for genre in genres]
        cursor.execute(query, params)
    else:
        cursor.execute('SELECT * FROM tracks')
    rows = cursor.fetchall()
    columns = [description[0] for description in cursor.description] if rows else [
        'id', 'name', 'artists', 'album', 'duration_ms',
        'popularity', 'acousticness', 'danceability', 'energy',
        'instrumentalness', 'key', 'liveness', 'loudness', 'mode',
        'speechiness', 'tempo', 'time_signature', 'valence', 'genre'
    ]

    tracks = []
    for row in rows[:limit]:
        track = dict(zip(columns, row))
        tracks.append(track)

    conn.close()
    # print(f"データベースから {len(tracks)} 曲を読み込みました。")
    return tracks

def find_matching_tracks(tracks, target_features, top_n=3):
    if not tracks:
        print("曲が見つかりませんでした。")
        return

    for track in tracks:
        distance = 0
        feature_count = 0
        for feature, target in target_features.items():
            track_value = track.get(feature)
            target_value = target['value']
            target_weight = target['weight']
            if track_value is not None:
                distance += target_weight * ((track_value - target_value) ** 2)
                feature_count += 1
        if feature_count > 0:
            track['distance'] = math.sqrt(distance)
        else:
            track['distance'] = float('inf')  # 音響特徴量がない場合

    sorted_tracks = sorted(tracks, key=lambda x: x['distance'])
    top_tracks = sorted_tracks[:top_n]

    display_attributes = ["id", "name", "artists", "genre", "danceability", "valence", "energy", "distance"]
    # print(f"\nTop {top_n} 曲 (距離が近い順):\n")
    # for idx, track in enumerate(top_tracks, start=1):
    #     print(f"曲 {idx}:")
    #     for attr in display_attributes:
    #         print(f"  {attr}: {track.get(attr, 'N/A')}")
    #     print()

    return top_tracks

def main(emotion_scores, csv_paths=None, limit=3, genre_filter=True, determine_mode="max",
        #  workspace = '/content/drive/MyDrive/Colab Notebooks/database_kokomelotalk', database_name = "filtered_v3_dataset"):
        workspace = os.path.join(os.getcwd(), "database_kokomelotalk"), database_name = "filtered_v3_dataset"):
    """
    音楽推薦のメイン関数。
    emotion_scores: 感情とスコアの辞書
    workspace: dbファイルの保存フォルダ
    database_name: 使用するdbの名前
    """
    database_path = f'{workspace}/{database_name}.db'

    # データベースの初期化と保存
    if csv_paths:
        print(f"CSVファイルからトラック情報を読み込んでいます...")
        print(f"CSVファイルパス: {csv_paths}")
        initialize_and_save_database(database_path, database_name, csv_paths)
    else:
        # データベースのダウンロード
        database_path = download_database(workspace, database_name)

    # データベースからトラックを読み込む
    desired_features =  calculate_combined_features(emotion_scores, determine_mode=determine_mode)
    # print("データベースからトラックを読み込んでいます...")
    # print(f"ジャンルフィルタ: {genre_filter}")
    genres = desired_features.get('genre', None) if genre_filter else None
    tracks = load_tracks_from_database(database_path, database_name, genres=genres)
    if tracks:
        # print(f"\n目標とする音響特徴量: {desired_features}")
        return find_matching_tracks(tracks, desired_features['features'], top_n=limit)
    else:
        return None

def calculate_combined_features(emotion_scores, determine_mode="max"):
    """
    感情スコアに基づいて音響特徴量を加重平均し、混合した特徴量を計算します。

    Args:
        emotion_scores (dict): {感情: スコア} の辞書。
        limit (int): 表示するトラックの数。
        csv_paths (list of str, optional): CSVファイルのパスのリスト。
        database_name (str, optional): データベースファイル名。
        genre_filter (bool, optional): ジャンルフィルタを適用するかどうか。
        determine_mode (str, optional): 特徴量決定方式 ("max" または "weighted_ave")。

    Returns:
        任意: main関数の戻り値。
    """
    if not emotion_scores:
        # 感情スコアが空の場合、デフォルトの音響特徴量を使用
        combined_features = {'danceability': {'value': 0.5, 'weight': 1.0},
                             'energy': {'value': 0.5, 'weight': 1.0},
                             'valence': {'value': 0.5, 'weight': 1.0}}
    else:
        total_score = sum(emotion_scores.values())
        # print(f"特徴量決定方式: {determine_mode}")
        if determine_mode == "max":
            emotion = max(emotion_scores, key=emotion_scores.get)
            # print(f"(対象の感情：{emotion})")
            desired_features = EMOTION_FEATURES.get(emotion, {
                'genre': [],
                'features': {
                    'danceability': {'value': 0.5, 'weight': 1.0},
                    'energy': {'value': 0.5, 'weight': 1.0},
                    'valence': {'value': 0.5, 'weight': 1.0}
                }
            })
        elif determine_mode == "weighted_ave":
            # 各感情のスコア割合に応じて加重平均
            combined_features = {'genre': [], 'features': {'danceability': {'value': 0.0, 'weight': 0.0},
                                                           'energy': {'value': 0.0, 'weight': 0.0},
                                                           'valence': {'value': 0.0, 'weight': 0.0}}}
            for emotion, score in emotion_scores.items():
                weight = score / total_score
                base = EMOTION_FEATURES.get(emotion, {
                    'genre': [],
                    'features': {
                        'danceability': {'value': 0.5, 'weight': 1.0},
                        'energy': {'value': 0.5, 'weight': 1.0},
                        'valence': {'value': 0.5, 'weight': 1.0}
                    }
                })
                combined_features['genre'].extend(base['genre'])
                for feature in combined_features['features']:
                    combined_features['features'][feature]['value'] += base['features'][feature]['value'] * weight
                    combined_features['features'][feature]['weight'] += base['features'][feature]['weight'] * weight
            desired_features = combined_features

    # 音響特徴量を使用してmain関数を実行
    return desired_features

# def local_test(csv_paths=None, genre_filter=True, determine_mode="max",
#                database_name="filtered_dataset", workspace='/content/drive/MyDrive/Colab Notebooks/database_kokomelotalk'):
#     """
#     ローカルテスト用関数。感情スコアを指定して機能をテストします。

#     Args:
#         csv_paths (list of str, optional): CSVファイルのパスのリスト。
#         genre_filter (bool, optional): ジャンルフィルタを適用するかどうか。
#         determine_mode (str, optional): 特徴量決定方式 ("max" または "weighted_ave")。
#     """
#     emotion_list = ['喜び', '悲しみ', '怒り', '恐れ', '嫌悪', '驚き', '信頼', '期待']
#     for key in emotion_list:
#         emotion_scores = {emotion: 1.0 if emotion == key else 0.0 for emotion in emotion_list}
#         main(emotion_scores, limit=3, csv_paths=csv_paths, genre_filter=genre_filter,
#              determine_mode=determine_mode, database_name=database_name, workspace=workspace)
#     return

# if __name__ == "__main__":
#     #csv_paths = ["dataset.csv"]
#     workspace = '/Users/kaoriinoue/2024zyugyo/tishikizyohosyori/kokomerotalk/database_kokomelotalk'
#     database_name = "filtered_v3_dataset"
#     genre_filter = False
#     determine_mode = "max"  # "max" or "weighted_ave"
#     local_test(workspace=workspace, genre_filter=genre_filter, determine_mode=determine_mode, database_name=database_name)
