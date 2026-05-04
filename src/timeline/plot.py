import matplotlib.pyplot as plt

import pandas as pd
from db.database import engine
from sqlalchemy import select
from db.models import EventGroup, Event
from datetime import datetime as dt
import pandas_log
import numpy as np
import matplotlib.dates as mdates

init_start_frame = "1500-01-01"
init_end_frame = "1526-01-01"

def_start_frame = dt.strptime(init_start_frame, "%Y-%m-%d")
def_end_frame = dt.strptime(init_end_frame, "%Y-%m-%d")
range_units = 54

conn = None


class Timeline(object):

    def __init__(self, s, e, ax):
        self.ax = ax
        self.date_start_frame = dt.strptime(s, "%Y-%m-%d")
        self.date_end_frame = dt.strptime(e, "%Y-%m-%d")
        self.get_data()
        self.display_slice()

    def get_data(self):
        stmt = select(EventGroup)
        # set up the dataframe for timeline groups
        self.events_group = pd.read_sql_query(
            stmt,
            con=engine,
            index_col='id',
        )
        # set up the dataframe for timelines
        stmt = select(Event, EventGroup).where(
            EventGroup.id == Event.parent)
        with pandas_log.enable():
            self.events = pd.read_sql_query(
                stmt,
                con=engine,
            )

    def increment_frame_years(self):
        new_date = np.datetime64(self.date_start_frame) +\
                                    np.timedelta64(1, 'Y')
        self.date_start_frame = new_date
        new_date = np.datetime64(self.date_start_frame) +\
            np.timedelta64(1, 'Y')
        self.date_end_frame = new_date

    def decrement_frame_years(self):
        new_date = np.datetime64(self.date_start_frame) -\
                                    np.timedelta64(1, 'Y')
        self.date_start_frame = new_date
        new_date = np.datetime64(self.date_start_frame) -\
            np.timedelta64(1, 'Y')
        self.date_end_frame = new_date

    def on_scroll(self, event):
        print(event.button, event.step)
        if event.button == 'up':
            self.increment_frame_years()
        elif event.button == 'down':
            self.decrement_frame_years()
        self.display_slice()

    def get_events_slice(self):
        s = self.date_start_frame
        e = self.date_end_frame
        # get all the events columns that intersect our time-slice
        #
        events_slice = self.events.query('date >= @s & date < @e')
        self.dates = [
            dt.strptime(d, "%Y-%m-%d")
            for d in events_slice['date'].values
        ]
        self.levels = [
            x for x in events_slice['level'].values
        ]
        self.colours = [
            x for x in events_slice['colour'].values
        ]
        self.labels = [
            x for x in events_slice['label'].values
        ]
        self.ext_labels = [
            x for x in events_slice['ext_labels'].values
        ]

    def display_slice(self):
        #
        # The baseline.
        self.get_events_slice()
        ax = self.ax
        ax.set(title="Events for 1300 to 1600")
        ax.axhline(0, c="black")
        ax.vlines(
            self.dates,
            0,
            self.levels,
            color=self.colours
        )
        #
        # The markers on the baseline.
        ax.plot(
            self.dates,
            np.zeros_like(self.dates),
            "-o",
            color="black",
            mfc="white"
        )
        #
        # set the top axis in years
        # set default values for now
        ax.margins(y=0.2)
        ax.set_ylim(-7, 7)
        # annotate the points on the horizontal line
        for d, level, colour, label, note in \
                zip(self.dates, self.levels, self.colours,
                    self.labels, self.notes):
            if note == "":
                annotate_label = label
            else:
                annotate_label = f"{label} ({note})"
            ax.annotate(
                annotate_label,
                xy=(d,
                    level),
                xytext=(-3, np.sign(level)*3),
                verticalalignment="bottom" if level > 0 else "top",
                textcoords="offset points",
                arrowprops=dict(
                    arrowstyle="-",
                    color=colour,
                    linewidth=2.0),
                bbox=dict(
                        boxstyle='square',
                        pad=0,
                        lw=0,
                        fc=(1, 1, 1, 0.7)
                    ),
                rotation=45
            )
        ax.yaxis.set_visible(False)
        ax.spines[["left", "top", "right"]].set_visible(False)

        ax.xaxis.set(
            major_locator=mdates.YearLocator(),
            major_formatter=mdates.DateFormatter("%Y"))
        ax.grid(False)


def run_app():
    # this initialises the data
    # this navigates the dates
    # to allow for distribution of horizontal timelines, this
    with plt.style.context('Solarize_Light2'):

        fig, ax = plt.subplots(figsize=(18, 9))
        t = Timeline(init_start_frame, init_end_frame, ax)
        fig.canvas.mpl_connect('key_press_event', t.on_scroll)
        plt.show()
