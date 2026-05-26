import matplotlib.pyplot as plt

import pandas as pd
import datetime
import numpy as np
from matplotlib.widgets import Button
from dateutil.relativedelta import relativedelta
from io import StringIO
import logging
import sys
import os

logger = logging.getLogger(__name__)

init_start_frame = (1500, 1, 1)
init_end_frame = (1526, 1, 1)
range_units = 54

conn = None
TESTDATA = """
id;label;date;inparens;parent;colour;level
1;Martin V;1417-01-01;;1;purple;1.5
2;Eugene IV;1431-01-01;;1;purple;1.5
3;Nicholas V;1447-01-01;;1;purple;1.5
4;Callixtus III;1455-01-01;;1;purple;1.5
5;Pius II;1458-01-01;;1;purple;1.5
6;Paul II;1464-01-01;;1;purple;1.5
7;Sixtus IV;1471-01-01;;1;purple;1.5
8;Innocent VIII;1484-01-01;;1;purple;1.5
9;Alexander VI;1492-01-01;;1;purple;1.5
10;Pius III;1503-01-01;;1;purple;1.5
11;Julius II;1503-06-01;;1;purple;1.5
12;Leo X;1513-06-01;;1;purple;1.5
13;Adrian VI;1522-01-01;;1;purple;1.5
14;Clement VII;1523-06-01;;1;purple;1.5
15;Paul III;1534-06-01;;1;purple;1.5
16;Julius III;1550-01-01;;1;purple;1.5
17;Marcellus II;1555-01-01;;1;purple;1.5
18;Paul IV;1555-06-01;;1;purple;1.5
19;Printing Press;1440-01-01;;2;blue;1
20;First Italian War;1494-01-01;start;3;green;0.8
21;First Italian War;1498-01-01;end;3;green;0.8
22;Second Italian War;1499-01-01;start;3;green;0.8
23;Second Italian War;1501-01-01;end;3;green;0.8
24;Third Italian War;1502-01-01;start;3;green;0.8
25;Third Italian War;1504-01-01;end;3;green;0.8
26;Fourth Italian War;1508-01-01;start;3;green;0.8
27;Fourth Italian War;1516-01-01;end;3;green;0.8
28;Fifth Italian War;1521-01-01;start;3;green;0.8
29;Fifth Italian War;1526-01-01;end;3;green;0.8
30;Sixth Italian War;1526-01-01;end;3;green;0.8
31;Sixth Italian War;1530-01-01;end;3;green;0.8
32;Seventh Italian War;1536-01-01;start;3;green;0.8
33;Seventh Italian War;1538-01-01;end;3;green;0.8
34;Eighth Italian War;1542-01-01;start;3;green;0.8
35;Eighth Italian War;1546-01-01;end;3;green;0.8
36;Ninth Italian War;1551-01-01;start;3;green;0.8
37;Ninth Italian War;1551-01-01;end;3;green;0.8
38;Giovanni Cimabue;1240-01-01;born;4;orange;-1
39;Giovanni Cimabue;1302-01-01;died;4;orange;-1
40;Jacopo della Quercia;1374-01-01;born;4;orange;-1
41;Jacopo della Quercia;1438-08-20;died;4;orange;-1
42;Leonardo da Vinci;1452-04-05;born;4;orange;-1
43;Leonardo da Vinci;1519-05-02;died;4;orange;-1
44;Michelangelo;1475-03-06;born;4;orange;-1
45;Michelangelo;1564-02-18;died;4;orange;-1
"""


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
        self.events = pd.read_csv(StringIO(TESTDATA), sep=";")

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

    def set_timeline_dict(self):
        self.data = dict()

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
    import pdb; pdb.set_trace()
    leaf = os.path.basename(sys.argv[0])
    log = f"logs/{leaf}.log"
    logging.basicConfig(filename=log, level=logging.INFO)
    logger.info('Started')
    # this initialises the data
    # this navigates the dates
    # to allow for distribution of horizontal timelines, this
    with plt.style.context('Solarize_Light2'):

        fig, ax = plt.subplots(figsize=(18, 9))
        Timeline(def_start_frame, def_end_frame, ax, fig)
        plt.show()
    logger.info("finished")
