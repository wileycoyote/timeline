import matplotlib.pyplot as plt
import datetime


def createtimeline(keydates, events):
    """
    Creates a timeline using horizontal bars
    with vertical lines to indicate key dates.

Parameters:
- key_dates: list of str
    A list of key dates in 'YYYY-MM-DD' format.
- events: list of str
    A list of events corresponding to the key dates.

Returns:
- None
    """
    # Convert key_dates to a format that matplotlib can understand
    dates = [datetime.datetime.strptime(date, '%Y-%m-%d')
             for date in keydates]

    # Create a figure and axis
    fig, ax = plt.subplots(figsize=(10, 5))

    # Create horizontal bars for each event
    for i, (date, event) in enumerate(zip(dates, events)):
        ax.barh(i, 1,
                left=date,
                height=0.4,
                color='skyblue',
                edgecolor='black')
        ax.text(date, i, ' ' + event, va='center', ha='left')

    # Add vertical lines for each key date
    for date in dates:
        ax.axvline(x=date, color='gray', linestyle='--')

    # Formatting the x-axis to show dates properly
    ax.xaxis_date()
    plt.xticks(rotation=45)
    ax.set_yticks(range(len(events)))
    ax.set_yticklabels(events)

    # Set labels and title
    plt.xlabel('Date')
    plt.title('Timeline of Key Events')

    # Show the plot
    plt.tight_layout()
    plt.show()


keydates = ['2023-01-01', '2023-02-15', '2023-03-30', '2023-04-20']
events = ['New Year', "Valentine's Day", 'Spring Equinox', 'Earth Day']
createtimeline(keydates, events)
