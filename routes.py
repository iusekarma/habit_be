import json
from datetime import datetime
from flask import Blueprint, request, jsonify
from flask_jwt_extended import create_access_token, jwt_required, JWTManager, set_access_cookies, unset_jwt_cookies, get_jwt_identity
from werkzeug.security import generate_password_hash, check_password_hash
from models import db, User, Habits
from config import Config

routes_all = Blueprint('routes_all', __name__)
jwt = JWTManager()

@routes_all.route('/register', methods=['POST'])
def register():
    data = request.get_json()
    username = data.get('username')
    password = data.get('password')
    if not username or not password:
        return jsonify({'msg': 'Username and password required'}), 400

    hashed_password = generate_password_hash(password, method='sha256')
    new_user = User(username=username, password=hashed_password)
    db.session.add(new_user)
    db.session.commit()

    return jsonify({'msg': 'User registered successfully'}), 201

@routes_all.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    username = data.get('username')
    password = data.get('password')
    user = User.query.filter_by(username=username).first()
    if user and check_password_hash(user.password, password):
        access_token = create_access_token(identity=username)
        response = jsonify({'msg': 'Login successful'})
        set_access_cookies(response, access_token)
        return response
    return jsonify({'msg': 'Invalid credentials'}), 401

@routes_all.route('/logout', methods=['POST'])
@jwt_required()
def logout():
    response = jsonify({'msg': 'Logout successful'})
    unset_jwt_cookies(response)
    return response

@routes_all.route('/habits', methods=['GET'])
@jwt_required()
def get_user_habits():
    try:
        user = User.query.filter_by(username=get_jwt_identity()).first()
        habits = Habits.query.filter_by(user_id=user.id).all()
    except Exception as e:
        print(e)
        return jsonify({'msg': 'Error Occurred'})
    response = []
    for habit in habits:
        response.append({
            'id' : habit.id,
            'name' : habit.name,
            'desc' : habit.desc,
            'date_added' : habit.date_added,
            'completed' : habit.completed,
            'user_id' : habit.user_id
        })
    return jsonify(response)

@routes_all.route('/habits/<id>', methods=['GET'])
@jwt_required()
def get_user_habit(id):
    try:
        user = User.query.filter_by(username=get_jwt_identity()).first()
        habit = Habits.query.filter_by(id=id).first()
    except:
        return jsonify({'msg': 'Error Occured'})
    if habit.user_id == user.id:
        return jsonify({
            'id' : habit.id,
            'name' : habit.name,
            'desc' : habit.desc,
            'date_added' : habit.date_added,
            'completed' : habit.completed,
            'user_id' : habit.user_id
            })
    return jsonify({'msg': 'Error Occured'})

@routes_all.route('/habits', methods=['POST'])
@jwt_required()
def create_habit():
    data = request.get_json()
    name = data.get('name')
    desc = data.get('desc',None)
    user = User.query.filter_by(username=get_jwt_identity()).first()

    new_habit = Habits(name=name, desc=desc, user_id=user.id)
    db.session.add(new_habit)
    db.session.commit()

    return jsonify({'msg': 'Habit created successfully'}), 201

@routes_all.route('/habits/delete/<id>', methods=['POST'])
@jwt_required()
def delete_habit(id):
    try:
        user = User.query.filter_by(username=get_jwt_identity()).first()
        habit = Habits.query.filter_by(id=id).first()
    except:
        return jsonify({'msg': 'Error Occured'})
    if habit.user_id == user.id:
        db.session.delete(habit)
        db.session.commit()
        return jsonify({'msg': 'Deleted Successfully'})
    return jsonify({'msg': 'Error Occured'})


@routes_all.route('/habits/update/<id>', methods=['POST'])
@jwt_required()
def update_habit(id):
    data = request.get_json()
    name = data.get('name', None)
    desc = data.get('desc', None)
    try:
        user = User.query.filter_by(username=get_jwt_identity()).first()
        habit = Habits.query.filter_by(id=id).first()
    except:
        return jsonify({'msg': 'Error Occured'})
    if habit.user_id == user.id:
        if name: habit.name = name
        if desc: habit.desc = desc
        db.session.commit()
        return jsonify({
            'id' : habit.id,
            'name' : habit.name,
            'desc' : habit.desc,
            'date_added' : habit.date_added,
            'completed' : habit.completed,
            'user_id' : habit.user_id
            })
    return jsonify({'msg': 'Error Occured'}), 201

@routes_all.route('/habit_checked/<id>', methods=['POST'])
@jwt_required()
def habit_check(id):
    try:
        user = User.query.filter_by(username=get_jwt_identity()).first()
        habit = Habits.query.filter_by(id=id).first()
    except:
        return jsonify({'msg': 'Error Occured'})
    if habit.user_id == user.id:
        habit_array = json.loads(habit.completed)
        habit_array.append(datetime.now().isoformat())
        print(habit_array)
        habit.completed = json.dumps(habit_array)
        db.session.commit()
        return jsonify({'msg': 'Checked In Successfully!'})
    return jsonify({'msg': 'Error Occured'})