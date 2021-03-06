import os
from flask import Flask, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_httpauth import HTTPDigestAuth

basedir = os.path.abspath(os.path.dirname(__file__))

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'data.sqlite')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = 'secret key here'
auth = HTTPDigestAuth()

users = {
    "vcu": "rams",
    "user2": "pass2"
}

@auth.get_password
def get_pw(username):
    if username in users:
        return users.get(username)
    return None

db = SQLAlchemy(app)

class ValidationError(ValueError):
    pass

class Role(db.Model):
    __tablename__= 'roles'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), unique=True)
    users = db.relationship('User', backref='role', lazy='dynamic')

    def __repr__(self):
        return '<Role %r>' % self.name




@app.route('/pong', methods=['GET'])
@auth.login_required
def pong_service():
    return jsonify({'pong':'Eroneous Information'})



@app.errorhandler(404)
def page_not_found(e):
    return jsonify({'message':'Page Is Not Here'}), 404

@app.errorhandler(500)
def internal_server_error(e):
    return jsonify({'message':'Something is broke'}), 500



if __name__ == '__main__':
    app.run()