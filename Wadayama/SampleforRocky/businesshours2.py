from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, Float, String
from datetime import datetime, time
import calendar
import os

current_dir = os.path.dirname(os.path.abspath(__file__))
database_file = os.path.join(current_dir, "testdata5.db")

engine = create_engine("sqlite:///"+ database_file, echo=True)

Session = sessionmaker(bind=engine)
session = Session()

Base = declarative_base()

class Store(Base):
    __tablename__ = "Store"
    store_id = Column(Integer, primary_key=True)
    store_name = Column(String, nullable=False)
    store_address = Column(String, nullable=True)
    store_contact = Column(String, nullable=True)
    brand = Column(String, nullable=True)
    businesshours = Column(String, nullable=True)
    rating = Column(Float, nullable=False)
    lat = Column(Float, nullable=False)
    lng = Column(Float, nullable=False)
    url = Column(String, nullable=True)
    district = Column(String, nullable=True)
    brandlogo_id = Column(Integer, nullable=True)

def is_business_hours(store_id, current_time):
    store = session.query(Store).filter(Store.store_id == store_id).first()
    if not store:
        return False  # Store not found

    current_day_eng = calendar.day_name[datetime.now().weekday()]  # 現在の曜日を英語で取得
    print("Current day: ", current_day_eng)  # デバッグログ: 現在の曜日

    business_hours = store.businesshours.split('\n')
    business_hours_dict = {}
    for hours in business_hours:
        day, time_range = hours.split(': ')
        if time_range:
            time_slots = [tuple(slot.split('～')) for slot in time_range.split(', ')]
            business_hours_dict[day] = time_slots

    print("Business hours dictionary:", business_hours_dict)  # デバッグログ: データベースから取得した営業時間情報

    if current_day_eng in business_hours_dict:
        time_slots = business_hours_dict[current_day_eng]
        current_time = current_time.time()
        print("Current time:", current_time)  # デバッグログ: 現在時刻
        for start, end in time_slots:
            open_time = datetime.strptime(start, "%H時%M分").time()
            close_time = datetime.strptime(end, "%H時%M分").time()
            print("Open time:", open_time)  # デバッグログ: 開店時間
            print("Close time:", close_time)  # デバッグログ: 閉店時間
            is_open = open_time <= current_time <= close_time
            print("Is open:", is_open)  # デバッグログ: 営業時間内であるかの評価結果
            if is_open:
                return True  # Store is open
    return False  # Store is closed

if __name__ == "__main__":
    store_id = 1  # Change store_id as needed
    current_time = datetime.now()  # 現在時刻をdatetime.timeに変換
    if is_business_hours(store_id, current_time):
        print("営業中")
    else:
        print("営業時間外")
