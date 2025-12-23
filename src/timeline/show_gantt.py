# Importing the matplotlib.pyplot
import matplotlib.pyplot as plt


def run_app():
    # Declaring a figure "gnt"
    fig, gnt = plt.subplots()

    # Setting Y-axis limits
    gnt.set_ylim(0, 50)

    # Setting X-axis limits
    gnt.set_xlim(0, 160)

    # Setting labels for x-axis and y-axis
    gnt.set_ylabel('Processor')
    gnt.spines[["bottom", "right"]].set_visible(False)
    gnt.invert_yaxis()
    gnt.xaxis.tick_top()
    gnt.tick_params(top=True, labeltop=True, bottom=False, labelbottom=False)
    gnt.set_xlabel('seconds since start')
    gnt.xaxis.set_label_position('top')
    gnt.xaxis.set_ticks_position('top')
    # Setting ticks on y-axis
    gnt.set_yticks([15, 25, 35])
    # Labelling tickes of y-axis
    gnt.set_yticklabels(['Help', 'Two', 'Three'])

    # Setting graph attribute
    gnt.grid(True)

    # Declaring a bar in schedule
    gnt.broken_barh([(40, 50)], (30, 9), facecolors=('tab:orange'))

    # Declaring multiple bars in at same level and same width
    gnt.broken_barh([(110, 10),
                    (150, 10)],
                    (10, 9),
                    facecolors='tab:blue')

    gnt.broken_barh([(10, 50), (100, 20), (130, 10)],
                    (20, 9),
                    facecolors=('tab:red'))

    plt.show()
