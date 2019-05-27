from app import db
from passlib.hash import pbkdf2_sha256  as sha256


class Pengguna(db.Model):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key = True, autoincrement=True)
    nama = db.Column(db.String())
    alamat = db.Column(db.String())
    telepon = db.Column(db.Integer)
    username = db.Column(db.String())
    password = db.Column(db.String())
    # nama backref harus unique
    item = db.relationship('Item', backref='own_pengguna', lazy='dynamic')

    def __init__(self, nama, alamat, telepon, username, password):

        self.nama = nama
        self.alamat = alamat
        self.telepon = telepon
        self.username = username
        self.password = password

    def __repr__(self):
        return '<id {}>'.format(self.id)

    def serialize(self):
        return {
            'id': self.id,
            'nama': self.nama,
            'alamat':self.alamat,
            'telepon':self.telepon,
            'username':self.username,
            'password':self.password
        }

    def save_to_db(self):
        db.session.add(self)
        db.session.commit()

    @staticmethod
    def generate_hash(password):
        return sha256.hash(password)

    @staticmethod
    def verify_hash(password, hash):
        return sha256.verify(password, hash)

class Item(db.Model):
    __tablename__ = 'items'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    pengguna = db.Column(db.Integer, db.ForeignKey('users.id'))
    nama = db.Column(db.String(),)
    jumlah = db.Column(db.Integer)
    transaksi = db.relationship('Transaksi', backref='own_item', lazy='dynamic')

    def __init__(self, pengguna, nama, jumlah):
        self.pengguna = pengguna
        self.nama = nama
        self.jumlah = self.jumlah

    def __repr__(self):
        return '<id {}>'.format(self.id)

    def serialize(self):
        return {
            'id':self.id,
            'pengguna':self.pengguna,
            'nama':self.nama,
            'jumlah':self.jumlah
        }
class Transaksi(db.Model):
    __tablename__ = 'transactions'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    nama = db.Column(db.String())
    item = db.Column(db.Integer, db.ForeignKey('items.id'))
    total = db.Column(db.Integer)

    def __init__(self, nama, item, total):
        self.nama = nama
        self.item = item
        self.total = total

# method ini berguna untuk membantu python tentang bagaimana mencetak objek kelas ini
    def __repr__(self):
        return '<id {}>'.format(self.id)

    def serialize(self):
        return {
            'id':self.id,
            'nama':self.nama,
            'item':self.item,
            'total':self.total
        }

class Admin(db.Model):
    __tablename__ = 'admins'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    nama = db.Column(db.String())
    username = db.Column(db.String())
    password = db.Column(db.String())

    def __init__(self, nama, username, password):
        self.nama = nama
        self.username = username
        self.password = password

    def __repr__(self):
        return '<id {}>'.format(self.id)

    def serialize(self):
        return {
            'id':self.id,
            'nama':self.nama,
            'username':self.username,
            'password':self.password
        }