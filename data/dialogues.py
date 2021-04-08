import sqlalchemy
from .db_session import SqlAlchemyBase
from sqlalchemy import orm



class Dialogue(SqlAlchemyBase):
    __tablename__ = 'dialogues'

    id = sqlalchemy.Column(sqlalchemy.Integer,
                           primary_key=True, autoincrement=True)
    first_user_id = sqlalchemy.Column(sqlalchemy.Integer,
                                sqlalchemy.ForeignKey("users.id"))
    first_user = orm.relation('User', foreign_keys=[first_user_id])

    second_user_id = sqlalchemy.Column(sqlalchemy.Integer,
                                   sqlalchemy.ForeignKey("users.id"))
    second_user = orm.relation('User', foreign_keys=[second_user_id])

