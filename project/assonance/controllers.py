from flask import Blueprint, request, jsonify, abort
from sqlalchemy.sql import func
from werkzeug.security import generate_password_hash, check_password_hash
from models import db, User, Artist, Genre, Song, Album, Comment, Rating
from datetime import datetime
from sqlalchemy.orm import joinedload
users_bp = Blueprint('users', __name__, url_prefix='/api/user/')

artists_bp = Blueprint('artists', __name__, url_prefix='/api/artists/')

genres_bp = Blueprint('genres', __name__, url_prefix='/api/genres/')

albums_bp = Blueprint('albums',__name__,url_prefix='/api/albums/')

comments_bp = Blueprint('comments',__name__,url_prefix='/api/comments/')

ratings_bp = Blueprint('rating',__name__,url_prefix='/api/rating')


@albums_bp.route('/count', methods=['GET'])
def get_album_count():
    album_count = db.session.query(func.count(Album.id)).scalar()
    return jsonify({'album_count': album_count}), 200

@artists_bp.route('/count', methods=['GET'])
def get_artist_count():
    artist_count = db.session.query(func.count(Artist.id)).scalar()
    return jsonify({'artist_count': artist_count}), 200

@comments_bp.route('/count', methods=['GET'])
def get_comment_count():
    comment_count = db.session.query(func.count(Comment.id)).scalar()
    return jsonify({'comment_count': comment_count}), 200

@ratings_bp.route('/count', methods=['GET'])
def get_rating_count_whole():
    rating_count = db.session.query(func.count(Rating.id)).scalar()
    return jsonify({'rating_count': rating_count}), 200


@ratings_bp.route('/count/<int:album_id>', methods=['GET'])
def get_rating_count(album_id):
    rating_count = db.session.query(func.count(Rating.id)).filter_by(album_id=album_id).scalar()

    if rating_count is None:
        return jsonify({'error': 'No ratings found for this album'}), 404

    return jsonify({'album_id': album_id, 'rating_count': rating_count}), 200

@ratings_bp.route('/<int:rating_id>', methods=['PUT'])
def update_rating(rating_id):
    data = request.json
    new_rating_value = data.get('rating')

    if new_rating_value is None:
        return jsonify({'error': 'Missing rating value'}), 400

    rating = Rating.query.get(rating_id)

    if not rating:
        return jsonify({'error': 'Rating not found'}), 404

    rating.rating = new_rating_value
    db.session.commit()

    return jsonify(rating.to_dict()), 200



@ratings_bp.route('/', methods=['POST'])
def add_rating():
    data = request.json
    rating_value = data.get('rating')
    user_id = data.get('userid')
    album_id = data.get('albumid')

    if not (rating_value and user_id and album_id):
        return jsonify({'error': 'Missing data'}), 400

    if not (1 <= rating_value <= 5):  # Assuming a rating scale of 1-5
        return jsonify({'error': 'Invalid rating value'}), 400

    user = User.query.get(user_id)
    album = Album.query.get(album_id)

    if not user or not album:
        return jsonify({'error': 'User or Album not found'}), 404

    rating = Rating(rating=rating_value, user_id=user_id, album_id=album_id)
    db.session.add(rating)
    db.session.commit()

    return jsonify(rating.to_dict()), 201

@ratings_bp.route('/<int:album_id>/<int:user_id>', methods=['GET'])
def get_rating_by_user(album_id, user_id):
    rating = Rating.query.filter_by(album_id=album_id, user_id=user_id).first()

    if not rating:
        return jsonify({'error': 'Rating not found'}), 404

    return jsonify(rating.to_dict()), 200

@ratings_bp.route('/avg/<int:album_id>', methods=['GET'])
def get_average_rating(album_id):
    avg_rating = db.session.query(func.avg(Rating.rating)).filter_by(album_id=album_id).scalar()

    if avg_rating is None:
        return jsonify({'error': 'No ratings found for this album'}), 404

    return jsonify({'album_id': album_id, 'average_rating': round(avg_rating, 2)}), 200

@comments_bp.route('/', methods=['POST'])
def add_comment():
    data = request.json
    content = data.get('content')
    user_id = data.get('user_').get('id')
    album_id = data.get('album_').get('id')

    if not (content and user_id and album_id):
        return jsonify({'error': 'Missing data'}), 400

    comment = Comment(content=content, user_id=user_id, album_id=album_id)
    db.session.add(comment)
    db.session.commit()

    return jsonify(comment.to_dict()), 201

@comments_bp.route('/ofalbum/<int:album_id>', methods=['GET'])
def get_comments_by_album(album_id):
    album = Album.query.get(album_id)

    if not album:
        return jsonify({'error': 'Album not found'}), 404

    comments = Comment.query.options(
        joinedload(Comment.user)
    ).filter_by(album_id=album_id).all()

    comments_list = [comment.to_dict() for comment in comments]
    return jsonify(comments_list), 200




# @ratings_bp.route('/', methods=['OPTIONS'])
# @users_bp.route('/', methods=['OPTIONS'])
# @users_bp.route('/login',methods=['OPTIONS'])
# @artists_bp.route('/', methods=['OPTIONS'])
# @albums_bp.route('/',methods=['OPTIONS'])
# def handle_preflight():
#     response = jsonify({})
#     response.headers.add('Access-Control-Allow-Origin', 'http://frontend:3000')
#     response.headers.add('Access-Control-Allow-Headers', 'Content-Type,Authorization')
#     response.headers.add('Access-Control-Allow-Methods', 'GET,PUT,POST,DELETE')
#     response.headers.add('Access-Control-Max-Age', '86400')
#     return response

@albums_bp.route('/', methods=['GET'])
def get_albums():
    albums = Album.query.options(
        joinedload(Album.artists),
        joinedload(Album.genres),
        joinedload(Album.songs)
    ).all()

    albums_list = [album.to_dict() for album in albums]
    return jsonify(albums_list), 200

@albums_bp.route('/<int:album_id>', methods=['GET'])
def get_album(album_id):
    album = Album.query.options(
        joinedload(Album.artists),
        joinedload(Album.genres),
        joinedload(Album.songs)
    ).filter_by(id=album_id).first()

    if album is None:
        return jsonify({'error': 'Album not found'}), 404
    print(album.to_dict())
    return jsonify(album.to_dict()), 200
@albums_bp.route('/', methods=['POST'])
def add_album():
    data = request.json
    print(data.get('released'))
    name = data.get('name')
    cover = data.get('cover')
    released = data.get('released')
    artist_ids = [data.get('author').get('id')]
    genre_ids = [data.get('genres')[0].get('id')]
    songs_data = data.get('songs')

    # Validate input data
    if not (name and cover and released and artist_ids and genre_ids and songs_data):
        return jsonify({'error': 'Missing data'}), 400

    try:
        creation_date = datetime.strptime(released, '%Y-%m-%d').date()
    except ValueError:
        return jsonify({'error': 'Invalid date format'}), 400

    # Fetch existing artists and genres
    artists = Artist.query.filter(Artist.id.in_(artist_ids)).all()
    genres = Genre.query.filter(Genre.id.in_(genre_ids)).all()

    if len(artists) != len(artist_ids):
        return jsonify({'error': 'One or more artists not found'}), 404

    if len(genres) != len(genre_ids):
        return jsonify({'error': 'One or more genres not found'}), 404

    # Create new songs
    songs = []
    for song_data in songs_data:
        song_name = song_data.get('name')
        if not song_name:
            return jsonify({'error': 'Song name missing'}), 400
        song = Song(name=song_name)
        songs.append(song)

    # Create new album
    album = Album(
        name=name,
        cover=cover,
        released=creation_date,
        artists=artists,
        genres=genres,
        songs=songs
    )

    db.session.add(album)
    db.session.commit()

    return jsonify(album.to_dict()), 201



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
    if not data or not 'name' in data or not 'email' in data or not 'role' in data:
        abort(400)
    user.name = data['name']
    user.email = data['email']
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
    print(user.to_dict())
    if user and check_password_hash(user.password, data['password']):
        return jsonify(user.to_dict())
    else:
        return jsonify({"message": "Invalid credentials"}), 400