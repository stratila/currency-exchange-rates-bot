import io
import numpy as np
import matplotlib.dates as mdates
from matplotlib.backends.backend_agg import FigureCanvasAgg as FigureCanvas
from matplotlib.figure import Figure


def exchange_rate_text(rates):
    text = 'Exchange rates 💸\n'
    for curr, val in rates.items():
        text += '{} {:.2f}\n'.format(curr, val)
    return text


def graph_chart(rates, base, curr):
    date_value_data = [(value[curr], date) for date, value in rates.items()]
    data = np.array(date_value_data, dtype=[('value', 'f4'), ('date', 'datetime64[s]')])
    fig = Figure()
    ax = fig.add_subplot(1, 1, 1)
    ax.plot('date', 'value', data=np.sort(data, order='date'))
    ax.set_ylabel(curr, fontsize=10)
    ax.title.set_text('Base: {}'.format(base))

    days = mdates.DayLocator()  # every day
    years_fmt = mdates.DateFormatter('%Y-%m-%d')

    ax.xaxis.set_major_locator(days)
    ax.xaxis.set_major_formatter(years_fmt)
    ax.grid(True)
    fig.autofmt_xdate()

    output = io.BytesIO()
    FigureCanvas(fig).print_png(output)
    return output.getvalue()



