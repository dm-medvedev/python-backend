from code.base import Base
from code.columns import Boolean, Date, Float, Integer, String
from code.session import Session

Data_path = '../hw3/Data/city.csv'
my_session = Session()
my_session.table_from_csv('city', Data_path,
                          {'city': str, 'region': int})


class City(Base):
    __session__ = my_session
    city = String()
    region = Integer()


class Movie(Base):
    __session__ = my_session
    name = String()
    dvd = Boolean()
    dollars = Float()  # millions
    date = Date()


def main():
    city = City(city=42, region='Рим')  # error!
    city = City(region=42, city='Рим')  # нет error
    movie = Movie(name='Fargo', dvd=None, dollars=None, date=None)
    movie = Movie(name='Fargo', dvd=False, dollars=99.9, date='2011-01-01')
    city.create()
    movie.create()


if __name__ == '__main__':
    main()
