import matplotlib.pyplot as plt
import pandas as pd
import pprint as pp
from db.database import engine
from sqlalchemy import select
from db.models import TimelineGroup, Timeline


def_start_frame = 1500
def_end_frame = 1526
range_units = 54

conn = None


def get_data():

    stmt = select(TimelineGroup).order_by("order")
    # set up the dataframe for timeline groups

    t_df = pd.read_sql_query(
        stmt,
        con=engine,
        index_col='id'
    )
    # set up the dataframe for timelines
    stmt = select(Timeline, TimelineGroup.label.label("timeline")).where(
        TimelineGroup.id == Timeline.parent)
    e_df = pd.read_sql_query(
        stmt,
        con=engine,
        index_col='start'
    )
    return t_df, e_df


def get_timelines_slice(df, s, e):
    # get all the events columns that intersect our time-slice
    q = f"start > '{s}' and start <= '{e}'"
    slice_df = df.query(q)
    return slice_df


def run_app():
    # this initialises the data
    # import pdb; pdb.set_trace()
    t_df, e_df = get_data()
    # this navigates the dates
    events_slice = get_timelines_slice(e_df, def_start_frame, def_end_frame)
    timeline_names = events_slice['timeline'].unique()

    # to allow for distribution of horizontal timelines, this
    with plt.style.context('Solarize_Light2'):
        fig, ax = plt.subplots(figsize=(20, 14), layout="constrained")
        ax.set(title="Timelines for 1300 to 1600")
        #
        # set the top axis in years
        # set default values for now
        years = [str(x) for x in range(def_start_frame, def_end_frame, 1)]
        posn = [x for x in range(2, range_units, 2)]
        # Remove the y-axis and some spines.
        ax.yaxis.set_visible(False)
        ax.spines[["bottom", "right"]].set_visible(False)
        ax.invert_yaxis()
        ax.xaxis.tick_top()
        ax.set_xticks(posn, years)
        ax.margins(y=0.2)

        # do the timelines
        for t in timeline_names:
            print(t)
            # get the timeline display data
            timeline_data = t_df.query(f"label  == '{t}'")
            pp.pprint(timeline_data)
            # get the associated events data
            events = events_slice.query(f"timeline == '{t}'")
            pp.pprint(events)
            pp.pprint(timeline_data)
            import pdb; pdb.set_trace()
            if timeline_data['line_type'].item() == 'continuous':
                points = events.index.values
                plt.plot(1, points, marker='o', linestyle='-')
                for label in events['label']:
                    # need to set up dates as DateTime
                    plt.annotate(
                        f'{label}',
                        (1, points),
                        textcoords="offset points",
                        xytext=(0, 10),
                        ha='center')
    plt.show()
