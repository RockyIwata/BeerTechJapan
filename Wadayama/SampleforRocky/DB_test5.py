from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, Float, String, LargeBinary, ForeignKey
from sqlalchemy.orm import relationship
import pandas as pd
import os

current_dir = os.path.dirname(os.path.abspath(__file__))
database_file = os.path.join(current_dir, "testdata5.db")

engine = create_engine("sqlite:///"+ database_file, echo=True)

db_session = scoped_session(
    sessionmaker(
        autocommit=False,
        autoflush=False,
        bind=engine
    )
)

Base = declarative_base()
Base.query = db_session.query_property()

class BrandLogo(Base):
    __tablename__ = "brandlogo"
    brandlogo_id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    data = Column(LargeBinary, nullable=False)

    def __init__(self, name=None, data=None):
        self.name = name
        self.data = data

class Store(Base):
    __tablename__ = "Store"
    store_id = Column(Integer, primary_key=True)
    store_name = Column(String, nullable=False)
    store_address = Column(String, nullable=True)
    store_contact = Column(String, nullable=True)
    brand = Column(String, nullable=True)
    businesshours = Column(String, nullable=True)  # Change to String
    rating = Column(Float, nullable=False)
    lat = Column(Float, nullable=False)
    lng = Column(Float, nullable=False)
    url = Column(String, nullable=True)
    district = Column(String, nullable=True)
    brandlogo_id = Column(Integer, ForeignKey('brandlogo.brandlogo_id'), nullable=True)
    brandlogo = relationship("BrandLogo")

    def __init__(self, store_name=None, store_address=None, store_contact=None, brand=None, businesshours=None, rating=None, lat=None, lng=None, url=None, district=None, brandlogo_id=None):
        self.store_name = store_name
        self.store_address = store_address
        self.store_contact = store_contact
        self.brand = brand
        self.businesshours = businesshours
        self.rating = rating
        self.lat = lat
        self.lng = lng
        self.url = url
        self.district = district
        self.brandlogo_id = brandlogo_id

class Review(Base):
    __tablename__ = "review"
    review_id = Column(Integer, primary_key=True)
    content = Column(String, nullable=False)
    post_date = Column(String, nullable=True)
    store_id = Column(Integer, ForeignKey('Store.store_id'), nullable=False)
    store = relationship("Store")

    def __init__(self, content=None, post_date=None, store_id=None):
        self.content = content
        self.post_date = post_date
        self.store_id = store_id

Base.metadata.create_all(bind=engine)

def read_data():
    csv_file_path = os.path.join(current_dir, "store_sample.csv")
    df = pd.read_csv(csv_file_path)

    for index, _df in df.iterrows():
        store = Store(store_name=_df["store_name"],
                    store_address=_df["store_address"],
                    store_contact=_df["store_contact"],
                    brand=_df["brand"],
                    businesshours=_df["businesshours"],
                    rating=_df["rating"],
                    lat=_df["lat"],
                    lng=_df["lng"],
                    url=_df["url"],
                    district=_df["district"],
                    brandlogo_id=_df["brandlogo_id"])
        db_session.add(store)
        db_session.commit()  # Committing after each store to get the store_id
        
        # Add reviews
        for i in range(1, 6):  # review_1 to review_5
            review_column = f"review_{i}"
            if pd.notna(_df[review_column]):
                review = Review(content=_df[review_column], store_id=store.store_id)
                db_session.add(review)
    db_session.commit()

if __name__ == "__main__":
    read_data()
