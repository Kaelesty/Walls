import sqlalchemy
from .db_session import SqlAlchemyBase
from sqlalchemy import orm


class Message(SqlAlchemyBase):
    __tablename__ = 'messages'

    id = sqlalchemy.Column(sqlalchemy.Integer,
                           primary_key=True, autoincrement=True)
    text = sqlalchemy.Column(sqlalchemy.String, nullable=True)
    user_id = sqlalchemy.Column(sqlalchemy.Integer, 
                                sqlalchemy.ForeignKey("users.id"))
    user = orm.relation('User')

    chat_id = sqlalchemy.Column(sqlalchemy.Integer,
                                sqlalchemy.ForeignKey("chats.id"))
    chat = orm.relation('Chat')