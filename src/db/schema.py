from sqlalchemy import create_engine, Table, Column, Integer, String

from sqlalchemy import ForeignKey, DateTime, Text
from sqlalchemy.orm import declarative_base, relationship

Base = declarative_base()

engine = create_engine('sqlite:///example.db')
metadata = Base.metadata()

# many to many relationship between timelines and events
#
timelines_to_events = Table(
    "timelines_to_events",
    Base.metadata,
    Column("timeline_id", ForeignKey("timelines.id")),
    Column("event_id", ForeignKey("events.id")),
)


class Timeline(Base):
    __tablename__ = "timeline"
    id = Column(Integer, primary_key=True)
    children = relationship("Event", secondary=timelines_to_events)
    label = Column('label', String),


class Event(Base):
    __tablename__ = "event"
    id = Column(Integer, primary_key=True)
    start = Column('start', DateTime)
    end = Column('end', DateTime)
    label = Column('label', String)
    state = Column('state', String)
    notes = Column('notes', Text)


# Create the table in the database
metadata.create_all(engine)


# Insert some data into the table
conn = engine.connect()

# Select all users from the table
result = conn.execute(timelines_to_events.select())

# Print the results
for row in result:
    print(row)
conn.commit()
conn.close()
engine.dispose()
