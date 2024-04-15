import pandas as pd
import requests
import json
from dotenv import load_dotenv
import os
load_dotenv()

GMAPS_API_KEY = os.getenv("GMAPS_API_KEY")

def get_place_details(place_id):
    params = {
        "place_id": place_id,
        "key": GMAPS_API_KEY,
        "region": "jp",
        "language": "ja",
    }

    url = "https://maps.googleapis.com/maps/api/place/details/json"
    res = requests.get(url, params=params)
    return json.loads(res.text)["result"]

def get_place_info(query):
    params = {
        "query": query,
        "key": GMAPS_API_KEY,
        "region": "jp",
        "language": "ja",
    }

    url = "https://maps.googleapis.com/maps/api/place/textsearch/json"
    res = requests.get(url, params=params)
    return json.loads(res.text)["results"]

# def get_image_data(photo_reference):
#     max_width = 400
#     photo_params = {
#         "maxwidth": max_width,
#         "photo_reference": photo_reference,
#         "key": GMAPS_API_KEY,
#     }
#     photo_url = "https://maps.googleapis.com/maps/api/place/photo"
#     photo_response = requests.get(photo_url, params=photo_params)
#     return photo_response.content

def get_reviews(reviews):
    return [review["text"] for review in reviews]

def get_place_details(place_id):
    params = {
        "place_id": place_id,
        "key": GMAPS_API_KEY,
        "region": "jp",
        "language": "ja",
        "fields": "name,rating,geometry,formatted_address,types,reviews,website,photos"  # typesと他の必要なフィールドを明示
    }

    url = "https://maps.googleapis.com/maps/api/place/details/json"
    res = requests.get(url, params=params)
    return json.loads(res.text)["result"]

# CSVファイルからデータを読み込む
df = pd.read_csv("sapporo_list_Sample.csv")

# 新しいカラムを追加する
for i in range(1, 6):
    df[f'レビュー{i}'] = ""

df['営業時間'] = ""
df['概要'] = ""
df['ジャンル'] = ""
df['評価'] = ""
df['ウェブサイトURL'] = ""
df['lat'] = ""
df['lng'] = ""
df['店名from Google'] = ""
df['住所from Google'] = ""
# df['画像データ'] = ""

for index, row in df.iterrows():
    target_info = get_place_info(row['店名'] + ' ' + row['住所'])
    if target_info:
        place_id = target_info[0]["place_id"]
        target_detail = get_place_details(place_id)
        df.at[index, '営業時間'] = target_detail.get("current_opening_hours", {}).get("weekday_text", "")
        df.at[index, '概要'] = target_detail.get("editorial_summary", {}).get("overview", "")
        df.at[index, 'ジャンル'] = ', '.join(target_detail.get("types", []))  # ジャンル情報をカンマ区切りで保存
        df.at[index, '評価'] = target_detail.get("rating", "")
        df.at[index, 'ウェブサイトURL'] = target_detail.get("website", "")
        geo = target_detail.get("geometry", {})
        df.at[index, 'lat'] = geo.get("location", {}).get("lat", "")
        df.at[index, 'lng'] = geo.get("location", {}).get("lng", "")
        df.at[index, '店名from Google'] = target_detail.get("name", "")
        df.at[index, '住所from Google'] = target_info[0]["formatted_address"]
        reviews = target_detail.get("reviews", [])
        for i, review in enumerate(reviews[:5]):
            df.at[index, f'レビュー{i+1}'] = review.get("text", "")
        # 画像データの取得
        # if "photos" in target_info[0] and target_info[0]["photos"]:
        #     photo_reference = target_info[0]["photos"][0]["photo_reference"]
        #     image_data = get_image_data(photo_reference)
        #     df.at[index, '画像データ'] = image_data

# DataFrameをUTF-8エンコーディングでCSVファイルとして出力
df.to_csv("output_sample0405_v3.csv", index=False, encoding="utf-8_sig")