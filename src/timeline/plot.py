import matplotlib.pyplot as plt

import pandas as pd
from db.database import engine
from sqlalchemy import select
from db.models import EventGroup, Event
import datetime
import pandas_log
import numpy as np
import matplotlib.dates as mdates

init_start_frame = (1500, 1, 1)
init_end_frame = (1526, 1, 1)

range_units = 54

conn = None


def dt_datetime(d):
    return datetime.date(d[0], d[1], d[2])


def_start_frame = dt_datetime(init_start_frame)
def_end_frame = dt_datetime(init_end_frame)


class Timeline(object):

    def __init__(self, s, e, ax, fig):
        self.ax = ax
        self.date_start_frame = s
        self.date_end_frame = e
        self.fig = fig
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
        timedelta = datetime.timedelta(days=365*5)
        self.date_start_frame = self.date_start_frame + timedelta
        self.date_end_frame = self.date_end_frame + timedelta

    def decrement_frame_years(self):
        timedelta = datetime.timedelta(days=365)
        self.date_start_frame = self.date_start_frame - timedelta
        self.date_end_frame = self.date_end_frame - timedelta

    def on_scroll(self, event):
        if event.key == 'right':
            self.increment_frame_years()
        elif event.key == 'left':
            self.decrement_frame_years()
        self.display_slice()

    def get_events_slice(self):
        s = str(self.date_start_frame.year)
        e = str(self.date_end_frame.year)
        # get all the events columns that intersect our time-slice
        #
        events_slice = self.events.query('date >= @s & date < @e')
        self.dates = [
            datetime.datetime.strptime(d, "%Y-%m-%d")
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
        self.inparens = [
            x for x in events_slice['inparens'].values
        ]

    def display_slice(self):
        #
        # The baseline.
        self.get_events_slice()
        ax = self.ax
        """
            The order is important for apps of this kind

            ax.cla()
            set locators/formatters
            set x-limits (datetimes or date2num)
            plot/vlines/annotate
            fig.canvas.draw_idle()
        """
        ax.cla()
        ax.xaxis.set(
            major_locator=mdates.YearLocator(),
            major_formatter=mdates.DateFormatter("%Y")
        )
        plt.xlim(
            self.date_start_frame,
            self.date_end_frame
        )
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
        for d, level, colour, label, inparens in \
                zip(self.dates, self.levels, self.colours,
                    self.labels, self.inparens):
            if inparens == "":
                annotate_label = label
            else:
                annotate_label = f"{label} ({inparens})"
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

        ax.grid(False)
        self.fig.canvas.draw()


def run_app():
    # this initialises the data
    # this navigates the dates
    # to allow for distribution of horizontal timelines, this
    with plt.style.context('Solarize_Light2'):

        fig, ax = plt.subplots(figsize=(18, 9))
        t = Timeline(def_start_frame, def_end_frame, ax, fig)
        fig.canvas.mpl_connect('key_press_event', t.on_scroll)
        plt.show()
