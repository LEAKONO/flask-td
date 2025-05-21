from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from models import db, Task, User

routes = Blueprint('routes', __name__)

@routes.route('/tasks', methods=['GET'])
@jwt_required()
def get_tasks():
    user_id = get_jwt_identity()
    tasks = Task.query.filter_by(user_id=user_id).all()
    return jsonify([{
        'id': t.id,
        'title': t.title,
        'is_done': t.is_done
    } for t in tasks])

@routes.route('/tasks', methods=['POST'])
@jwt_required()
def add_task():
    user_id = get_jwt_identity()
    data = request.get_json()
    task = Task(title=data['title'], user_id=user_id)
    db.session.add(task)
    db.session.commit()
    return jsonify(message="Task added"), 201

@routes.route('/tasks/<int:id>', methods=['PUT'])
@jwt_required()
def update_task(id):
    user_id = get_jwt_identity()
    task = Task.query.filter_by(id=id, user_id=user_id).first_or_404()
    data = request.get_json()
    task.title = data.get('title', task.title)
    task.is_done = data.get('is_done', task.is_done)
    db.session.commit()
    return jsonify(message="Task updated")

@routes.route('/tasks/<int:id>', methods=['DELETE'])
@jwt_required()
def delete_task(id):
    user_id = get_jwt_identity()
    task = Task.query.filter_by(id=id, user_id=user_id).first_or_404()
    db.session.delete(task)
    db.session.commit()
    return jsonify(message="Task deleted")
