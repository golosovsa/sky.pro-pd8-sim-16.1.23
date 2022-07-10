# Добавление городов
#
# Дана модель City и таблица city.
#
# Добавьте в базу данных сведения о городах
# в соответствии с таблицей ниже.
# +----+---------+------------+------------+
# | id |   name  | country_ru | population |
# +----+---------+------------+------------+
# | 1  |   Рим   |   Италия   |  28730000  |
# | 2  |  Милан  |   Италия   |  1333000   |
# | 3  | Венеция |   Италия   |   265000   |
# | 4  | Стамбул |   Турция   | 108950000  |
# | 5  |  Кемер  |   Турция   |   22421    |
# +----+---------+------------+------------+
#
#
import prettytable
from flask import Flask
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)


class City(db.Model):
    __tablename__ = 'city'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    country_ru = db.Column(db.String)
    population = db.Column(db.Integer)


db.create_all()

db.session.add_all([
    City(id=1, name="Рим", country_ru="Италия", population=28730000),
    City(id=2, name="Милан", country_ru="Италия", population=1333000),
    City(id=3, name="Венеция", country_ru="Италия", population=265000),
    City(id=4, name="Стамбул", country_ru="Турция", population=108950000),
    City(id=5, name="Кемер", country_ru="Турция", population=22421),
])

db.session.commit()

# Не удаляйте код ниже, он нужен для корректного отображения
# созданной вами модели при запуске файла

session = db.session()
cursor = session.execute(f"SELECT * from {City.__tablename__}").cursor
mytable = prettytable.from_db_cursor(cursor)
mytable.max_width = 30


if __name__ == '__main__':
    print(mytable)
