import matplotlib.pyplot as plt


start_year = 1500
end_year = 1526
range_units = 54


def get_data():
    temp_rows = []
    temp_rows.append({
        "group": "External Events",
        "event": "One Hundred Years War",
        "start": 1504,
        "duration": 4,
        "color": "C0",
        "row": 1
    })
    temp_rows.append({
        "group": "Italian Wars",
        "task": "First War",
        "start": 1507,
        "duration": 5,
        "color": "C1",
        "row": 2
    })
    return temp_rows


def run_app():
    # to allow for distribution of horizontal timelines, this
    fig, ax = plt.subplots(figsize=(20, 14), layout="constrained")
    ax.set(title="Timelines for 1300 to 1600")
    ax.axhline(0.5, c="black")
    ax.axhline(0.75, c="yellow")
    ax.axhline(1, c="red")
    ax.axhline(2, c="blue")
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
    plt.show()
