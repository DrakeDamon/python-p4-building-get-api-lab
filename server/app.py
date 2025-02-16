#!/usr/bin/env python3

from flask import Flask, make_response, jsonify
from flask_migrate import Migrate
from sqlalchemy import desc  # Add this line
from models import db, Bakery, BakedGood

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.json.compact = False

migrate = Migrate(app, db)

db.init_app(app)

@app.route('/')
def index():
    return '<h1>Bakery GET API</h1>'

@app.route('/bakeries')
def bakeries():
    bakeries = Bakery.query.all()

    response = make_response(
        jsonify([bakery.to_dict() for bakery in bakeries]),
        200
    )
    return response


@app.route('/bakeries/<int:id>')
def bakery_by_id(id):
    bakeries = Bakery.query.filter_by(id=id).first()

    response = make_response(
        jsonify(bakeries.to_dict()),
        200
    )
    return response

@app.route('/baked_goods/by_price')
def baked_goods_by_price():
    baked_goods = BakedGood.query.order_by(BakedGood.price.desc()).all()

    response = make_response(
        jsonify([bg.to_dict() for bg in baked_goods]),
        200
    )

    return response

@app.route('/baked_goods/most_expensive')
def most_expensive_baked_good():
    most_expensive = BakedGood.query.order_by(BakedGood.price.desc()).first()
    
    if most_expensive:
        return jsonify(most_expensive.to_dict()), 200, {'Content-Type': 'application/json'}
    else:
        return jsonify({"error": "No baked goods found"}), 404, {'Content-Type': 'application/json'}
if __name__ == '__main__':
    app.run(port=5555, debug=True)
