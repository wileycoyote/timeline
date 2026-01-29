from sqlalchemy import Column, Integer, String

from sqlalchemy import ForeignKey, Text
from sqlalchemy.orm import relationship

from .database import Base


# one to many relationship between timeline groups and events
class TimelineGroup(Base):
    __tablename__ = "timelinegroups"

    id = Column(Integer, primary_key=True, index=True)
    label = Column('label', String)
    colour = Column('colour', String)
    order = Column('order', Integer)
    # broken, continuous line, band
    line_type = Column('line_type', String)
    notes = Column('notes', Text)
    timelines = relationship("Timeline")


# granularity of time is one day
class Timeline(Base):
    __tablename__ = "timelines"

    id = Column(Integer, primary_key=True, index=True)
    label = Column('label', String)
    notes = Column('notes', Text)
    start = Column('start', String)
    end = Column('end', String)
    parent = Column(
        Integer,
        ForeignKey("timelinegroups.id")
    )
