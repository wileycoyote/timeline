from sqlalchemy import Column, Integer, String

from sqlalchemy import ForeignKey, Text
from sqlalchemy.orm import relationship

from .database import Base


# one to many relationship between timeline groups and events
class EventGroup(Base):
    __tablename__ = "eventgroups"

    id = Column(Integer, primary_key=True, index=True)
    label = Column('label', String)
    colour = Column('colour', String)
    level = Column('level', Integer)
    notes = Column('notes', Text)
    events = relationship("Event")


# granularity of time is one day
class Event(Base):
    __tablename__ = "events"

    id = Column(Integer, primary_key=True, index=True)
    label = Column('label', String)
    notes = Column('notes', Text)
    date = Column('date', Text)
    parent = Column(
        Integer,
        ForeignKey("eventgroups.id")
    )
