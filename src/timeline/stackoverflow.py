import matplotlib.pyplot as plt

import datetime
from matplotlib.widgets import Button
from dateutil.relativedelta import relativedelta
import logging
import sys
import os

logger = logging.getLogger(__name__)

init_start_frame = (1500, 1, 1)
init_end_frame = (1526, 1, 1)
range_units = 54


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

        self.display_slice()

    # implement key handlers and timer callback to shift the date window
    def on_key_press(self, event):
        # example single-step handling
        if event.key in ('right', 'd'):
            self.next()
        elif event.key in ('left', 'a'):
            self.prev()

    def on_key_release(self, event):
        pass

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
        e = self.date_end_frame.year
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
        ax.cla()
        print("#########")
        print("xticks")
        print(self.xticks)
        print(self.xlabels)
        ax.set_xticks(self.xticks, labels=self.xlabels, minor=True)
        print("#########")
        print(self.date_start_frame)
        print(self.date_end_frame)
        print("#########")
        ax.set_xlim(
            self.date_start_frame,
            self.date_end_frame
        )
        ax.set_ylim(-7, 7)
        ax.set(title="Events for 1300 to 1600")
        ax.axhline(0, c="black")
        ax.yaxis.set_visible(False)
        ax.spines[["left", "top", "right"]].set_visible(False)

        ax.grid(False)

        # self.fig.canvas.draw()
        self.fig.canvas.draw()


def run_app():
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
