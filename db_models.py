import sqlalchemy as sq
from sqlalchemy.orm import declarative_base, relationship

Base = declarative_base()

class Bot_user(Base):
    __tablename__ = "bot_user"
    bot_user_id = sq.Column(sq.Integer, primary_key=True)
    #а нам действительно нужно поле никнейм? не совсем понимаю, когда будем выводить, но посмотрим
    nickname = sq.Column(sq.String(length=20), unique=True)
    from_age = sq.Column(sq.Integer, nullable=False)
    to_age = sq.Column(sq.Integer, nullable=False)
    gender = sq.Column(sq.String, nullable=False)
    city = sq.Column(sq.String, nullable=False)
    offset = sq.Column(sq.Integer, nullable=False)


class buffer_user_VK(Base):
    __tablename__ = "buffer_user_VK"
    user_id = sq.Column(sq.Integer, primary_key=True)
    VK_id = sq.Column(sq.Integer, unique=True, nullable=False)
    name = sq.Column(sq.String(length=20))
    surname = sq.Column(sq.String(length=20))
    link_to_profile = sq.Column(sq.String(length=40), unique=True, nullable=False)
    bot_user_id = sq.Column(sq.Integer, sq.ForeignKey("bot_user.bot_user_id"), nullable=False)
    bot_user = relationship(Bot_user, backref="users_VK")

class Blacklist(Base):
    __tablename__ = "blacklist"
    blacklist_VK_id = sq.Column(sq.Integer, primary_key=True)
    bot_user_id = sq.Column(sq.Integer, sq.ForeignKey("bot_user.bot_user_id"), nullable=False)
    bot_user = relationship(Bot_user, backref="blacklists")

class Favorite_VK(Base):
    __tablename__ = "favourite_VK"
    favourite_VK_id = sq.Column(sq.Integer, primary_key=True)
    name = sq.Column(sq.String(length=20))
    surname = sq.Column(sq.String(length=20))
    link_to_profile = sq.Column(sq.String(length=40), unique=True, nullable=False)
    bot_user_id = sq.Column(sq.Integer, sq.ForeignKey("bot_user.bot_user_id"), nullable=False)
    bot_user = relationship(Bot_user, backref="favourites")

class Photo_VK(Base):
    __tablename__ = "photo_VK"
    photo_id = sq.Column(sq.Integer, primary_key=True)
    user_VK_id = sq.Column(sq.Integer, sq.ForeignKey("favourite_VK.favourite_VK_id"), nullable=False)
    user_VK = relationship(Favorite_VK, backref="photos_VK")

def create_tables(engine):
    Base.metadata.drop_all(engine)
    Base.metadata.create_all(engine)