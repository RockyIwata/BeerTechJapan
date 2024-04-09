from DB_test2 import db_session, Store

def get_lat_lng_by_id(store_id):
    # store_idに対応するlatとlngを取得するクエリ
    query = db_session.query(Store).filter(Store.store_id == store_id)
    
    # store_idが存在する場合はlatとlngを取得し、存在しない場合はNoneを返す
    store = query.first()
    if store:
        return store.lat, store.lng
    else:
        return None, None

# 任意のstore_idを指定
store_id = 1
lat, lng = get_lat_lng_by_id(store_id)
if lat is not None and lng is not None:
    print(f"store_id {store_id} に対応する lat は {lat} で、lng は {lng} です。")
else:
    print(f"store_id {store_id} に対応する店舗は見つかりませんでした。")

