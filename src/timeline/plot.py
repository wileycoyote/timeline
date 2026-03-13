import matplotlib.pyplot as plt

import pandas as pd
import pprint as pp
from db.database import engine
from sqlalchemy import select
from db.models import TimelineGroup, Timeline
from datetime import datetime as dt
import pandas_log
import numpy as np
import matplotlib.dates as mdates

def_start_frame = dt.fromisoformat("1500-01-01")
def_end_frame = dt.fromisoformat("1526-01-01")
range_units = 54

conn = None


def get_data():

    stmt = select(TimelineGroup)
    # set up the dataframe for timeline groups
    t_df = pd.read_sql_query(
        stmt,
        con=engine,
        index_col='id'
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
    events_slice = get_timelines_slice(e_df, def_start_frame, def_end_frame)
    dates = events_slice['start']
    # to allow for distribution of horizontal timelines, this
    with plt.style.context('Solarize_Light2'):
        fig, ax = plt.subplots(figsize=(20, 14), layout="constrained")
        ax.set(title="Timelines for 1300 to 1600")
        #
        # The baseline.
        # ax.axhline(0, c="black")
        #
        # The markers on the baseline.
        import pdb; pdb.set_trace()
        ax.plot(dates.Date, np.zeros_like(dates), "ko", mfc="white")
        #
        # set the top axis in years
        # set default values for now
        year_start = def_start_frame.year
        year_end = def_end_frame.year
        years = [str(x) for x in range(year_start, year_end, 1)]
        posn = [x for x in range(2, range_units, 2)]
        # Remove the y-axis and some spines.
        ax.yaxis.set_visible(False)
        ax.spines[["left", "top", "bottom", "right"]].set_visible(False)
        ax.spines[["bottom"]].set_position(("axes", 0.5))
        # ax.xaxis.tick_top()
        ax.set_xticks(posn, years)
        ax.margins(y=0.2)
        ax.set_ylim(-7, 7)
        # import pdb; pdb.set_trace()
        # annotate the points on the horizontal line
        for e, event in events_slice.iterrows():
            pp.pprint(event)
            level = event['level']
            dt = event['start']
            label = event['label']
            colour = event['colour']
            plt.annotate(
                label,
                xy=(dt,
                    0.1 if level > 0 else -0.1),
                xytext=(dt, level),
                textcoords="offset points",
                arrowprops=dict(
                    arrowstyle="-",
                    color=colour,
                    linewidth=0.8),
                ha='center',
            )
        ax.xaxis.set(
            major_locator=mdates.YearLocator(),
            major_formatter=mdates.DateFormatter("%Y"))
    plt.show()
