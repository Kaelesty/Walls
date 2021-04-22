import sqlalchemy
from .db_session import SqlAlchemyBase
from sqlalchemy import orm


class Chat(SqlAlchemyBase):
    __tablename__ = 'chats'

    id = sqlalchemy.Column(sqlalchemy.Integer,
                           primary_key=True, autoincrement=True)
    name = sqlalchemy.Column(sqlalchemy.String)
    creator_id = sqlalchemy.Column(sqlalchemy.Integer,
                                   sqlalchemy.ForeignKey("users.id"))
    creator = orm.relation('User', foreign_keys=[creator_id])

    users = sqlalchemy.Column(sqlalchemy.String)

    def to_dict(self):
        return {
            "id": self.id,
            "name": self.name,
            "creator_id": self.creator_id,
            "users": self.users
        }
