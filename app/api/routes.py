from flask import Blueprint, request, jsonify, render_template
from helpers import token_required
from models import db, User, Sneaker, sneaker_schema, sneakers_schema

api = Blueprint('api',__name__, url_prefix='/api')

@api.route('/getdata')
def getdata():
    return {'yee': 'haw'}

@api.route('/sneakers', methods = ['POST'])
@token_required
def create_sneaker(current_user_token):
    brand = request.json['brand']
    size = request.json['size']
    price = request.json['price']
    release = request.json['release']
    user_token = current_user_token.token

    print(f'BIG TESTER: {current_user_token.token}')

    sneaker = Sneaker(brand, size, price, release, user_token = user_token )

    db.session.add(sneaker)
    db.session.commit()

    response = sneaker_schema.dump(sneaker)
    return jsonify(response)

@api.route('/sneakers', methods = ['GET'])
@token_required
def get_sneaker(current_user_token):
    a_user = current_user_token.token
    sneakers = Sneaker.query.filter_by(user_token = a_user).all()
    response = sneakers_schema.dump(sneakers)
    return jsonify(response)

@api.route('/sneakers/<id>', methods = ['POST', 'PUT'])
@token_required
def update_sneaker(current_user_token, id):
    sneaker = Sneaker.query.get(id)
    sneaker.brand = request.json['brand']
    sneaker.size = request.json['size']
    sneaker.price = request.json['price']
    sneaker.release = request.json['release']
    sneaker.user_token = current_user_token.token

    db.session.commit()
    response = sneaker_schema.dump(sneaker)
    return jsonify(response)

@api.route('/sneakers/<id>', methods = ['DELETE'])
@token_required
def delete_sneaker(current_user_token, id):
    sneaker = Sneaker.query.get(id)
    db.session.delete(sneaker)
    db.session.commit()
    response = sneaker_schema.dump(sneaker)
    return jsonify(response)