from flask import Flask, jsonify, render_template, request
from flask_sqlalchemy import SQLAlchemy
import random

app = Flask(__name__)

# Connect to Database
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///cafes.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)
app.app_context().push()


# Cafe TABLE Configuration
class Cafe(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(250), unique=True, nullable=False)
    map_url = db.Column(db.String(500), nullable=False)
    img_url = db.Column(db.String(500), nullable=False)
    location = db.Column(db.String(250), nullable=False)
    seats = db.Column(db.String(250), nullable=False)
    has_toilet = db.Column(db.Boolean, nullable=False)
    has_wifi = db.Column(db.Boolean, nullable=False)
    has_sockets = db.Column(db.Boolean, nullable=False)
    can_take_calls = db.Column(db.Boolean, nullable=False)
    coffee_price = db.Column(db.String(250), nullable=True)

    def to_dict(self):
        dictionary = {}
        # Loop through each column in the data record
        for column in self.__table__.columns:
            dictionary[column.name] = getattr(self, column.name)
        return dictionary


db.create_all()


@app.route("/")
def home():
    return render_template("index.html")


# HTTP GET - Read Record
@app.route('/random', methods=['GET'])
def get_random_cafe():
    random_number = random.randint(1, 21)
    random_cafe = Cafe.query.filter_by(id=random_number).first()
    return jsonify(cafe=random_cafe.to_dict())


@app.route('/all', methods=['GET'])
def get_all_cafes():
    # This returns a list of data records
    cafe_list = db.session.query(Cafe).all()
    # Loops through the list of data records in order to convert it to dictionary
    return jsonify(cafe=[cafe.to_dict() for cafe in cafe_list])


@app.route('/search', methods=['GET'])
def get_cafe_at_location():
    query_location = request.args.get('loc')
    cafes = db.session.query(Cafe).filter_by(location=query_location).all()
    if cafes:
        return jsonify(cafes=[cafe.to_dict() for cafe in cafes])
    else:
        return jsonify(error={'Not Found': 'Sorry, we do not have a cafe at that location'})

# HTTP POST - Create Record

# HTTP PUT/PATCH - Update Record

# HTTP DELETE - Delete Record


if __name__ == '__main__':
    app.run(debug=True)
