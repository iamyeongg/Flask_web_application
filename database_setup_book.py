import os
import sys
from sqlalchemy import Column, ForeignKey, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
Base = declarative_base()


class BookStore(Base):
    __tablename__ = 'bookstore'

    id = Column(Integer, primary_key=True)
    name = Column(String(100), nullable=False)

    @property
    def serialize(self):
        """Return object data in easily serializeable format"""
        return {
            'name': self.name,
            'id': self.id,
        }


class BookItem(Base):
    __tablename__ = 'bookitem'

    name = Column(String(100), nullable=False)
    id = Column(Integer, primary_key=True)
    price = Column(String(8))
    bookstore_id = Column(Integer, ForeignKey('bookstore.id'))
    bookstore = relationship(BookStore)

    @property
    def serialize(self):
        """Return object data in easily serializeable format"""
        return {
            'name': self.name,
            'id': self.id,
            'price': self.price,
        }


engine = create_engine('mysql+pymysql://root:3536@localhost/bookstore')


Base.metadata.create_all(engine)


# 세션 생성
Session = sessionmaker(bind=engine)
session = Session()

# BookItem 데이터 추가
bookstore = BookStore(name='Bookstore 1')
session.add(bookstore)
session.commit()

bookitem1 = BookItem(name='Book 1', price='10', bookstore_id=bookstore.id)
bookitem2 = BookItem(name='Book 2', price='15', bookstore_id=bookstore.id)
bookitem3 = BookItem(name='Book 3', price='20', bookstore_id=bookstore.id)
bookitem4 = BookItem(name='Book 4', price='25', bookstore_id=bookstore.id)
bookitem5 = BookItem(name='Book 5', price='30', bookstore_id=bookstore.id)

session.add_all([bookitem1, bookitem2, bookitem3, bookitem4, bookitem5])
session.commit()
