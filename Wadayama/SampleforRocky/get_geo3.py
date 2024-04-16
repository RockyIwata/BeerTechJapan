import folium
import base64
from geopy.distance import geodesic
from DB_test5 import db_session, Store, BrandLogo

def get_lat_lng_by_district(district):
    query = db_session.query(Store).filter(Store.district == district)
    stores = query.all()
    if stores:
        return [(store.lat, store.lng, store.store_name, store.brand) for store in stores]
    else:
        return []

def get_stores_within_radius(center_lat, center_lng, radius_km):
    stores_within_radius = []
    all_stores = db_session.query(Store).all()
    for store in all_stores:
        store_location = (store.lat, store.lng)
        distance = geodesic((center_lat, center_lng), store_location).kilometers
        if distance <= radius_km:
            stores_within_radius.append((store.lat, store.lng, store.store_name, store.brand))
    return stores_within_radius

# フロントエンドから提供された地区（district）に該当する店舗情報を取得
district = '千代田区'  # 仮のデフォルト地区
stores_info = get_lat_lng_by_district(district)

# もし地区に対応する店舗情報がなければ、現在地を取得して半径3km以内の店舗情報を取得
if not stores_info:
    # ここに現在地を取得する処理を実装する必要があります
    current_lat, current_lng = 35.682839, 139.759455  # 仮のデフォルト現在地
    stores_info = get_stores_within_radius(current_lat, current_lng, 3)

if stores_info:
    print(f"{district}に存在する店舗の情報: {stores_info}")
    
    # foliumマップの作成
    map = folium.Map(location=[stores_info[0][0], stores_info[0][1]], zoom_start=14)  # 店舗情報の最初の店舗の位置を中心とする
    
    # 同じbrand毎に異なる色を割り当てるための色のマッピング
    color_map = {'ヱビス樽生': 'blue', 'エーデル樽生': 'green', 'アサヒスーパードライ': 'yellow', '黒ラベル樽生': 'black', 'マスターズドリーム': 'red'}
    
    # ポップアップの作成と追加
    for lat, lng, store_name, brand in stores_info:
        popup_html = f"<b>{store_name}</b><br>ブランド: {brand}<br>"
        
        # brandlogoテーブルから該当するブランドの画像を取得
        brand_logo = db_session.query(BrandLogo).filter(BrandLogo.name == brand).first()
        if brand_logo:
            # 画像の復元
            img_tag = f"<img src='data:image/png;base64,{base64.b64encode(brand_logo.data).decode('utf-8')}' width='100px'/>"
            popup_html += img_tag
        
        popup = folium.Popup(popup_html, max_width=300)
        folium.Marker(location=[lat, lng], popup=popup, icon=folium.Icon(color=color_map.get(brand, 'gray'))).add_to(map)
    
    map.save("map.html")
    
    print("マップが作成され、map.htmlに保存されました。")
else:
    print(f"{district}に対応する店舗は見つかりませんでした。")
