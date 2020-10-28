import unittest
from code.base import Base
from code.columns import Integer, String
from code.session import Session


CITY_CSV = './Data/city.csv'


class City(Base):
    city = String()
    region = Integer()


class TestCity(unittest.TestCase):
    def setUp(self):
        self.my_session = Session()
        self.my_session.table_from_csv('city', CITY_CSV,
                                       {'city': str, 'region': int})
        connection = self.my_session.connection
        command = 'SELECT * from city WHERE city = ?'
        self.get_city = lambda c: list(connection.execute(command, (c,)))
        City.__session__ = self.my_session

    def test_all(self):
        with open(CITY_CSV, 'r') as f:
            lines = f.readlines()[1:]
            r_cities, r_regions = zip(*list(line.strip().split(';')
                                            for line in lines))
        new_cities, new_regions = zip(*[(el.city, el.region)
                                        for el in City.all()])
        r_cities = sorted(r_cities)
        new_cities = sorted(r_cities)
        new_regions = sorted(new_regions)
        r_regions = sorted([int(el) for el in r_regions])
        self.assertEqual(r_regions, new_regions)
        self.assertEqual(r_cities, new_cities)

    def test_read(self):
        cities74 = City.read(region=74)
        self.assertIsInstance(cities74, list)
        self.assertTrue(len(cities74) == 1)
        tuple74 = cities74[0].city, cities74[0].region
        self.assertEqual(tuple74, ('Северодвинск', 74))

    def test_update(self):
        city74 = City.read(region=74)[0]
        city74.region = 174
        intable = self.get_city(city74.city)
        self.assertTrue(len(intable) == 1)
        self.assertEqual(intable[0], ('Северодвинск', 74))
        city74.update()
        intable = self.get_city(city74.city)
        self.assertEqual(intable[0], ('Северодвинск', 174))
        msg = "Can't create already existing row"
        with self.assertRaisesRegex(RuntimeError, msg):
            city74.create()

    def test_delete(self):
        city74 = City.read(region=74)[0]
        city74.delete()
        intable = self.get_city(city74.city)
        self.assertTrue(len(intable) == 0)
        msg = "Can't delete non-readen or non-created row"
        with self.assertRaisesRegex(RuntimeError, msg):
            city74.delete()

    def test_create(self):
        neg_city = City(city='Negative', region=-10)
        intable = self.get_city(neg_city.city)
        self.assertTrue(len(intable) == 0)
        neg_city.create()
        intable = self.get_city(neg_city.city)
        self.assertTrue(len(intable) == 1)
        self.assertEqual(intable[0], ('Negative', -10))
        msg = "Can't create already existing row"
        with self.assertRaisesRegex(RuntimeError, msg):
            neg_city.create()

    def test_duplicates(self):
        neg_city = City(city='Negative', region=-10)
        neg_city.create()
        neg_city2 = City(city='Negative', region=-10)
        self.assertFalse(id(neg_city2) == id(neg_city))
        msg = "Can't create already existing row"
        with self.assertRaisesRegex(RuntimeError, msg):
            neg_city2.create()
        msg = "Can't update non-readen or non-created row"
        with self.assertRaisesRegex(RuntimeError, msg):
            neg_city2.update()
        msg = "Can't delete non-readen or non-created row"
        with self.assertRaisesRegex(RuntimeError, msg):
            neg_city2.delete()
        neg_city2 = City.read(city=neg_city2.city,
                              region=neg_city2.region)[0]
        msg = "Can't create already existing row"
        with self.assertRaisesRegex(RuntimeError, msg):
            neg_city2.create()
        msg = "Can't update row, update will create copy"
        with self.assertRaisesRegex(RuntimeError, msg):
            neg_city2.update()
        neg_city2.delete()
        intable = self.get_city(neg_city.city)
        self.assertTrue(len(intable) == 0)
        msg = "Can't update non-existing row"
        with self.assertRaisesRegex(RuntimeError, msg):
            neg_city.update()
        msg = "Can't delete non-existing row"
        with self.assertRaisesRegex(RuntimeError, msg):
            neg_city.delete()
        neg_city.create()
        intable = self.get_city(neg_city.city)
        self.assertTrue(len(intable) == 1)
        msg = "Can't create already existing row"
        with self.assertRaisesRegex(RuntimeError, msg):
            neg_city2.create()
        neg_city2.region = -100
        msg = "Can't update non-readen or non-created row"
        with self.assertRaisesRegex(RuntimeError, msg):
            neg_city2.update()
        msg = "Can't delete non-readen or non-created row"
        with self.assertRaisesRegex(RuntimeError, msg):
            neg_city2.delete()
        neg_city2.create()
        intable = self.get_city(neg_city.city)
        self.assertTrue(len(intable) == 2)


if __name__ == '__main__':
    unittest.main()
