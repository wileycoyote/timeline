import matplotlib.pyplot as plt
import sqlite3
import pandas as pd
import pprint as pp

start_year = 1500
end_year = 1526
range_units = 54


def get_data():
    conn = sqlite3.connect('database/timelines.db')
    query = """SELECT requested_order, timelines.timeline, label, start,end,
            line_type
            FROM timelines, meta
            WHERE timelines.timeline=meta.timeline;"""

    df = pd.read_sql_query(query, conn)
    return df


def get_date_frame(df, s, e):
    # sort by values so requested order needs to be in place here somewhere
    # only the requested range of rows needed as well
    timelines = df['timeline'].unique()
    for timeline in timelines:
        df.query('timeline=="' + timeline + '"')
    return "<TOKEN RETURN>"


def run_app():
    # this initialises the data
    df = get_data()
    # this navigates the dates
    timelines = get_date_frame(df, start_year, end_year)
    pp.pprint(timelines)
    return

    # to allow for distribution of horizontal timelines, this
    with plt.style.context('Solarize_Light2'):
        fig, ax = plt.subplots(figsize=(20, 14), layout="constrained")
        ax.set(title="Timelines for 1300 to 1600")
        #
        # set the top axis in years
        # set default values for now
        years = [str(x) for x in range(start_year, end_year, 1)]
        posn = [x for x in range(2, range_units, 2)]
        # Remove the y-axis and some spines.
        ax.yaxis.set_visible(False)
        ax.spines[["bottom", "right"]].set_visible(False)
        ax.invert_yaxis()
        ax.xaxis.tick_top()
        ax.set_xticks(posn, years)
        ax.margins(y=0.2)

        # Work through the queue
    plt.show()
