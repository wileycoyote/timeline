import matplotlib.pyplot as plt

import pandas as pd
from db.database import engine
from sqlalchemy import select
from db.models import EventGroup, Event
import datetime
import pandas_log
import numpy as np
import matplotlib.dates as mdates
from matplotlib.widgets import Button
from dateutil.relativedelta import relativedelta

init_start_frame = (1500, 1, 1)
init_end_frame = (1526, 1, 1)

range_units = 54

conn = None


def dt_datetime(d):
    return datetime.datetime(d[0], d[1], d[2])


def_start_frame = dt_datetime(init_start_frame)
def_end_frame = dt_datetime(init_end_frame)


class Timeline(object):

    def __init__(self, s, e, ax, fig):
        self.ax = ax
        self.date_start_frame = s
        self.date_end_frame = e
        self.fig = fig
        self.get_data()
        import pdb; pdb.set_trace()
        # create navigation buttons ONCE (use positions inside [0,1])
        axprev = self.fig.add_axes([0.81, 0.02, 0.08, 0.04])
        axnext = self.fig.add_axes([0.90, 0.02, 0.08, 0.04])
        self.bprev = Button(axprev, 'Previous')
        self.bnext = Button(axnext, 'Next')
        self.bprev.on_clicked(self.onclick_prev)
        self.bnext.on_clicked(self.onclick_next)

        # ensure the canvas has keyboard focus (backend-specific)
        try:
            self.fig.canvas.set_focus()      # modern Matplotlib
        except Exception:
            try:
                self.fig.canvas.setFocus()   # Qt backend
            except Exception:
                try:
                    self.fig.canvas.get_tk_widget().focus_set()  # Tk backend
                except Exception:
                    pass

        # connect key events once
        self.fig.canvas.mpl_connect('key_press_event', self.on_key_press)
        self.fig.canvas.mpl_connect('key_release_event', self.on_key_release)

        # (optional) timer for continuous scrolling
        # self._timer = self.fig.canvas.new_timer(interval=30)
        # self._timer.add_callback(self._on_timer)
        # self._timer.start()

        self.display_slice()

    # implement key handlers and timer callback to shift the date window
    def on_key_press(self, event):
        print(f"on keypress {event.key}")
        # example single-step handling
        if event.key in ('right', 'd'):
            self.next()
        elif event.key in ('left', 'a'):
            self.prev()

    def on_key_release(self, event):
        pass

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
        timedelta = relativedelta(years=5)
        self.date_start_frame = self.date_start_frame + timedelta
        self.date_end_frame = self.date_end_frame + timedelta

    def decrement_frame_years(self):
        timedelta = relativedelta(years=5)
        self.date_start_frame = self.date_start_frame - timedelta
        self.date_end_frame = self.date_end_frame - timedelta

    def onclick_next(self, event):
        self.next()

    def onclick_prev(self, event):
        self.prev()

    def next(self):
        self.increment_frame_years()
        self.display_slice()

    def prev(self):
        self.decrement_frame_years()
        self.display_slice()

    def get_events_slice(self):
        s = self.date_start_frame.year
        s1 = str(s)
        e = self.date_end_frame.year
        e1 = str(e)
        # get all the events columns that intersect our time-slice
        #
        events_slice = self.events.query('date >= @s1 & date < @e1')
        import pprint; pprint.pprint(events_slice)
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
        self.xticks = [
            x for x in range(s, e + 1)
        ]
        self.xlabels = [
            str(x) for x in range(s, e + 1)
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
        """ ax.xaxis.set(
            major_locator=mdates.YearLocator(),
            major_formatter=mdates.DateFormatter("%Y")
        )"""
        print("#########")
        print(self.xticks)
        print(self.xlabels)
        ax.set_xticks(self.xticks, labels=self.xlabels, minor=True)
        print("#########")
        print(self.date_start_frame)
        print(self.date_end_frame)
        print("#########")
        plt.xlim(
            self.date_start_frame,
            self.date_end_frame
        )
        ax.set_ylim(-7, 7)
        ax.set(title="Events for 1300 to 1600")
        ax.axhline(0, c="black")
        print(self.dates)
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

        # self.fig.canvas.draw()
        self.fig.canvas.draw()


def run_app():
    # this initialises the data
    # this navigates the dates
    # to allow for distribution of horizontal timelines, this
    with plt.style.context('Solarize_Light2'):

        fig, ax = plt.subplots(figsize=(18, 9))
        Timeline(def_start_frame, def_end_frame, ax, fig)
        plt.show()
