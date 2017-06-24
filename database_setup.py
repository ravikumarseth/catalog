#!/usr/bin/python
# -*- coding: utf-8 -*-
from sqlalchemy import Column, ForeignKey, Integer, String, DateTime, func
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship, backref
from sqlalchemy import create_engine

Base = declarative_base()


class User(Base):

    __tablename__ = 'user'
    id = Column(Integer, primary_key=True)
    name = Column(String(250), nullable=False)
    email = Column(String(250), nullable=False)
    picture = Column(String(250))


class GameGenre(Base):

    __tablename__ = 'gamegenre'

    name = Column(String(30), primary_key=True, nullable=False)
    description = Column(String(500), nullable=False)


class Game(Base):

    __tablename__ = 'game'

    name = Column(String(80), nullable=False)
    id = Column(Integer, primary_key=True)
    description = Column(String(500))
    time = Column(DateTime, default=func.now())
    genre = Column(String(30), ForeignKey('gamegenre.name'))
    gamegenre = relationship(GameGenre)
    user_id = Column(Integer, ForeignKey('user.id'))
    user = relationship(User, backref=backref("game", cascade="all, delete-orphan"))

    @property
    def serialize(self):
        return {
            'name': self.name,
            'description': self.description,
            'genre': self.genre,
            'id': self.id,
            }

    @property
    def serialize2(self):
        return {'name': self.name, 'description': self.description,
                'id': self.id}

        @classmethod
        def error(self):
            return {'status': 404, 'error': 'Data not found'}


engine = create_engine('sqlite:///games.db')

Base.metadata.create_all(engine)
