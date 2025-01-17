# УРОК 16 Задание 8
# В этом финальном задании вам нужно
# применить знания о моделях для создания 3 представлений,
# которые реализуют запросы на создание, добавление, удаление.

"""
    # Задание
    # Шаг 1.
    # ######
    # Создайте представение для эндпоинта GET /guides
    # которое возвращает список всех гидов со всеми полями
    # в формате JSON
    #
    #
    # Шаг 2.
    # ######
    # - Создайте представение для эндпоинта GET /guides/{id}
    # которое возвращает одного гида со всеми полями
    # в формате JSON в соответствии с его id
    #
    # Шаг 3.
    # ######
    # Создайте представение для эндпоинта
    # GET /guides/{id}/delete`, которое удаляет
    # одного гида в соответствии с его `id`
    #
    # Шаг 4.
    # ######
    # Создайте представление для эндпоинта POST /guides
    #  которое добавляет в базу данных гида, при получении
    # следующих данных:
    # {
    #     "surname": "Иванов",
    #     "full_name": "Иван Иванов",
    #     "tours_count": 7,
    #     "bio": "Провожу экскурсии",
    #     "is_pro": true,
    #     "company": "Удивительные экскурсии"
    # }
    # Шаг 5.
    # ######
    # - Допишите представление из шага 1 для фильтрации так,
    # чтобы при получении запроса типа /guides?tours_count=1
    # возвращались гиды с нужным количеством туров.
"""

from flask import Flask, jsonify, request
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import text
from guides_sql import CREATE_TABLE, INSERT_VALUES

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['JSON_AS_ASCII'] = False
app.url_map.strict_slashes = False
db = SQLAlchemy(app)
with db.session.begin():
    db.session.execute(text(CREATE_TABLE))
    db.session.execute(text(INSERT_VALUES))


class Guide(db.Model):
    __tablename__ = 'guide'
    id = db.Column(db.Integer, primary_key=True)
    surname = db.Column(db.String)
    full_name = db.Column(db.String)
    tours_count = db.Column(db.Integer)
    bio = db.Column(db.String)
    is_pro = db.Column(db.Boolean)
    company = db.Column(db.Integer)

    def as_dict(self):
        return {
            "id": self.id,
            "surname": self.surname,
            "full_name": self.full_name,
            "tours_count": self.tours_count,
            "bio": self.bio,
            "is_pro": self.is_pro,
            "company": self.company,
        }

# TODO напишите роуты здесь

# Задание
# Шаг 1.
# ######
# Создайте представение для эндпоинта GET /guides
# которое возвращает список всех гидов со всеми полями
# в формате JSON
#


@app.route("/guides")
def index_guides():

    tours_count = request.args.get("tours_count", None)

    if tours_count is None:
        return jsonify([item.as_dict() for item in Guide.query.all()]), 200
    else:
        return jsonify([item.as_dict() for item in Guide.query.filter(Guide.tours_count == tours_count).all()]), 200
#
# Шаг 2.
# ######
# - Создайте представение для эндпоинта GET /guides/{id}
# которое возвращает одного гида со всеми полями
# в формате JSON в соответствии с его id


@app.route("/guides/<int:pk>", methods=["GET"])
def index_guide_by_pk(pk):

    return jsonify(Guide.query.get(pk).as_dict()), 200

# Шаг 3.
# ######
# Создайте представение для эндпоинта
# GET /guides/{id}/delete`, которое удаляет
# одного гида в соответствии с его `id`


@app.route("/guides/<int:pk>/delete", methods=["GET"])
def index_delete_guide(pk):
    Guide.query.get(pk).delete()
    db.session.commit()
    return "ok", 200

# Шаг 4.
# ######
# Создайте представление для эндпоинта POST /guides
#  которое добавляет в базу данных гида, при получении
# следующих данных:
# {
#     "surname": "Иванов",
#     "full_name": "Иван Иванов",
#     "tours_count": 7,
#     "bio": "Провожу экскурсии",
#     "is_pro": true,
#     "company": "Удивительные экскурсии"
# }


@app.route("/guides", methods=["POST"])
def index_guides_add():
    db.session.add(Guide(**request.form))
    db.session.commit()
    return "ok", 200

# Шаг 5.
# ######
# - Допишите представление из шага 1 для фильтрации так,
# чтобы при получении запроса типа /guides?tours_count=1
# возвращались гиды с нужным количеством туров.


if __name__ == "__main__":
    app.run()
