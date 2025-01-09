import sqlite3
import math
import csv
import os

# 感情と対応する音響特徴量のマッピング (目標値、重み)
# EMOTION_FEATURES は感情に紐づく推奨ジャンルと音響特徴量の目標値を定義する辞書。
# 例: "喜び" はジャンル ['k-pop', 'pop']、danceability=0.7, energy=0.7, valence=0.7 など。
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

def main(emotion_scores, workspace = '/content/drive/MyDrive/Colab Notebooks/database_kokomelotalk',
         database_name = "filtered_v3_dataset", limit=3, genre_filter=False, determine_mode="max", csv_paths=None):
    """
    音楽推薦のメイン関数。
    感情スコアをもとに音響特徴量を算出し、データベースからマッチング度の高い楽曲を取得する。

    Args:
        emotion_scores (dict): 感情名をキー、スコア（float）を値とする辞書。
        workspace (str, optional): データベースファイルの保存ディレクトリ。デフォルトはColab想定。
        database_name (str, optional): 使用するデータベースファイル名。デフォルトは "filtered_v3_dataset.db"。
        limit (int, optional): 推薦曲を何件返すか。デフォルトは3。
        genre_filter (bool, optional): True の場合、感情に対応するジャンルに絞り込みを行う。デフォルトは False。
        determine_mode (str, optional): "max" または "weighted_ave" を指定。
                                        "max"=最もスコアの高い感情を採用、"weighted_ave"=複数感情を加重平均。
        csv_paths (list of str, optional): CSVファイルのパスリスト。指定があればDB作成を行う。

    Returns:
        list of dict または None: find_matching_tracks()関数で得られた上位limit件のトラック情報。
                                曲が存在しない場合は None を返す。
    """
    database_path = f'{workspace}/{database_name}.db'

    # CSVパスが指定されている場合、新規データベースを作成して保存。
    # 指定がなければ既存データベースをダウンロードして使用。
    if csv_paths:
        print(f"CSVファイルからトラック情報を読み込んでいます...")
        print(f"CSVファイルパス: {csv_paths}")
        initialize_and_save_database(database_path, database_name, csv_paths)
    else:
        database_path = download_database(workspace, database_name)

    # 感情スコアに基づいて目標音響特徴量を計算
    desired_features =  calculate_combined_features(emotion_scores, determine_mode=determine_mode)
    print("データベースからトラックを読み込んでいます...")
    print(f"ジャンルフィルタ: {genre_filter}")
    # genre_filterが有効ならジャンルを設定
    genres = desired_features.get('genre', None) if genre_filter else None
    # DBからトラックを読み込み
    tracks = load_tracks_from_database(database_path, database_name, genres=genres)
    if tracks:
        print(f"\n目標とする音響特徴量: {desired_features}")
        return find_matching_tracks(tracks, desired_features['features'], top_n=limit)
    else:
        return None

def local_test(csv_paths=None, genre_filter=True, determine_mode="max",
               database_name="filtered_dataset", workspace='/content/drive/MyDrive/Colab Notebooks/database_kokomelotalk'):
    """
    全8感情を順次テストし、各感情における推奨曲が正しく取得されるかを確認するローカルテスト用関数。

    Args:
        csv_paths (list of str, optional): CSVファイルのパスリスト。
        genre_filter (bool, optional): ジャンルフィルタを適用するかどうか。
        determine_mode (str, optional): 特徴量決定方式 ("max" または "weighted_ave")。
        database_name (str, optional): 使用するデータベースファイル名。
        workspace (str, optional): データベースファイルを保存または読み込むディレクトリ。

    Returns:
        なし（コンソール出力のみ）。
    """
    emotion_list = ['喜び', '悲しみ', '怒り', '恐れ', '嫌悪', '驚き', '信頼', '期待']
    for key in emotion_list:
        # 各実行で、テスト対象感情のみスコア=1.0、他は0.0とする。
        emotion_scores = {emotion: 1.0 if emotion == key else 0.0 for emotion in emotion_list}
        main(emotion_scores, limit=3, csv_paths=csv_paths, genre_filter=genre_filter,
             determine_mode=determine_mode, database_name=database_name, workspace=workspace)
    return

def initialize_and_save_database(database_path, database_name, csv_paths):
    """
    CSVファイルから曲情報を読み込み、新規にデータベースを作成・初期化してデータを格納する関数。
    すでに同名のデータベースファイルが存在する場合は作成をスキップする。

    Args:
        database_path (str): 新規作成または参照するデータベースファイルの絶対パス。
        database_name (str): データベース名を示す文字列（ログ表示などに使用）。
        csv_paths (list of str): 曲情報が入ったCSVファイルのパスリスト。

    Returns:
        なし（データをデータベースに書き込むのみ）。
    """
    # 既にデータベースが存在する場合、初期化処理をスキップ。
    if os.path.exists(database_path):
        print(f"データベース '{database_name}' は既に存在します。初期化と保存をスキップします。")
        return

    # データベースへ接続してテーブル 'tracks' を作成する。
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

    # CSVからトラック情報を読み込む
    tracks = read_tracks_from_csv(csv_paths)
    if not tracks:
        print("CSVからトラック情報を取得できませんでした。")
        conn.close()
        return

    # テーブルにトラック情報をINSERTする。
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
    print(f"データベースに {len(tracks)} 曲を保存しました。")

def read_tracks_from_csv(csv_paths):
    """
    指定したCSVファイルリスト(csv_paths)から曲情報を読み込み、辞書型リストとして返す関数。

    Args:
        csv_paths (list of str): CSVファイルへのパスを格納したリスト。

    Returns:
        list of dict: CSVから読み込んだトラック情報を要素とするリスト。
                      各要素は 'id', 'name', 'artists', 'album', 'duration_ms' など
                      必要な情報をキーとする辞書である。
    """
    tracks = []
    for csv_path in csv_paths:
        try:
            with open(csv_path, 'r', encoding='utf-8') as file:
                reader = csv.DictReader(file)
                for row in reader:
                    # CSV中の各行を辞書形式に変換し、tracksリストに追加する。
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

def download_database(workspace, database_name):
    """
    データベースファイルを Google Drive からダウンロードし、指定したディレクトリに配置する関数。
    すでに同名のデータベースファイルが存在する場合はダウンロードをスキップする。

    Args:
        workspace (str): ダウンロード先のディレクトリパス。
        database_name (str): ダウンロード対象データベースの名称。"full_dataset"、"filtered_dataset"、
                             "filtered_v3_dataset"のいずれか。

    Returns:
        str: ダウンロードまたは既存のデータベースファイルのパスを返す。

    Raises:
        ValueError: database_name に無効な名前が与えられた場合に発生。
    """
    database_path = f'{workspace}/{database_name}.db'

    # 指定されたデータベース名に応じて、Google Drive 上のファイルIDを切り替え。
    if database_name == "full_dataset": # 全曲版
        file_id = "1qk8HswEoFL1jDkO_tIQpa0BuGbDgVWTb"
    elif database_name == "filtered_dataset": # 一部日本アーティストのみ
        file_id = "1TCYICRkTvct-e7Kahk6VwHpjZHQtez9N"
    elif database_name == "filtered_v3_dataset": # 一部日本アーティスト + 多様なジャンル
        file_id = "1CwnGQZZnOu-u623ysB12vlpj2mzjUBRa"
    else:
        raise ValueError("無効なデータベース名です。")

    # 同名ファイルが既に存在するか確認し、なければダウンロードを実行。
    if os.path.exists(database_path):
        print(f"データベース '{database_name}' は既に存在します。")
    else:
        print(f"データベース '{database_name}' は存在しません。ダウンロードを開始します。")
        os.makedirs(workspace, exist_ok=True)
        # gdownコマンドを用いてGoogle Driveからファイルをダウンロード
        os.system(f'gdown "https://drive.google.com/uc?export=download&id={file_id}" -O "{database_path}"')

    return database_path


def calculate_combined_features(emotion_scores, determine_mode="max"):
    """
    感情スコア (emotion_scores) を用いて音響特徴量を計算する関数。
    "max" か "weighted_ave" を指定し、各感情に対応するEMOTION_FEATURESの値を組み合わせる。

    Args:
        emotion_scores (dict): {感情: スコア} の形式。
        determine_mode (str, optional): 音響特徴量の決定方式。
                                        "max"=スコア最大の感情を使用,
                                        "weighted_ave"=スコア比率で加重平均。

    Returns:
        dict: 統合した音響特徴量およびジャンルを含む辞書。以下の形式を想定。
        {
          'genre': [...],  # 抽出または加算されたジャンル
          'features': {
             'danceability': {'value': float, 'weight': float},
             'energy': {'value': float, 'weight': float},
             'valence': {'value': float, 'weight': float},
             ...
          }
        }
    """
    # 感情スコアが空の場合、デフォルト値を設定
    if not emotion_scores:
        combined_features = {
            'danceability': {'value': 0.5, 'weight': 1.0},
            'energy': {'value': 0.5, 'weight': 1.0},
            'valence': {'value': 0.5, 'weight': 1.0}
        }
    else:
        total_score = sum(emotion_scores.values())
        print(f"特徴量決定方式: {determine_mode}")
        if determine_mode == "max":
            # スコア最大の感情のみを対象とする
            emotion = max(emotion_scores, key=emotion_scores.get)
            print(f"対象の感情：{emotion}")
            desired_features = EMOTION_FEATURES.get(emotion, {
                'genre': [],
                'features': {
                    'danceability': {'value': 0.5, 'weight': 1.0},
                    'energy': {'value': 0.5, 'weight': 1.0},
                    'valence': {'value': 0.5, 'weight': 1.0}
                }
            })
        elif determine_mode == "weighted_ave":
            # すべての感情をスコア比率に基づいて加重平均
            combined_features = {
                'genre': [],
                'features': {
                    'danceability': {'value': 0.0, 'weight': 0.0},
                    'energy': {'value': 0.0, 'weight': 0.0},
                    'valence': {'value': 0.0, 'weight': 0.0}
                }
            }
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

    return desired_features

def load_tracks_from_database(database_path, database_name, limit=100000, genres=None):
    """
    SQLiteデータベースから指定条件に一致する曲情報を読み込み、辞書型リストとして返す関数。
    ジャンルフィルタを適用する場合、LIKE検索を用いる。

    Args:
        database_path (str): 既存のデータベースファイルのパス。
        database_name (str): データベース名を示す文字列（ログ表示などに使用）。
        limit (int, optional): 読み込む最大曲数。デフォルトは100000。
        genres (list of str, optional): ジャンルフィルタを行う際に用いる文字列のリスト。

    Returns:
        list of dict: データベースから取得したトラック情報を含む辞書のリスト。
                      取得件数がlimitを超える場合、先頭limit件のみ返す。
    """
    # データベースファイルが存在するかチェック
    if not os.path.exists(database_path):
        print(f"データベース '{database_name}' が存在しません。")
        return []

    conn = sqlite3.connect(database_path)
    cursor = conn.cursor()

    # ジャンルフィルタがある場合、placeholdersとparamsを生成してクエリを実行。
    if genres:
        placeholders = ' OR '.join(['genre LIKE ?' for _ in genres])
        query = f'SELECT * FROM tracks WHERE {placeholders}'
        params = [f'%{genre}%' for genre in genres]
        cursor.execute(query, params)
    else:
        cursor.execute('SELECT * FROM tracks')
    rows = cursor.fetchall()

    # カラム名を取得。曲が一件もない場合はデフォルトのカラム一覧を用意する。
    columns = [description[0] for description in cursor.description] if rows else [
        'id', 'name', 'artists', 'album', 'duration_ms',
        'popularity', 'acousticness', 'danceability', 'energy',
        'instrumentalness', 'key', 'liveness', 'loudness', 'mode',
        'speechiness', 'tempo', 'time_signature', 'valence', 'genre'
    ]

    # rows の各タプルを辞書に変換して格納。
    tracks = []
    for row in rows[:limit]:
        track = dict(zip(columns, row))
        tracks.append(track)

    conn.close()
    print(f"データベースから {len(tracks)} 曲を読み込みました。")
    return tracks

def find_matching_tracks(tracks, target_features, top_n=3):
    """
    与えられた曲リスト(tracks)と目標音響特徴量(target_features)に基づき、
    ユークリッド距離（加重）を用いて近い順にソートし、上位top_n件を抽出する関数。

    Args:
        tracks (list of dict): データベースやCSVから取得した曲情報。
        target_features (dict): 目標とする音響特徴量とその重みを持つ辞書。
                                例: {"danceability": {"value": 0.5, "weight": 1.0}, ...}
        top_n (int, optional): 上位何曲を返すかを指定。デフォルトは3件。

    Returns:
        list of dict: 目標値との距離が小さい曲から順に並んだ上位top_n件のリスト。
    """
    if not tracks:
        print("曲が見つかりませんでした。")
        return

    # 各トラックの音響特徴量を、目標値との二乗差（重みあり）を累積してdistanceに保存。
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
        # 最終的にユークリッド距離を算出。該当音響特徴量が無い場合は無限大(inf)に。
        if feature_count > 0:
            track['distance'] = math.sqrt(distance)
        else:
            track['distance'] = float('inf')  # 音響特徴量がない場合は大きい距離とみなす

    # 'distance' キーを基準にソートし、上位top_n件を抽出
    sorted_tracks = sorted(tracks, key=lambda x: x['distance'])
    top_tracks = sorted_tracks[:top_n]

    # コンソール表示用に必要な属性を定義し、表示を行う。
    display_attributes = ["id", "name", "artists", "genre", "danceability", "valence", "energy", "distance"]
    print(f"\nTop {top_n} 曲 (距離が近い順):\n")
    for idx, track in enumerate(top_tracks, start=1):
        print(f"曲 {idx}:")
        for attr in display_attributes:
            print(f"  {attr}: {track.get(attr, 'N/A')}")
        print()

    return top_tracks

if __name__ == "__main__":
    # 例: CSVファイルを指定して初期化する場合
    # csv_paths = ["dataset.csv"]
    workspace = '/Users/kaoriinoue/2024zyugyo/tishikizyohosyori/kokomerotalk/database_kokomelotalk'
    database_name = "filtered_v3_dataset"
    genre_filter = False
    determine_mode = "max"  # "max" または "weighted_ave"
    local_test(workspace=workspace, genre_filter=genre_filter, determine_mode=determine_mode, database_name=database_name)
