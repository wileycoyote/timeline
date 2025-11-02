# Plotly
# https://plotly.com/python/gantt/
# https://plotly.com/python-api-reference/generated/plotly.express.timeline.html
# https://plotly.com/python/discrete-color/#color-sequences-in-plotly-express
import plotly.express as px
import pandas as pd
import math
from dash import Dash, dash_table

'''
see
https://stackoverflow.com/questions/67405363/transforming-string-containing-a-date-before-1600-to-datetime-object-in-pandas
for using julian date type things
'''


def conv(x):
    year, day, month = map(int, x.split("-"))
    return pd.Period(year=year, month=month, day=day, freq="M")


def run_app():
    source = pd.read_csv('data/data.csv')
    # import pprint
    import pdb; pdb.set_trace()
    source['start'] = pd.to_datetime(source['start'])
    # source['start'] = source['start'].apply(conv)
    source['end'] = pd.to_datetime(source['end'])
    # source['end'] = source['end'].apply(conv)
    print("YYYYYYYYYYYYYY")
    fig = px.timeline(
        # source.sort_values('start'),
        source,
        x_start="start",
        x_end="end",
        y="event",
        text="event",
        color_discrete_sequence=["red"])

    for idx, row in source.iterrows():
        periods = pd.date_range(row["start"], row["end"], freq='1D')
        center_pos = math.floor(len(periods) / 2)
        x_dates = periods[center_pos]
        print(x_dates)
        fig.add_annotation(
            {
                "x": x_dates,  # row["Finish"],
                "y": row["event"],
                "text": row["notes"],
                "align": "center",
                "showarrow": False,
            }
        )
#    fig.show()
    app = Dash()

    app.layout = dash_table.DataTable(
        style_data={
            'whiteSpace': 'normal',
            'height': 'auto',
            'lineHeight': '15px'
        },
        data=fig.to_dict(),
        columns=[{'id': c, 'name': c} for c in source.columns]
    )
    app.run(debug=True)
