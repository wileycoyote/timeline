import matplotlib.pyplot as plt

import pandas as pd
from db.database import engine
from sqlalchemy import select
from db.models import TimelineGroup, Timeline
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


def get_data():

    stmt = select(TimelineGroup)
    # set up the dataframe for timeline groups
    t_df = pd.read_sql_query(
        stmt,
        con=engine,
        index_col='id',
    )
    # set up the dataframe for timelines
    stmt = select(Timeline, TimelineGroup).where(
        TimelineGroup.id == Timeline.parent)
    with pandas_log.enable():
        e_df = pd.read_sql_query(
            stmt,
            con=engine,
        )
    return t_df, e_df


def get_timelines_slice(df, s, e):
    # get all the events columns that intersect our time-slice
    #
    slice_df = df.query('start >= @s & start < @e')
    return slice_df


def run_app():
    # this initialises the data
    t_df, e_df = get_data()
    # import pdb;pdb.set_trace()
    # this navigates the dates
    events_slice = get_timelines_slice(e_df, init_start_frame, init_end_frame)
    # import pdb; pdb.set_trace()
    dates = [
        dt.strptime(d, "%Y-%m-%d")
        for d in events_slice['start'].values
    ]
    levels = [
        x for x in events_slice['level'].values
    ]

    # to allow for distribution of horizontal timelines, this
    with plt.style.context('Solarize_Light2'):
        fig, ax = plt.subplots(figsize=(18, 9))
        ax.set(title="Timelines for 1300 to 1600")
        #
        # The baseline.
        ax.axhline(0, c="black")
        ax.vlines(dates, 0, levels)
        #
        # The markers on the baseline.
        ax.plot(
            dates,
            np.zeros_like(dates),
            "-o",
            color="black",
            mfc="white"
        )
        #
        # set the top axis in years
        # set default values for now
        ax.margins(y=0.2)
        ax.set_ylim(-7, 7)
        # import pdb; pdb.set_trace()
        # annotate the points on the horizontal line
        for e, event in events_slice.iterrows():
            level = event['level']
            d = dt.strptime(event['start'], "%Y-%m-%d")
            label = event['label']
            colour = event['colour']
            ax.annotate(
                label,
                xy=(d,
                    level),
                xytext=(-3, np.sign(level)*3),
                verticalalignment="bottom" if level > 0 else "top",
                textcoords="offset points",
                arrowprops=dict(
                    arrowstyle="-",
                    color=colour,
                    linewidth=0.8),
                bbox=dict(
                     boxstyle='square',
                     pad=0,
                     lw=0,
                     fc=(1, 1, 1, 0.7)
                 )
            )
        ax.yaxis.set_visible(False)
        ax.spines[["left", "top", "right"]].set_visible(False)

        ax.xaxis.set(
            major_locator=mdates.YearLocator(),
            major_formatter=mdates.DateFormatter("%Y"))
        ax.grid(False)
    plt.show()
