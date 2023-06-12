import threading
import tkinter as tk
from tkinter import messagebox
import matplotlib.dates as mdates
from stock import Stock
from chart import Chart


class StockGui(tk.Frame):
    """
    A GUI for displaying historical and real-time stock prices.

    Attributes:
        master (tk.Tk): The root window of the GUI.
        symbol_label (tk.Label): The label for the stock symbol entry field.
        entry (tk.Entry): The entry field for the stock symbol.
        time_range_label (tk.Label): The label for the time range dropdown menu.
        time_range_var (tk.StringVar): The variable for the selected time range.
        time_range_menu (tk.OptionMenu): The dropdown menu for selecting the time range.
        get_price_button (tk.Button): The button for getting historical prices.
        chart_frame (tk.Frame): The frame for displaying the chart.
        export_chart_button (tk.Button): The button for exporting the chart.
    """

    def __init__(self, master=None):
        """
        Initializes the StockGui object.

        Args:
            master (tk.Tk): The root window of the GUI.
        """
        if master is None:
            master = tk.Tk()
        super().__init__(master)
        self.master = master
        self.master.title("Stock Price Chart")
        self.pack()
        self.create_widgets()

        # windows size = 3/4 of screen size
        self.master.geometry("%dx%d" % (self.master.winfo_screenwidth() * 3 / 4, self.master.winfo_screenheight() * 3 / 4))

    def create_widgets(self):
        """
        Creates the widgets for the GUI.
        """
        # Create the stock symbol label and entry field
        self.symbol_label = tk.Label(self, text="Stock Symbol:")
        self.symbol_label.pack(side="top", padx=10, pady=10)
        self.entry = tk.Entry(self)
        self.entry.pack(side="top", padx=10, pady=10)

        # Create the time range label and dropdown menu
        self.time_range_label = tk.Label(self, text="Time Range:")
        self.time_range_label.pack(side="top", padx=10, pady=10)
        self.time_range_var = tk.StringVar(self)
        self.time_range_var.set("1 month")
        self.time_range_menu = tk.OptionMenu(self, self.time_range_var, "1 month", "3 months", "6 months", "1 year")
        self.time_range_menu.pack(side="top", padx=10, pady=10)

        # Create the get price button
        self.get_price_button = tk.Button(self, text="Get Historical Prices", command=self.get_price)
        self.get_price_button.pack(side="top", padx=10, pady=10)

        # Create the chart frame
        self.chart_frame = tk.Frame(self)
        self.chart_frame.pack()

        # Create the export buttons
        self.export_chart_button = tk.Button(self, text="Export Chart")
        self.export_chart_button.pack(pady=10)

    def get_price(self):
        """
        Gets the historical prices for the selected stock symbol and time range.
        """
        symbol = self.entry.get()
        time_range = self.time_range_var.get()
        stock_obj = Stock(symbol)
        prices = stock_obj.get_price(time_range)
        if prices is None:
            messagebox.showerror("Error", "Invalid stock symbol or API issue")
            return

        # Clear previous chart from chart_frame
        for widget in self.chart_frame.winfo_children():
            widget.destroy()

        chart_obj = Chart(symbol, prices)
        fig, ax, dates, prices = chart_obj.create_chart(self.chart_frame)
        ax.set_xlabel("Days")
        ax.set_ylabel("Price")
        ax.set_title(f"Historical Prices")
        ax.legend()

        # Add the plot to the chart with a specified color
        ax.plot(dates, prices, label=symbol, color="blue")

        # Format the x-axis labels to show proper dates
        ax.xaxis.set_major_formatter(mdates.DateFormatter('%Y-%m-%d'))
        ax.xaxis.set_major_locator(mdates.DayLocator(interval=7))
        fig.autofmt_xdate(rotation=45)

        # Create a new thread to run the get_realtime_price() method
        realtime_price_label = tk.Label(self, text="")
        realtime_price_label.pack()
        t = threading.Thread(target=chart_obj.get_realtime_price, args=(realtime_price_label,))
        t.daemon = True
        t.start()

        # Update export button command
        self.export_chart_button.config(command=lambda: chart_obj.export_chart())

if __name__ == "__main__":
    root = tk.Tk()
    app = StockGui(master=root)
    app.mainloop()