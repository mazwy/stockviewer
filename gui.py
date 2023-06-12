import tkinter as tk
from tkinter import ttk

class GUI:
    def __init__(self, master):
        self.master = master
        self.master.title("Stock Prices")

        # Add a label
        self.label = tk.Label(self.master, text="Enter stock symbol:")
        self.label.pack()

        # Add an entry box
        self.entry = tk.Entry(self.master)
        self.entry.pack()

        # Add a dropdown menu for time range
        self.time_range_label = tk.Label(self.master, text="Select time range:")
        self.time_range_label.pack()

        self.time_range_var = tk.StringVar()
        self.time_range_dropdown = ttk.Combobox(self.master, textvariable=self.time_range_var, state="readonly")
        self.time_range_dropdown["values"] = ["1 month", "3 months", "6 months", "1 year"]
        self.time_range_dropdown.current(0)
        self.time_range_dropdown.pack()

        # Add a canvas for the chart
        self.chart_canvas = tk.Canvas(self.master, width=600, height=400)
        self.chart_canvas.pack()

        # Add a scrollbar for the chart
        self.chart_scrollbar = tk.Scrollbar(self.master, orient="horizontal", command=self.chart_canvas.xview)
        self.chart_scrollbar.pack(side="bottom", fill="x")
        self.chart_canvas.configure(xscrollcommand=self.chart_scrollbar.set)

        # Add a frame for the chart
        self.chart_frame = tk.Frame(self.chart_canvas)
        self.chart_canvas.create_window((0, 0), window=self.chart_frame, anchor="nw")

        # Add a button to get the prices
        self.get_price_button = tk.Button(self.master, text="Get Prices")
        self.get_price_button.pack()