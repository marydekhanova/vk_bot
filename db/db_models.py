import sqlalchemy as sq
from sqlalchemy.orm import declarative_base, relationship

Base = declarative_base()

class BotUser(Base):
    __tablename__ = "bot_user"
    bot_user_id = sq.Column(sq.Integer, primary_key=True)
    from_age = sq.Column(sq.Integer)
    to_age = sq.Column(sq.Integer)
    gender = sq.Column(sq.Integer)
    city = sq.Column(sq.String)
    offset = sq.Column(sq.Integer, nullable=False)
    VK_offset = sq.Column(sq.Integer, nullable=False)


class BufferUser(Base):
    __tablename__ = "buffer_user"
    user_id = sq.Column(sq.Integer, primary_key=True)
    VK_id = sq.Column(sq.Integer, nullable=False)
    name = sq.Column(sq.String(length=20))
    surname = sq.Column(sq.String(length=20))
    link_to_profile = sq.Column(sq.String(length=40), nullable=False)
    photo_ids = sq.Column(sq.ARRAY(sq.Integer))
    bot_user_id = sq.Column(sq.Integer, sq.ForeignKey("bot_user.bot_user_id"), nullable=False)
    bot_user = relationship(BotUser, backref="users_VK")

class Blacklist(Base):
    __tablename__ = "blacklist"
    id = sq.Column(sq.Integer, primary_key=True)
    bot_user_id = sq.Column(sq.Integer, sq.ForeignKey("bot_user.bot_user_id"), nullable=False)
    bot_user = relationship(BotUser, backref="blacklist_links")
    blacklist_VK_id = sq.Column(sq.Integer, nullable=False)

class Favourite(Base):
    __tablename__ = "favourite"
    favourite_VK_id = sq.Column(sq.Integer, primary_key=True)
    name = sq.Column(sq.String(length=20))
    surname = sq.Column(sq.String(length=20))
    link_to_profile = sq.Column(sq.String(length=40), unique=True, nullable=False)

class Photo(Base):
    __tablename__ = "photo"
    id = sq.Column(sq.Integer, primary_key=True)
    photo_id = sq.Column(sq.Integer)
    user_VK_id = sq.Column(sq.Integer, sq.ForeignKey("favourite.favourite_VK_id"), nullable=False)
    user_VK = relationship(Favourite, backref="photos")

class FavouriteUserLink(Base):
    __tablename__ = "favourite_bot_user"
    id = sq.Column(sq.Integer, primary_key=True)
    bot_user_id = sq.Column(sq.Integer, sq.ForeignKey("bot_user.bot_user_id"), nullable=False)
    bot_user = relationship(BotUser, backref="favourite_links")
    favourite_id = sq.Column(sq.Integer, sq.ForeignKey("favourite.favourite_VK_id"), nullable=False)
    favourite = relationship(Favourite, backref="favourite_links")

def create_tables(engine):
    Base.metadata.drop_all(engine)
    Base.metadata.create_all(engine)