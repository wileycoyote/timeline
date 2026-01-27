#!/usr/bin/env python
# from sqlalchemy.orm import Session
from database import SessionLocal
from models import TimelineGroup, Timeline
import csv


def import_csv_data():
    try:
        db = SessionLocal()
        db.commit()
        # build the data from ground up
        with open('data/timelines.csv') as csvfile:
            children = dict()
            timelines = csv.reader(csvfile, delimiter=',', quotechar='|')
            for t in timelines:
                key = t[0]
                if key not in children:
                    children[key] = []
                children[key].append(t)
        with open('data/timeline_groups.csv') as csvfile:
            timeline_gs = csv.reader(csvfile, delimiter=',', quotechar='|')
            for t in timeline_gs:
                print(', '.join(t))
                key = t[0]
                label = t[1]
                order = t[2]
                line_type = t[3]
                colour = t[4]
                notes = t[5]
                group = TimelineGroup(
                    label=label,
                    colour=colour,
                    order=order,
                    line_type=line_type,
                    notes=notes,
                )
                db.add(group)
                db.commit()
                for t in children[key]:
                    tl = Timeline(
                        label=t[1],
                        start=t[2],
                        end=t[3],
                        notes=t[4],
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


def get_tl_groups():

    return


def get_timelines():
    return


if __name__ == "__main__":
    import_csv_data()
