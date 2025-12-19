import matplotlib.pyplot as plt


start_year = 1500
end_year = 1526
range_units = 54


def run_app():
    fig, ax = plt.subplots(figsize=(16.8, 4), layout="constrained")
    ax.set(title="Timelines for 1300 to 1600")
    # set default values for now
    years = [str(x) for x in range(start_year, end_year, 1)]
    posn = [x for x in range(2, range_units, 2)]
    # Remove the y-axis and some spines.
    ax.yaxis.set_visible(False)
    ax.spines[["left", "top", "right"]].set_visible(False)
    ax.invert_yaxis()
    ax.xaxis.tick_top()
    ax.margins(y=0.1)
    plt.xticks(posn, years)

    plt.show()
