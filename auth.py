from flask import Blueprint, request, jsonify
from models import db, User
from flask_jwt_extended import create_access_token
import datetime

auth = Blueprint('auth', __name__)

@auth.route('/signup', methods=['POST'])
def signup():
    data = request.get_json()
    if User.query.filter_by(email=data['email']).first():
        return jsonify(message="User already exists"), 409

    user = User(username=data['username'], email=data['email'])
    user.set_password(data['password'])
    db.session.add(user)
    db.session.commit()
    return jsonify(message="User created"), 201

@auth.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    user = User.query.filter_by(email=data['email']).first()
    if user and user.check_password(data['password']):
        token = create_access_token(identity=user.id, expires_delta=datetime.timedelta(hours=1))
        return jsonify(token=token)
    return jsonify(message="Invalid credentials"), 401
