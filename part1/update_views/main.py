# Имеется наполненная БД с таблицей guide и полуготовый код на фласке.
# Напишите представления для следующих ендпоинтов:
#
# Method: GET
# URL: /guides
# Response: [{guide_json}, {guide_json}, {guide_json}]
#
# Method: GET
# URL: /guides/1
# Response: { <guide_json> }
#
#
from flask import Flask, jsonify
from sqlalchemy import text, inspect
from flask_sqlalchemy import SQLAlchemy
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

@app.route("/guides")
def get_guides():
    data = [item.as_dict() for item in Guide.query.all()]
    print(data)
    return jsonify(data), 200


@app.route("/guides/<int:gid>")
def get_guide(gid):
    data = Guide.query.get(gid).as_dict()
    return jsonify(data), 200

# чтобы увидеть результат работы функций
# запустите фаил и
# перейдите по адресу:
# 127.0.0.1:5000/guides
# 127.0.0.1:5000/guides/1


if __name__ == "__main__":
    app.run()
