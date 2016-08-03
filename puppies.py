import os, sys
from sqlalchemy import Column, Date, Integer, ForeignKey, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine

Base = declarative_base()

class Shelter(Base):
    __tablename__ = "shelter"
    name = Column(String(40), nullable= False)
    address = Column(String(100))
    city = Column(String(50))
    state = Column(String(5))
    zipCode = Column(String(20))
    website = Column(String(50))
    id = Column(Integer, primary_key= True)

    @property
    def serialize(self):
        return {
            'name': self.name,
            'address': self.address,
            'city': self.city,
            'state': self.state,
            'zipCode': self.zipCode,
            'website': self.website,
            'id': self.id
        }

class Puppy(Base):
    __tablename__ = "puppy"
    name = Column(String(40), nullable= False)
    dateOfBirth = Column(Date)
    gender = Column(String(20), nullable= False)
    picture = Column(String)
    weight = Column(Integer)
    id = Column(Integer, primary_key= True)
    shelter_id = Column(Integer, ForeignKey("shelter.id"))

    @property
    def serialize(self):
        return {
            'name': self.name,
            'dateOfBirth': self.dateOfBirth,
            'gender': self.gender,
            'picture': self.picture,
            'weight': self.weight,
            'id': self.id
        }

engine = create_engine('sqlite:///puppyshelter.db')
Base.metadata.create_all(engine)
