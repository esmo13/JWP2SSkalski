from flask import Blueprint, request, jsonify, abort
from werkzeug.security import generate_password_hash, check_password_hash
from models import db, User, Artist, Genre

users_bp = Blueprint('users', __name__, url_prefix='/api/user/')

artists_bp = Blueprint('artists', __name__, url_prefix='/api/artists/')

genres_bp = Blueprint('genres', __name__, url_prefix='/api/genres/')

# @users_bp.route('/', methods=['OPTIONS'])
# @users_bp.route('/login',methods=['OPTIONS'])
# @artists_bp.route('/', methods=['OPTIONS'])
# def handle_preflight():
#     response = jsonify({})
#     response.headers.add('Access-Control-Allow-Origin', 'http://localhost:3000')
#     response.headers.add('Access-Control-Allow-Headers', 'Content-Type,Authorization')
#     response.headers.add('Access-Control-Allow-Methods', 'GET,PUT,POST,DELETE')
#     response.headers.add('Access-Control-Max-Age', '86400')
#     return response

@genres_bp.route('/',methods=["GET"])
def get_genres():
    genres = Genre.query.all()
    return jsonify([genre.to_dict() for genre in genres])

@genres_bp.route('/', methods=['POST'])
def create_genre():
    data = request.json
    if not data or not 'name' in data:
        abort(400)
    existing_genre = Genre.query.filter((Genre.name == data['name'])).first()
    if existing_genre:
        return jsonify({"message": "Genre with such name already exists"}), 400
    genre = Genre(
        name=data['name']
    )
    db.session.add(genre)
    db.session.commit()
    return jsonify(genre.to_dict()), 201

@artists_bp.route('/', methods=['GET'])
def get_artist():
    artists = Artist.query.all()
    return jsonify([artist.to_dict() for artist in artists])
@artists_bp.route('/', methods=['POST'])
def create_artist():
    data = request.json
    if not data or not 'name' in data or not 'country' in data:
        abort(400)
    existing_artist = Artist.query.filter((Artist.name == data['name']) & (Artist.country == data['country'])).first()
    if existing_artist:
        return jsonify({"message": "Artist with such name from this country already exists"}), 400
    artist = Artist(
        name=data['name'],
        country=data['country']
    )
    db.session.add(artist)
    db.session.commit()
    return jsonify(artist.to_dict()), 201



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