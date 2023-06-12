import datetime
from tkinter import filedialog
from matplotlib import pyplot as plt
import matplotlib.dates as mdates
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import websocket
import json


class Chart:
    """
    A class for creating and exporting a historical price chart for a stock symbol.

    Attributes:
        symbol (str): The stock symbol.
        prices (list): A list of tuples containing the timestamp and closing price for each day.
    """

    def __init__(self, symbol, prices):
        """
        Initializes the Chart object.

        Args:
            symbol (str): The stock symbol.
            prices (list): A list of tuples containing the timestamp and closing price for each day.
        """
        self.symbol = symbol
        self.prices = prices

    def create_chart(self, frame):
        """
        Creates a historical price chart for the selected stock symbol and time range.

        Args:
            frame (tk.Frame): The frame to display the chart in.

        Returns:
            tuple: A tuple containing the figure, axis, dates, and prices.
        """
        fig, ax = plt.subplots()
        canvas = FigureCanvasTkAgg(fig, master=frame)
        canvas.get_tk_widget().pack(side="top", fill="both", expand=True)

        # Convert the dates to datetime objects and the prices to floats
        dates = [datetime.datetime.fromtimestamp(int(price[0])/1000) for price in self.prices]
        prices = [float(price[1]) for price in self.prices]

        # Plot the prices as a line chart
        ax.plot(dates, prices, label="Historical Prices")

        # Set the x-axis label, y-axis label, and chart title
        ax.set_xlabel("Date")
        ax.set_ylabel("Price")
        ax.set_title(f"{self.symbol} Historical Prices")
        ax.legend()

        # Format the x-axis labels to show proper dates
        ax.xaxis.set_major_formatter(mdates.DateFormatter('%Y-%m-%d'))
        ax.xaxis.set_major_locator(mdates.DayLocator(interval=7))
        fig.autofmt_xdate(rotation=45)

        return fig, ax, dates, prices

    def get_realtime_price(self, realtime_price_label):
        """
        Retrieves the real-time price for the selected stock symbol and updates the label.

        Args:
            realtime_price_label (tk.Label): The label for displaying the real-time price.
        """
        def on_message(ws, message):
            data = json.loads(message)
            price = data["p"]
            realtime_price_label.config(text=f"Real-time Price: {price}")

        ws = websocket.WebSocketApp(f"wss://socket.polygon.io/stocks/trades/{self.symbol}/last?apiKey=yohjrjGDzw16Mt80pajyhHQBr4eAWOD2",
                                    on_message=on_message)
        ws.run_forever()

    def export_chart(self):
        """
        Exports the chart to a PNG file.
        """
        try:
            file_path = filedialog.asksaveasfilename(defaultextension=".png")
            if file_path:
                plt.savefig(file_path)
                return True
        except:
            pass
        return False