#!/usr/bin/env python3

from flask import Flask, make_response, jsonify
from flask_migrate import Migrate

from models import db, Bakery, BakedGood

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db' #direct your Flask app to a database at
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
    bakeries_serialized = [bakery.to_dict() for bakery in bakeries]
    # OR
    # bakeries = []
    # for bakery in Bakery.query.all():
    #     bakeries_serialized = bakery.to_dict()
    #     bakeries.append(bakery)
    response = make_response(
        jsonify(bakeries_serialized),
        200
    )
    # sends the http json header to the browser to 
    # inform it what kind of data it expects

    # response.headers['Content-Type'] = 'application/json' #optional

    return response
        # jsonify is a method in Flask that serializes 
        # (converts from one format to another) the SQLAlchemy object 
        # (its arguments) as JSON object by getting a list of keys and values 
        # to pass to the client, then returns a Response object
        # but due to its limitations we need ?????
        # SQLAlchemy-serializer in models

@app.route('/bakeries/<int:id>')
def bakery_by_id(id):
    # bakery = Bakery.query.filter_by(id=id).first()
    # OR 
    bakery = Bakery.query.filter(Bakery.id == id).first()
    bakery_dict = bakery.to_dict()
    response = make_response(jsonify(bakery_dict), 200)

    # response.headers['Content-Type'] = 'application/json' #optional

    return response

@app.route('/baked_goods/by_price')
def baked_goods_by_price():
    # bg_price_desc = BakedGood.query.order_by(BakedGood.price.desc()).first()
    # baked_goods_dict = [bg_price_desc.to_dict()] 
    # ^this is wrong even tho it passed the test
    bg_price_desc = BakedGood.query.order_by(BakedGood.price.desc()).all() 
    baked_goods_dict = [bg.to_dict() for bg in bg_price_desc] 
    # OR
    # price_desc = BakedGood.query.order_by(BakedGood.price).all()
    # baked_goods_dict = [
    #     bg.to_dict() for bg in price_desc
    # ]
    response = make_response(jsonify(baked_goods_dict), 200)

    # response.headers['Content-Type'] = 'application/json' #optional

    return response

@app.route('/baked_goods/most_expensive')
def most_expensive_baked_good():
    # most_expensive = BakedGood.query.order_by(BakedGood.price.desc()).limit(1).first()
    # ^this is wrong, limit() is used in vanila sql, here we use first()  

    most_expensive = BakedGood.query.order_by(BakedGood.price.desc()).first() 
    baked_goods_dict = most_expensive.to_dict()
    response = make_response(jsonify(baked_goods_dict), 200)

    # response.headers['Content-Type'] = 'application/json' #optional

    return response

if __name__ == '__main__':
    app.run(port=5555, debug=True)
