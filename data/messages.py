import sqlalchemy
from .db_session import SqlAlchemyBase
from sqlalchemy import orm
from flask_login import UserMixin


class Message_l1(SqlAlchemyBase, UserMixin):
    __tablename__ = 'messages_l1'

    id = sqlalchemy.Column(sqlalchemy.Integer,
                           primary_key=True, autoincrement=True)
    sender_id = sqlalchemy.Column(sqlalchemy.Integer,
                                sqlalchemy.ForeignKey("users.id"))
    sender = orm.relation('User')

    dialogue_id = sqlalchemy.Column(sqlalchemy.Integer,
                                  sqlalchemy.ForeignKey("dialogues.id"))
    dialogue = orm.relation('Dialogue')

    text = sqlalchemy.Column(sqlalchemy.String)


class Message_l2(SqlAlchemyBase, UserMixin):
    __tablename__ = 'messages_l2'

    id = sqlalchemy.Column(sqlalchemy.Integer,
                           primary_key=True, autoincrement=True)
    sender_id = sqlalchemy.Column(sqlalchemy.Integer,
                                sqlalchemy.ForeignKey("users.id"))
    sender = orm.relation('User')

    chat_id = sqlalchemy.Column(sqlalchemy.Integer,
                                  sqlalchemy.ForeignKey("chats.id"))
    chat = orm.relation('Chat')

    text = sqlalchemy.Column(sqlalchemy.String)

