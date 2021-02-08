from flask import Flask, jsonify, request, abort, redirect, url_for, session
from models import db, User
from werkzeug.security import generate_password_hash, check_password_hash
from flask_sqlalchemy import SQLAlchemy 
from sqlalchemy.dialects import postgresql
import psycopg2
from datetime import datetime
from flask_jwt_extended import JWTManager, create_access_token, get_jwt_identity
from flask_cors import CORS

app = Flask(__name__)
CORS(app)
jwt = JWTManager(app)
app.config['JWT_SECRET_KEY'] = 'secret'
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgres://postgres:root@localhost:5432/demodb'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db.init_app(app)
app.debug = True

@app.route("/api/Register", methods=["POST"])
def register():
    fname = request.get_json().get('fname')
    lname = request.get_json().get('lname')
    email = request.get_json().get('email')
    password = request.get_json().get('password')
    user = User.query.filter_by(email=email).first()
    if user is not None:
        return jsonify({'status': 'username already exists'}),401
    else:
        print(fname)
        newUser = User(fname=fname,
                       lname=lname,
                       email=email,
                       password=generate_password_hash(password, method='sha256'))
        db.session.add(newUser)
        db.session.commit()
        return jsonify({'status': 'successful'}),200

@app.route('/api/login', methods=['POST'])
def login():
    email = request.get_json().get('email')
    password = request.get_json().get('password')
    user = User.query.filter_by(email=email).first()
    
    if user is None:
        return jsonify({'status': 'invalid username'}),401
    elif not check_password_hash(user.password, password):
        return jsonify({'status': 'credentials do not match'})
    else:
        access_token = create_access_token(identity={
            'id': user.id,
            'fname': user.fname,
            'lname': user.lname,
            'email': user.email
        })
        return jsonify({'token': access_token , 'status': 'successful'} )

@app.route('/api/admin',methods=['GET'])
def viewUser():
    user = User.query.all()
    results = [{
            "id" : i.id,
            "fname" : i.fname,
            "lname" : i.lname,
            "email" : i.email
            }for i in user]
    return jsonify({ "user": results})

if __name__ == '__main__':
    app.run()