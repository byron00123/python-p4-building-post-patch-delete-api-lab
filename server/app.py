from flask import Flask, request, make_response, jsonify
from flask_migrate import Migrate

from models import db, Bakery, BakedGood

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.json_encoder.compact = False

migrate = Migrate(app, db)

db.init_app(app)

@app.route('/')
def home():
    return '<h1>Bakery GET-POST-PATCH-DELETE API</h1>'

@app.route('/bakeries', methods=['GET'])
def get_bakeries():
    bakeries = Bakery.query.all()
    bakeries_serialized = [bakery.to_dict() for bakery in bakeries]
    return jsonify(bakeries_serialized), 200

@app.route('/bakeries/<int:id>', methods=['GET'])
def get_bakery_by_id(id):
    bakery = Bakery.query.get_or_404(id)
    bakery_serialized = bakery.to_dict()
    return jsonify(bakery_serialized), 200

@app.route('/bakeries/<int:id>', methods=['PATCH'])
def update_bakery(id):
    bakery = Bakery.query.get_or_404(id)

    if 'name' in request.form:
        bakery.name = request.form['name']

    db.session.commit()
    bakery_serialized = bakery.to_dict()
    return jsonify(bakery_serialized), 200

@app.route('/baked_goods', methods=['POST'])
def create_baked_good():
    name = request.form.get('name')
    price = request.form.get('price')
    description = request.form.get('description')

    baked_good = BakedGood(name=name, price=price, description=description)
    db.session.add(baked_good)
    db.session.commit()

    baked_good_serialized = baked_good.to_dict()
    return jsonify(baked_good_serialized), 201

@app.route('/baked_goods/<int:id>', methods=['DELETE'])
def delete_baked_good(id):
    baked_good = BakedGood.query.get_or_404(id)
    db.session.delete(baked_good)
    db.session.commit()
    return jsonify({'message': 'Baked good deleted successfully.'}), 200

if __name__ == '__main__':
    app.run(port=5555, debug=True)
