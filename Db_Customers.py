from sqlalchemy import MetaData, String, Column, BigInteger
from Db3_config import create_all_entities, Base

meta = MetaData()


class Customer(Base):
    __tablename__ = 'Customer'
    id = Column(BigInteger, primary_key=True, nullable=False, unique=True)
    name = Column(String, nullable=False)
    address = Column(String, nullable=True)

    def __repr__(self):
        return f'Customer: (id={self.id}, name={self.name}, address={self.address})'

    def __str__(self):
        return f'Customer: [id={self.id}, name={self.name}, address={self.address}]'


create_all_entities()
