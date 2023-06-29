import sqlalchemy as sq
from sqlalchemy.orm import declarative_base, relationship

Base = declarative_base()

class Bot_user(Base):
    __tablename__ = "bot_user"
    bot_user_id = sq.Column(sq.Integer, primary_key=True)
    nickname = sq.Column(sq.String(length=20), unique=True)
    age = sq.Column(sq.Integer, nullable=False)
    gender = sq.Column(sq.String, nullable=False)
    city = sq.Column(sq.String, nullable=False)

class User_VK(Base):
    __tablename__ = "user_VK"
    user_VK_id = sq.Column(sq.Integer, primary_key=True)
    name = sq.Column(sq.String(length=20), unique=True)
    surname = sq.Column(sq.String(length=20), unique=True)
    link_to_profile = sq.Column(sq.String(length=40), unique=True)
    bot_user_id = sq.Column(sq.Integer, sq.ForeignKey("bot_user.bot_user_id"), nullable=False)
    bot_user = relationship(Bot_user, backref="users_VK")

class Blacklist(Base):
    __tablename__ = "blacklist"
    blacklist_user_id = sq.Column(sq.Integer, primary_key=True)
    user_VK_id = sq.Column(sq.Integer, sq.ForeignKey("user_VK.user_VK_id"), nullable=False)
    user_VK = relationship(User_VK, backref="blacklists")

class Favorite_VK(Base):
    __tablename__ = "favorite_VK"
    favorite_id = sq.Column(sq.Integer, primary_key=True)
    user_VK_id = sq.Column(sq.Integer, sq.ForeignKey("user_VK.user_VK_id"), nullable=False)
    user_VK = relationship(User_VK, backref="favorites_VK")

class Photo_VK(Base):
    __tablename__ = "photo_VK"
    photo_id = sq.Column(sq.Integer, primary_key=True)
    media_id = sq.Column(sq.String(length=20), unique=True)
    user_VK_id = sq.Column(sq.Integer, sq.ForeignKey("user_VK.user_VK_id"), nullable=False)
    user_VK = relationship(User_VK, backref="photos_VK")

def create_tables(engine):
    Base.metadata.drop_all(engine)
    Base.metadata.create_all(engine)