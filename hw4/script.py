from code.session import Session
from code.columns import String, Integer, Date, Boolean, Float
from code.base import Base

my_session = Session()      
my_session.table_from_csv('city', '../hw3/Data/city.csv', {'city': str, 'region': int})
    
class City(Base):
    __session__ = my_session
    city = String()
    region = Integer()


city = City(city=42, region='Рим') # error!
# city = City(region=42, city='Рим') # нет error
