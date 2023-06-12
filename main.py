import tkinter as tk
from gui import GUI
from chart import Chart
from data import Data

# Create instance
win = tk.Tk()

# Create instances of the classes
gui = GUI(win)
chart = Chart(gui.chart_canvas)
data = Data()

# Add a button to get the prices
def get_price():
    symbol = gui.entry.get()
    time_range = gui.time_range_var.get()
    data.get_data(symbol, time_range)
    chart.plot_data(data.data)

gui.get_price_button.config(command=get_price)

# Start the GUI
win.mainloop()