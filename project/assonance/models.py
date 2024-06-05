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
    country = db.Column(db.String(100), nullable=False)
    def __eq__(self, other):
        return self.id == other.id

    def __hash__(self):
        return hash(self.id)
    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'country': self.country,
        }

class Genre(db.Model):
    __tablename__ = 'genres'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False)
    def __eq__(self, other):
        return self.id == other.id

    def __hash__(self):
        return hash(self.id)
    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name
        }
class Song(db.Model):
    __tablename__ = 'songs'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(200), nullable=False)
    def __eq__(self, other):
        return self.id == other.id

    def __hash__(self):
        return hash(self.id)
    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name
        }



album_artist_association = db.Table('album_artist',
    db.Column('album_id', db.Integer, db.ForeignKey('albums.id'), primary_key=True),
    db.Column('artist_id', db.Integer, db.ForeignKey('artists.id'), primary_key=True)
)

album_genre_association = db.Table('album_genre',
    db.Column('album_id', db.Integer, db.ForeignKey('albums.id'), primary_key=True),
    db.Column('genre_id', db.Integer, db.ForeignKey('genres.id'), primary_key=True)
)

album_song_association = db.Table('album_song',
    db.Column('album_id', db.Integer, db.ForeignKey('albums.id'), primary_key=True),
    db.Column('song_id', db.Integer, db.ForeignKey('songs.id'), primary_key=True)
)
class Album(db.Model):
    __tablename__ = 'albums'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(200), nullable=False)
    cover = db.Column(db.Text, nullable=False) 
    released = db.Column(db.Date, nullable=False)
    
    artists = db.relationship('Artist', secondary=album_artist_association, backref=db.backref('albums', lazy='dynamic'))
    genres = db.relationship('Genre', secondary=album_genre_association, backref=db.backref('albums', lazy='dynamic'))
    songs = db.relationship('Song', secondary=album_song_association, backref=db.backref('albums', lazy='dynamic'))
    
    def __eq__(self, other):
        return self.id == other.id

    def __hash__(self):
        return hash(self.id)

    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'cover': self.cover,
            'released': self.released.isoformat(),
            'author': self.artists[0].to_dict(),
            'genres': [genre.to_dict() for genre in self.genres],
            'songs': [song.to_dict() for song in self.songs]
        }

class Comment(db.Model):
    __tablename__ = 'comments'
    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.String(500), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    album_id = db.Column(db.Integer, db.ForeignKey('albums.id'), nullable=False)

    user = db.relationship('User', backref=db.backref('comments', lazy='dynamic'))
    album = db.relationship('Album', backref=db.backref('comments', lazy='dynamic'))

    def to_dict(self):
        return {
            'id': self.id,
            'content': self.content,
            'user_id': self.user_id,
            'album_id': self.album_id,
            'user_': self.user.to_dict() if self.user else None,
            'album': self.album.to_dict() if self.album else None
        }

class Rating(db.Model):
    __tablename__ = 'ratings'
    id = db.Column(db.Integer, primary_key=True)
    rating = db.Column(db.Integer, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    album_id = db.Column(db.Integer, db.ForeignKey('albums.id'), nullable=False)

    user = db.relationship('User', backref=db.backref('ratings', lazy='dynamic'))
    album = db.relationship('Album', backref=db.backref('ratings', lazy='dynamic'))

    def to_dict(self):
        return {
            'id': self.id,
            'rating': self.rating,
            'user_id': self.user_id,
            'album_id': self.album_id,
            'user': self.user.to_dict() if self.user else None,
            'album': self.album.to_dict() if self.album else None
        }
