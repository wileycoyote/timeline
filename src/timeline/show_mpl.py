import matplotlib.pyplot as plt


start_year = 1500
end_year = 1526
range_units = 54


def get_data():
    temp_rows = []
    temp_rows.append({
        "group": "External Events",
        "task": "One Hundred Years War",
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
    fig, ax = plt.subplots(figsize=(16.8, 4), layout="constrained")
    rows = get_data()
    for row in rows:
        plt.barh(
            y=row['row'],
            height=0.4,
            width=row['duration'],
            left=row['start'] + 1,
            color=row['color'],
            alpha=0.4
        )
    ax.set(title="Timelines for 1300 to 1600")
    # set default values for now
    years = [str(x) for x in range(start_year, end_year, 1)]
    posn = [x for x in range(2, range_units, 2)]
    # Remove the y-axis and some spines.
    # ax.yaxis.set_visible(False)
    ax.spines[["bottom", "right"]].set_visible(False)
    ax.invert_yaxis()
    # ax.xaxis.tick_top()
    ax.set_xticks(posn, years)
    ax.margins(y=0.2)
    plt.show()
