from datetime import datetime
from dash_calendar_timeline import DashCalendarTimeline
from dash import Dash, html

now = datetime.now()


# Helper to convert datetime to UNIX timestamp in milliseconds
def to_unix_ms(x):
    return int(x.timestamp() * 1000)


"""
Start: 2010
End: 2025

P1 2011 -> 2014
P2 2012 -> 2017
P3 2016 -> 2030
"""


def to_year_ms(x):
    s = "01/01/%s" % x
    dt = datetime.strptime(s, "%d/%m/%Y")
    return to_unix_ms(dt)


groups = [
    {"id": 1, "title": "group 1"},
    {"id": 2, "title": "group 2"}
]

items = [
    {
        "id": 1,
        "group": 1,
        "title": "item 1",
        "start_time": to_year_ms(2011),
        "end_time": to_year_ms(2014)
    },
    {
        "id": 2,
        "group": 2,
        "title": "item 2",
        "start_time": to_year_ms(2012),
        "end_time": to_year_ms(2017)
    },
    {
        "id": 3,
        "group": 1,
        "title": "item 3",
        "start_time": to_year_ms(2016),
        "end_time": to_year_ms(2025)
    }
]


def run_app():
    app = Dash(
        __name__,
        meta_tags=[
            {
                "name": "viewport",
                "content": "width=device-width, initial-scale=1.0"
            }
        ]
    )

    app.layout = html.Div(
        [
            DashCalendarTimeline(
                groups=groups,
                items=items,
                defaultTimeStart=to_year_ms("2012"),
                defaultTimeEnd=to_year_ms("2020"),
                dateHeaderUnit="year"
            )
        ]
    )
    app.run(debug=True)
