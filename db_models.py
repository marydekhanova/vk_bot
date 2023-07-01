import sqlalchemy as sq
from sqlalchemy.orm import declarative_base, relationship

Base = declarative_base()

class BotUser(Base):
    __tablename__ = "bot_user"
    bot_user_id = sq.Column(sq.Integer, primary_key=True)
    #а нам действительно нужно поле никнейм? не совсем понимаю, когда будем выводить, но посмотрим
    nickname = sq.Column(sq.String(length=20), unique=True)
    from_age = sq.Column(sq.Integer, nullable=False)
    to_age = sq.Column(sq.Integer, nullable=False)
    gender = sq.Column(sq.String, nullable=False)
    city = sq.Column(sq.String, nullable=False)
    offset = sq.Column(sq.Integer, nullable=False)
    VK_offset = sq.Column(sq.Integer, nullable=False)


class BufferUser(Base):
    __tablename__ = "buffer_user"
    user_id = sq.Column(sq.Integer, primary_key=True)
    VK_id = sq.Column(sq.Integer, nullable=False)
    name = sq.Column(sq.String(length=20))
    surname = sq.Column(sq.String(length=20))
    link_to_profile = sq.Column(sq.String(length=40), unique=True, nullable=False)
    bot_user_id = sq.Column(sq.Integer, sq.ForeignKey("bot_user.bot_user_id"), nullable=False)
    bot_user = relationship(BotUser, backref="users_VK")

class Blacklist(Base):
    __tablename__ = "blacklist"
    blacklist_VK_id = sq.Column(sq.Integer, primary_key=True)

class Favorite(Base):
    __tablename__ = "favourite"
    favourite_VK_id = sq.Column(sq.Integer, primary_key=True)
    name = sq.Column(sq.String(length=20))
    surname = sq.Column(sq.String(length=20))
    link_to_profile = sq.Column(sq.String(length=40), unique=True, nullable=False)
    bot_user_id = sq.Column(sq.Integer, sq.ForeignKey("bot_user.bot_user_id"), nullable=False)
    bot_user = relationship(BotUser, backref="favourites")

class Photo(Base):
    __tablename__ = "photo"
    photo_id = sq.Column(sq.Integer, primary_key=True)
    user_VK_id = sq.Column(sq.Integer, sq.ForeignKey("favourite.favourite_VK_id"), nullable=False)
    user_VK = relationship(Favorite, backref="photos")

class BlacklistUserLink(Base):
    __tablename__ = "blacklist_bot_user"
    id = sq.Column(sq.Integer, primary_key=True)
    bot_user_id = sq.Column(sq.Integer, sq.ForeignKey("bot_user.bot_user_id"), nullable=False)
    bot_user = relationship(BotUser, backref="blacklist_links")
    blacklist_id = sq.Column(sq.Integer, sq.ForeignKey("blacklist.blacklist_VK_id"), nullable=False)
    blacklist = relationship(Blacklist, backref="blacklist_links")

class FavouriteUserLink(Base):
    __tablename__ = "favourite_bot_user"
    id = sq.Column(sq.Integer, primary_key=True)
    bot_user_id = sq.Column(sq.Integer, sq.ForeignKey("bot_user.bot_user_id"), nullable=False)
    bot_user = relationship(BotUser, backref="favourite_links")
    favourite_id = sq.Column(sq.Integer, sq.ForeignKey("favourite.favourite_VK_id"), nullable=False)
    favourite = relationship(Favorite, backref="favourite_links")

def create_tables(engine):
    Base.metadata.drop_all(engine)
    Base.metadata.create_all(engine)