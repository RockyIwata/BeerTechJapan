from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, Float, String
import sqlalchemy
import pandas as pd
import os

# uname() error回避
import platform
print(platform.uname())

main_path = os.path.dirname(os.path.abspath(__file__))
path = os.chdir(main_path)
print(path)
engine = create_engine("sqlite:///testdb1.db", echo=True)

db_session = scoped_session(
    sessionmaker(
        autocommit = False,
        autoflush = False,
        bind = engine
    )
)

Base = declarative_base()
Base.query = db_session.query_property()

class Store(Base):
    __tablename__ = "Store"
    store_id = Column(Integer, primary_key=True)
    store_name = Column(String, nullable=False)
    store_address = Column(Integer, nullable=False)
    store_contact = Column(String)
    businesshours = Column(String, nullable=False)
    rating = Column(Float, nullable = False)
    lat = Column(Float, nullable = False)
    lng = Column(Float, nullable = False)

def __init__(self, store_name = None, store_address = None, store_contact = None, businesshours = None, rating = None, lat = None, lng = None):
    self.store_name = store_name
    self.store_address = store_address
    self.store_contact = store_contact
    self.businesshours = businesshours
    self.rating = rating
    self.lat = lat
    self.lng = lng

Base.metadata.create_all(bind=engine)

# 現在の作業ディレクトリを取得する
current_directory = os.getcwd()
# CSVファイルのパスを指定する
csv_file_path = os.path.join(current_directory, "googleAPI_output_sample_20240402.csv")

def read_data():
    df = pd.read_csv(csv_file_path)

    for index, _df in df.iterrows():
        row = Store(store_name = _df["store_name"], store_address = _df["store_address"], store_contact = _df["store_contact"], businesshours = _df["businesshours"], rating = _df["rating"], lat = _df["lat"], lng = _df["lng"])
        db_session.add(row)
    db_session.commit()

read_data()