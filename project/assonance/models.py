from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()



class User(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(200), nullable=False)
    email = db.Column(db.String(200), nullable=False, unique=True)
    password = db.Column(db.String(200), nullable=False)
    role = db.Column(db.Integer, nullable=False)

    def __init__(self, name, email, password, role):
        self.name = name
        self.email = email
        self.password = password
        self.role = role

    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'email': self.email,
            'password': self.password,
            'role': self.role
        }

    def __eq__(self, other):
        return self.id == other.id

    def __hash__(self):
        return hash(self.id)








class Artist(db.Model):
    __tablename__ = 'artists'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    albums = db.relationship('Album', backref='author', lazy=True)

class Genre(db.Model):
    __tablename__ = 'genres'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False)
    albums = db.relationship('AlbumGenre', back_populates='genre')

class Song(db.Model):
    __tablename__ = 'songs'
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    album_id = db.Column(db.Integer, db.ForeignKey('albums.id'), nullable=False)

class AlbumGenre(db.Model):
    __tablename__ = 'album_genre'
    album_id = db.Column(db.Integer, db.ForeignKey('albums.id'), primary_key=True)
    genre_id = db.Column(db.Integer, db.ForeignKey('genres.id'), primary_key=True)
    genre = db.relationship('Genre', back_populates='albums')
    album = db.relationship('Album', back_populates='genres')

class Album(db.Model):
    __tablename__ = 'albums'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(200), nullable=False)
    cover = db.Column(db.Text, nullable=False)
    author_id = db.Column(db.Integer, db.ForeignKey('artists.id'), nullable=False)
    released = db.Column(db.DateTime, nullable=True)
    genres = db.relationship('AlbumGenre', back_populates='album')
    songs = db.relationship('Song', backref='album', lazy=True)

    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'cover': self.cover,
            'author': self.author.name,
            'released': self.released.isoformat() if self.released else None,
            'genres': [genre.genre.name for genre in self.genres],
            'songs': [song.title for song in self.songs]
        }
