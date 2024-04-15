import pandas as pd
import requests
import json
from dotenv import load_dotenv
import os

# 環境変数をロード
load_dotenv()

# Google Maps APIキーを環境変数から取得
GMAPS_API_KEY = os.getenv("GMAPS_API_KEY")

def get_place_details(place_id):
    params = {
        "place_id": place_id,
        "key": GMAPS_API_KEY,
        "language": "ja",
        "fields": "name,rating,geometry,formatted_address,types,opening_hours,website,reviews,photos,price_level"
    }
    url = "https://maps.googleapis.com/maps/api/place/details/json"
    try:
        response = requests.get(url, params=params)
        response.raise_for_status()  # HTTPエラーをチェック
        return json.loads(response.text)["result"]
    except requests.RequestException as e:
        print(f"Error fetching place details: {e}")
        return None

def get_place_info(query):
    params = {
        "query": query,
        "key": GMAPS_API_KEY,
        "language": "ja",
    }
    url = "https://maps.googleapis.com/maps/api/place/textsearch/json"
    try:
        response = requests.get(url, params=params)
        response.raise_for_status()
        return json.loads(response.text)["results"]
    except requests.RequestException as e:
        print(f"Error searching for place: {e}")
        return []

# CSVファイルからデータを読み込む
df = pd.read_csv("sapporo_list_Sample.csv")

# 新しいカラムをDataFrameに追加する
columns_to_add = ['レビュー1', 'レビュー2', 'レビュー3', 'レビュー4', 'レビュー5', '営業時間', 'ジャンル', '評価', 'ウェブサイトURL', '価格レベル', 'lat', 'lng', '店名from Google', '住所from Google']
for col in columns_to_add:
    df[col] = ""

# 各行に対してAPIを呼び出してデータを取得し、DataFrameを更新
for index, row in df.iterrows():
    print(f"Processing {row['店名']} at {row['住所']}...")
    target_info = get_place_info(f"{row['店名']} {row['住所']}")
    if target_info:
        place_id = target_info[0]["place_id"]
        target_detail = get_place_details(place_id)
        if target_detail:
            # 営業時間を取得し、文字列に変換
            opening_hours = target_detail.get("opening_hours", {})
            df.at[index, '営業時間'] = '\n'.join(opening_hours.get("weekday_text", []))
            # その他の情報をDataFrameに追加
            df.at[index, 'ジャンル'] = ', '.join(target_detail.get("types", []))
            df.at[index, '評価'] = target_detail.get("rating", "")
            df.at[index, 'ウェブサイトURL'] = target_detail.get("website", "")
            df.at[index, '価格レベル'] = target_detail.get("price_level", "情報なし")
            geo = target_detail.get("geometry", {})
            df.at[index, 'lat'] = geo.get("location", {}).get("lat", "")
            df.at[index, 'lng'] = geo.get("location", {}).get("lng", "")
            df.at[index, '店名from Google'] = target_detail.get("name", "")
            df.at[index, '住所from Google'] = target_info[0]["formatted_address"]
            reviews = target_detail.get("reviews", [])
            for i, review in enumerate(reviews[:5]):
                df.at[index, f'レビュー{i+1}'] = review.get("text", "")
        else:
            print(f"Details not found for {place_id}")
    else:
        print(f"No information found for {row['店名']} at {row['住所']}")

# DataFrameをUTF-8エンコーディングでCSVファイルとして出力
df.to_csv("output_sample0415_v3.csv", index=False, encoding="utf-8_sig")
