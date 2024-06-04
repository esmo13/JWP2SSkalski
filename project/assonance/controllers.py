from flask import Blueprint, request, jsonify, abort
from werkzeug.security import generate_password_hash, check_password_hash
from models import db, User

users_bp = Blueprint('users', __name__, url_prefix='/api/user/')

@users_bp.route('/', methods=['GET'])
def get_users():
    users = User.query.all()
    return jsonify([user.to_dict() for user in users])

@users_bp.route('/<int:id>', methods=['GET'])
def get_user(id):
    user = User.query.get_or_404(id)
    return jsonify(user.to_dict())

@users_bp.route('/<int:id>', methods=['PUT'])
def update_user(id):
    user = User.query.get_or_404(id)
    data = request.json
    if not data or not 'name' in data or not 'email' in data or not 'password' in data or not 'role' in data:
        abort(400)
    user.name = data['name']
    user.email = data['email']
    user.password = generate_password_hash(data['password'])
    user.role = data['role']
    db.session.commit()
    return '', 204

@users_bp.route('/', methods=['POST'])
def create_user():
    data = request.json
    if not data or not 'name' in data or not 'email' in data or not 'password' in data or not 'role' in data:
        abort(400)
    existing_user = User.query.filter((User.name == data['name']) | (User.email == data['email'])).first()
    if existing_user:
        return jsonify({"message": "User with the same name or email already exists"}), 400
    user = User(
        name=data['name'],
        email=data['email'],
        password=generate_password_hash(data['password']),
        role=data['role']
    )
    db.session.add(user)
    db.session.commit()
    return jsonify(user.to_dict()), 201

@users_bp.route('/<int:id>', methods=['DELETE'])
def delete_user(id):
    user = User.query.get_or_404(id)
    db.session.delete(user)
    db.session.commit()
    return '', 204

@users_bp.route('/login/', methods=['POST'])
def login():
    data = request.json
    if not data or not 'name' in data or not 'password' in data:
        abort(400)
    user = User.query.filter_by(name=data['name']).first()
    if user and check_password_hash(user.password, data['password']):
        return jsonify(user.to_dict())
    else:
        return jsonify({"message": "Invalid credentials"}), 400