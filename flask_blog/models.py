from datetime import datetime
import flask
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer
from flask_blog import db, loginManager, app
from flask import current_app
from flask_login import UserMixin

@loginManager.user_loader
def load_user(user_id):
    return Usuario.query.get(int(user_id))

class Usuario(db.Model, UserMixin):
    id =  db.Column(db.Integer, primary_key=True)
    usuarionombre = db.Column(db.String(20), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    image_file = db.Column(db.String(20), nullable=False, default='default.jpg')
    password = db.Column(db.String(60), nullable=False)
    posts = db.relationship('Post', backref='autor', lazy=True)

    def __repr__(self):
        return f"User('{self.usuarionombre}', '{self.email}', '{self.image_file}')"

    def get_reset_token(self, expires_sec=1800):
        s = Serializer(current_app.config['SECRET_KEY'], expires_sec)
        return s.dumps({'user_id': self.id}).decode('utf-8')

    @staticmethod
    def verify_reset_token(token):
        s = Serializer(current_app.config['SECRET_KEY'])
        try:
            user_id = s.loads(token)['user_id']
        except:
            return None
        return Usuario.query.get(user_id)

class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    titulo =db.Column(db.String(100), nullable=False)
    fecha = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    contenido = db.Column(db.Text, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('usuario.id'), nullable=False)

    def __repr__(self):
        return f"Post('{self.titulo}', '{self.fecha}')"