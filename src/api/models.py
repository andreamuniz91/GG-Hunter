from flask_sqlalchemy import SQLAlchemy


db = SQLAlchemy()


class Users(db.Model):
    __tablename__ = "users"
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(50), unique=True, nullable=False)
    password = db.Column(db.String(255), nullable=False)
    alias = db.Column(db.String(50))
    lastname = db.Column(db.String(50))
    birth_day = db.Column(db.DateTime)
    mobile_phone = db.Column(db.String(20))
    address = db.Column(db.String(100))
    country = db.Column(db.String(25))
    city = db.Column(db.String(50))
    zip_code = db.Column(db.String(10))
    imagen = db.Column(db.String(50))
    status = db.Column(db.Boolean)
    bio = db.Column(db.Text)
    rol = db.Column(db.Enum('admin', 'user', 'premium', name='role_enum'), nullable=False)
    created_at = db.Column(db.DateTime, default=db.func.current_timestamp())

    def __repr__(self):
        return f'<User {self.id} - {self.email}>'

    def serialize(self):
        return {
            "id": self.id,
            "email": self.email,
            "alias": self.alias,
            "lastname": self.lastname,
            "birth_day": self.birth_day,
            "mobile_phone": self.mobile_phone,
            "address": self.address,
            "country": self.country,
            "city": self.city,
            "zip_code": self.zip_code,
            "imagen": self.imagen,
            "status": self.status,
            "bio": self.bio,
            "rol": self.rol,
            "created_at": self.created_at
        }



class Favorites(db.Model):
    __tablename__ = 'favorites'
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), primary_key=True, nullable=False)
    game_id = db.Column(db.Integer, db.ForeignKey('games.id'), primary_key=True, nullable=False)
    user = db.relationship('Users', backref=db.backref('favorites', lazy=True))
    game = db.relationship('Games', backref=db.backref('favorites', lazy=True))

    def __repr__(self):
        return f'<Favorite UserID {self.user_id} - GameID {self.game_id}>'

    def serialize(self):
        return {
            "user_id": self.user_id,
            "game_id": self.game_id
        }


class SocialAccounts(db.Model):
    __tablename__ = "social_accounts"
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    provider = db.Column(db.String(50))
    social_id = db.Column(db.String(100))
    access_token = db.Column(db.String(255))
    user = db.relationship('Users', backref=db.backref('social_accounts', lazy=True))

    def __repr__(self):
        return f'<SocialAccount {self.id} - Provider {self.provider}>'

    def serialize(self):
        return {
            "id": self.id,
            "user_id": self.user_id,
            "provider": self.provider,
            "social_id": self.social_id,
            "access_token": self.access_token
        }


class Comments(db.Model):
    __tablename__ = "comments"
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    game_id = db.Column(db.Integer, db.ForeignKey('games.id'), nullable=False)
    body = db.Column(db.Text, nullable=False)
    created_at = db.Column(db.DateTime, default=db.func.current_timestamp())
    user = db.relationship('Users', backref=db.backref('comments', lazy=True))
    game = db.relationship('Games', backref=db.backref('comments', lazy=True))

    def __repr__(self):
        return f'<Comment {self.id} - User {self.user_id} - Game {self.game_id}>'

    def serialize(self):
        return {
            "id": self.id,
            "user_id": self.user_id,
            "game_id": self.game_id,
            "body": self.body,
            "created_at": self.created_at
        }


class Media(db.Model):
    __tablename__ = "media"
    id = db.Column(db.Integer, primary_key=True)
    game_id = db.Column(db.Integer, db.ForeignKey('games.id'))
    url = db.Column(db.String(255), nullable=False)
    caption = db.Column(db.Text)
    type_media = db.Column(db.Enum('video', 'imagen', name='media_type_enum'), nullable=False)
    uploaded_at = db.Column(db.DateTime, default=db.func.current_timestamp())
    game = db.relationship('Games', backref=db.backref('media', lazy=True))

    def __repr__(self):
        return f'<Media {self.id} - {self.url}>'

    def serialize(self):
        return {
            "id": self.id,
            "game_id": self.game_id,
            "url": self.url,
            "caption": self.caption,
            "type_media": self.type_media,
            "uploaded_at": self.uploaded_at
        }

      
class Games(db.Model):
    __tablename__ = "games"
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text)
    release_date = db.Column(db.Date)
    developer = db.Column(db.String(100))
    publisher = db.Column(db.String(100))
    
    def __repr__(self):
        return f'<Game {self.id} - {self.title}>'
      
    def serialize(self):
        return {
            "id": self.id,
            "title": self.title,
            "description": self.description,
            "release_date": self.release_date,
            "developer": self.developer,
            "publisher": self.publisher
        }      


class GamesCharacteristic(db.Model):
    __tablename__ = "games_characteristic"
    id = db.Column(db.Integer, primary_key=True)
    game_id = db.Column(db.Integer, db.ForeignKey('games.id'))
    plataform_id = db.Column(db.Integer, db.ForeignKey('plataforms.id'))
    filename = db.Column(db.String(255), nullable=False)
    filetype = db.Column(db.String(50))
    size = db.Column(db.Integer)
    minimun = db.Column(db.JSON)
    recomended = db.Column(db.JSON)

    def __repr__(self):
        return f'<GamesCharacteristic {self.id} - GameID {self.game_id}>'

    def serialize(self):
        return {
            "id": self.id,
            "game_id": self.game_id,
            "plataform_id": self.plataform_id,
            "filename": self.filename,
            "filetype": self.filetype,
            "size": self.size,
            "minimun": self.minimun,
            "recomended": self.recomended
        }


class Plataforms(db.Model):
    __tablename__ = "plataforms"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)

    def __repr__(self):
        return f'<Plataform {self.id} - {self.name}>'

    def serialize(self):
        return {
            "id": self.id,
            "name": self.name
        }
