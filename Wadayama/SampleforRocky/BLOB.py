import sqlite3

# データベース接続
conn = sqlite3.connect('MVP.db')
c = conn.cursor()

# テーブル作成
c.execute('''CREATE TABLE IF NOT EXISTS brandlogo (brandlogo_id INTEGER PRIMARY KEY, name TEXT, data BLOB)''')

# ファイル名とBLOBデータのリスト
file_blob_pairs = [
    ('kurolabel.png', '黒ラベル樽生'),
    ('ebisu.png', 'ヱビス樽生'),
    ('kohaku_ebisu.png', '琥珀ヱビス'),
    ('edelpils.png', 'エーデル樽生'),
    ('tarunama_black.png', '樽生ブラック'),
    ('sorachi.png', 'ソラチ樽生'),
    ('premol.png', 'プレミアムモルツ')
    # 他の画像ファイルと名前のペアを追加
]

# バイナリデータを挿入
for file_name, name in file_blob_pairs:
    with open(file_name, 'rb') as f:
        blob_data = f.read()
    c.execute('INSERT INTO brandlogo (name, data) VALUES (?, ?)', (name, blob_data))

# コミットと接続解除
conn.commit()
conn.close()
