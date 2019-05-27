import os
from flask import Flask, request, jsonify, render_template, abort, make_response
from flask_sqlalchemy import SQLAlchemy
from flask_jwt_extended import (create_access_token, create_refresh_token, jwt_required, jwt_refresh_token_required, get_jwt_identity, get_raw_jwt, JWTManager)
# from psycopg2 import *

apl = Flask(__name__)

apl.config.from_object(os.environ['APP_SETTINGS'])
apl.config['JWT_SECRET_KEY'] = 'somestri1!ng'
jwt = JWTManager(apl)
apl.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(apl)

from models import Pengguna, Item, Transaksi, Admin

@apl.route("/")
def hello():
    return jsonify({'message': 'index ok'})

@apl.route("/getitems")
def get_items():
    try:
        items = Item.query.all()
        return jsonify([e.serialize() for e in items])
    except Exception as e:
        return(str(e))

@apl.route("/getpengguna")
def get_pengguna():
    try:
        users = Pengguna.query.all()
        return jsonify([e.serialize() for e in users])
    except Exception as e:
        return (str(e))

@apl.route("/getransaksi")
def get_transaksi():
    try:
        transactions = Transaksi.query.all()
        return jsonify([e.serialize() for e in transactions])
    except Exception as e:
        return (str(e))

@apl.route("/getadmin")
def get_admin():
    try:
        admins = Admin.query.all()
        return jsonify([e.serialize() for e in admins])
    except Exception as e:
        return (str(e))

@apl.route("/get/<id_>")
def get_by_id(id_):
    try:
        book = Book.query.filter_by(id = id_).first()
        return jsonify(book.serialize())
    except Exception as e:
        return(str(e))

@apl.route("/getpengguna/<id_>")
def getpengguna_by_id(id_):
    try:
        user = Pengguna.query.filter_by(id = id_).first()
        return jsonify(user.serialize())
    except Exception as e:
        return (str(e))

@apl.route("/getitem/<id_>")
def get_item_by_id(id_):
    try:
        item = Item.query.filter_by(id = id_).first()
        return jsonify(item.serialize())
    except Exception as e:
        return (str(e))

@apl.route("/getransaksi/<id_>")
def get_transaksi_by_id(id_):
    try:
        transaction = Transaksi.query.filter_by(id = id_).first()
        return jsonify(transaction.serialize())
    except Exception as e:
        return (str(e))

@apl.route("/getadmin/<id_>")
def get_admin_by_id(id_):
    try:
        admin = Admin.query.filter_by(id = id_).first()
        return jsonify(admin.serialize())
    except Exception as e:
        return str(e)

@apl.route('/pengguna', methods=['POST'])
@jwt_required
def create_pengguna():
    post_data = request.get_json()
    if request.method == 'POST':
       
        try:
            user = Pengguna (
                
                nama = post_data.get('nama'),
                alamat = post_data.get('alamat'),
                telepon = post_data.get('telepon'),
                username = post_data.get('username'),
                password = Pengguna.generate_hash(post_data['password'])
            )
            db.session.add(user)
            db.session.commit()
            resp = {
                'status': 'success',
                'message': 'successfully insert'
            }
            return make_response(jsonify(resp)), 201
        except Exception as e:
            resp = {
                'status': 'fail',
                'message': e
            }
            return make_response(jsonify(resp)), 401

@apl.route('/item', methods=['POST'])
@jwt_required
def create_item():
    post_data = request.get_json()
    if request.method == 'POST':
        
        try:
            item = Item(
                pengguna = post_data.get('pengguna'),
                nama = post_data.get('nama'),
                jumlah = post_data.get('jumlah')
            )
            db.session.add(item)
            db.session.commit()
            resp = {
                'status': 'success',
                'message': 'successfully insert'
            }
            return make_response(jsonify(resp)), 201
        except Exception as e:
            # return (str(e))
            resp = {
                'status': 'fail',
                'message': 'some error occured' + e
            }
            return make_response(jsonify(resp)), 401

@apl.route('/transaksi', methods=['POST'])
@jwt_required
def create_transactions():
    post_data = request.get_json()
    if request.method == 'POST':
        try:
            transaksi = Transaksi(
                nama = post_data.get('nama'),
                item = post_data.get('item'),
                total = post_data.get('total')
            )
            db.session.add(transaksi)
            db.session.commit()
            resp = {
                'status': 'success',
                'message': 'successfully insert'
            }
            return make_response(jsonify(resp)), 201
        except Exception as e:
            # return (str(e))
            resp = {
                'status': 'fail',
                'message': 'some error occured' + e.getMessage()
            }
            return make_response(jsonify(resp)), 401

@apl.route('/admin', methods=['POST'])
@jwt_required
def create_admin():
    post_data = request.get_json()
    if request.method == 'POST':
        try:
            admin = Admin (
                nama = post_data.get('nama'),
                username = post_data.get('username'),
                password = post_data.get('password')
            )
            db.session.add(admin)
            db.session.commit()
            resp = {
                'status': 'success',
                'message': 'successfully insert'
            }
            return make_response(jsonify(resp)), 201
        except Exception as e:
            # return (str(e))
            resp = {
                'status': 'fail',
                'message': 'some error occurred' + e.getMessage()
            }
            return make_response(jsonify(resp)), 401
    
@apl.route('/pengguna/<id>', methods=['PUT'])
@jwt_required
def update_pengguna(id):
    post_data = request.get_json()
    pengguna = Pengguna.query.filter_by(id = post_data.get('id')).first()
    if not pengguna:
        if not isinstance(str):
            try:
                nama = str(request.data.get('nama', ''))
                pengguna.nama = nama
                db.session.add(pengguna)
                db.session.commit()
                resp = {
                    'id': pengguna.id,
                    'nama': pengguna.nama,
                    'alamat': pengguna.alamat,
                    'telepon': pengguna.telepon,
                    'username': pengguna.username,
                    'password': pengguna.password
                }
                return jsonify(resp), 200
            except Exception as e:
                return (str(e))

@apl.route('/item/<id>', methods=['PUT'])
@jwt_required 
def update_item(id):
    post_data = request.get_json()
    item = Item.query.filter_by(id = post_data.get('id')).first()
    if not item:
        if not isinstance(str):
            try: 
                nama = str(request.data.get('nama', ''))
                item.nama = nama
                db.session.add(item)
                db.session.commit()
                resp = {
                    'id': item.id,
                    'nama': item.nama,
                    'pengguna': item.pengguna,
                    'jumlah': item.jumlah
                }
                return jsonify(resp), 200
            except Exception as e:
                return(str(e))

@apl.route('/transaksi/<id>', methods=['PUT'])
@jwt_required 
def update_transaksi(id):
    post_data = request.get_json()
    transaksi = Transaksi.query.filter_by(id = post_data.get('id')).first()
    if not transaksi:
        if not isinstance(str):
            try:
                nama = str(request.data.get('nama', ''))
                transaksi.nama = nama
                db.session.add(transaksi)
                db.session.commit()
                resp = {
                    'id': transaksi.id,
                    'nama': transaksi.nama,
                    'item': transaksi.item,
                    'total': transaksi.total
                }
                return jsonify(resp), 200
            except Exception as e:
                return (str(e))

@apl.route('/admin/<id>', methods=['PUT'])
@jwt_required 
def update_admin(id):
    post_data = request.get_json()
    admin = Admin.query.filter_by(id = post_data.get('id')).first()
    if not admin:
        if not isinstance(str):
            try:
                nama = str(request.data.get('nama', ''))
                admin.nama = nama
                db.session.add(admin)
                db.session.commit()
                resp = {
                    'id': admin.id,
                    'nama': admin.nama,
                    'username': admin.username,
                    'password': admin.password
                }
                return jsonify(resp), 200
            except Exception as e:
                return (str(e))

@apl.route('/pengguna/<id>', methods=['DELETE'])
@jwt_required 
def hapus_pengguna(id):
    post_data = request.get_json()
    pengguna = Pengguna.query.filter_by(id = post_data.get('id')).first()
    if not pengguna:
        if not isinstance(str):
            try:
                db.session.delete(pengguna)
                db.session.commit()
                return {
                    "message": " user {} was deleted".format(pengguna.id)
                }, 200
            except Exception as e:
                return (str(e))

@apl.route('/item/<id>', methods=['DELETE'])
@jwt_required 
def hapus_item(id):
    post_data = request.get_json()
    item = Item.query.filter_by(id = post_data.get('id')).first()
    if not item:
        if not isinstance(str):
            try:
                db.session.delete(item)
                db.session.commit()
                return {
                    "message": "item {} was deleted".format(item.id)
                }
            except Exception as e:
                return (str(e))

@apl.route('/transaksi/<id>', methods=['DELETE'])
@jwt_required 
def hapus_transaksi(id):
    post_data = request.get_json()
    transaksi = Transaksi.query.filter_by(id = post_data.get('id')).first()
    if not transaksi:
        if not isinstance(str):
            try:
                db.session.delete(transaksi)
                db.session.commit()
                return {
                    "message": "transaction {} was deleted".format(transaksi.id)
                }
            except Exception as e:
                return (str(e))

@apl.route('/admin/<id>', methods=['DELETE'])
@jwt_required 
def hapus_admin(id):
    post_data = request.get_json()
    admin = Admin.query.filter_by(id = post_data.get('id')).first()
    if not admin:
        if not isinstance(str):
            db.session.delete(admin)
            db.session.commit()
            return {
                "message": "admin {} was deleted".format(admin.id)
            }

@apl.route('/registration', methods=['POST'])
def reg_user():
    data = request.get_json()
    if Pengguna.query.filter_by(username=data.get('username')).first():
        return jsonify({'message': 'User {} already exists'.format(data['username'])})
    new_user = Pengguna(
        nama = data['nama'],
        alamat = data['alamat'],
        telepon = data['telepon'],
        username = data['username'],
        password = Pengguna.generate_hash(data['password'])
    )
    try:
        new_user.save_to_db()
        access_token = create_access_token(identity = data['username'])
        refresh_token = create_refresh_token(identity = data['username'])
        return jsonify({
            'message': 'User {} was created'.format(data['username']),
            'access token': access_token,
            'refresh token': refresh_token
        })
    except:
        return jsonify({'message': 'something wrong'}), 500

@apl.route('/login', methods=['POST'])
def login_user():
    data = request.get_json()
    current_user = Pengguna.query.filter_by(username=data.get('username')).first()
    if not current_user:
        return jsonify({'message': 'User {} doesn\'t exists'.format(data['username'])})
    if Pengguna.verify_hash(data['password'], current_user.password):
        access_token = create_access_token(identity = data['username'])
        refresh_token = create_refresh_token(identity = data['username'])
        return jsonify({
            'message': 'Logged as {}'.format(current_user.username),
            'access token': access_token,
            'refresh token': refresh_token
        })
    else:
        return jsonify({'message': 'wrong credentials'})

if __name__ == '__main__':
    apl.run()