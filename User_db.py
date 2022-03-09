from sqlalchemy import MetaData, String, Column, BigInteger
from Db3_config import create_all_entities, Base

meta = MetaData()


class User(Base):
    __tablename__ = 'User'
    id = Column(BigInteger, primary_key=True, nullable=False, unique=True, autoincrement=True)
    user_name = Column(String, nullable=False, unique=True)
    password = Column(String, nullable=False)

    def __repr__(self):
        return f'User: (id={self.id}, user_name={self.user_name}, password={self.password})'

    def __str__(self):
        return f'User: [id={self.id}, user_name={self.user_name}, password={self.password}]'


create_all_entities()
