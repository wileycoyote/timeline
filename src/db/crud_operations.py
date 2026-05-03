#!/usr/bin/env python
# from sqlalchemy.orm import Session
from .database import SessionLocal
from .models import EventGroup, Event
import csv


def import_csv_data():
    try:
        db = SessionLocal()
        # build the data from ground up
        with open('data/events.csv') as csvfile:
            children = dict()
            timelines = csv.reader(
                csvfile,
                delimiter=',',
                quotechar='|',
                skipinitialspace=True
            )
            for t in timelines:
                key = t[0]
                if key not in children:
                    children[key] = []
                children[key].append(t)
        with open('data/event_groups.csv') as csvfile:
            timeline_gs = csv.reader(csvfile, delimiter=',', quotechar='|')
            for t in timeline_gs:
                key = t[0]
                label = t[1]
                level = t[2]
                colour = t[3]
                notes = t[4]
                group = EventGroup(
                    label=label,
                    colour=colour,
                    level=level,
                    notes=notes,
                )
                db.add(group)
                db.commit()
                for t in children[key]:
                    tl = Event(
                        label=t[1],
                        date=t[2],
                        notes=t[3],
                        parent=group.id
                    )
                    db.add(tl)
                    db.commit()
    except Exception as e:
        print(f"❌ Error creating sample data: {e}")
        db.rollback()
    finally:
        db.close()
    return


if __name__ == "__main__":
    import_csv_data()
