# yohjrjGDzw16Mt80pajyhHQBr4eAWOD2
import tkinter as tk
from tkinter import ttk
import requests
import datetime
import matplotlib.pyplot as plt
import csv
import mplcursors
import websocket
import json

# Create instance
win = tk.Tk()

# Add a title
win.title("Stock Prices")

# Add a label
label = tk.Label(win, text="Enter stock symbol:")
label.pack()

# Add an entry box
entry = tk.Entry(win)
entry.pack()

# Add a dropdown menu for time range
time_range_label = tk.Label(win, text="Select time range:")
time_range_label.pack()

time_range_var = tk.StringVar()
time_range_dropdown = ttk.Combobox(win, textvariable=time_range_var, state="readonly")
time_range_dropdown["values"] = ["1 month", "3 months", "6 months", "1 year"]
time_range_dropdown.current(0)
time_range_dropdown.pack()

# Add a canvas for the chart
chart_canvas = tk.Canvas(win, width=600, height=400)
chart_canvas.pack()

# Add a scrollbar for the chart
chart_scrollbar = tk.Scrollbar(win, orient="horizontal", command=chart_canvas.xview)
chart_scrollbar.pack(side="bottom", fill="x")
chart_canvas.configure(xscrollcommand=chart_scrollbar.set)

# Add a frame for the chart
chart_frame = tk.Frame(chart_canvas)
chart_canvas.create_window((0, 0), window=chart_frame, anchor="nw")

# Add a button to get the prices
def get_price():
    symbol = entry.get()
    time_range = time_range_var.get()
    if time_range == "1 month":
        days = 30
    elif time_range == "3 months":
        days = 90
    elif time_range == "6 months":
        days = 180
    elif time_range == "1 year":
        days = 365
    end_date = "2023-01-09"
    start_date = (datetime.datetime.strptime(end_date, "%Y-%m-%d") - datetime.timedelta(days=days)).strftime("%Y-%m-%d")
    response = requests.get(f"https://api.polygon.io/v2/aggs/ticker/{symbol}/range/1/day/{start_date}/{end_date}?adjusted=true&sort=asc&limit=120&apiKey=yohjrjGDzw16Mt80pajyhHQBr4eAWOD2")
    if response.status_code != 200:
        price_label.config(text="Error: Invalid stock symbol or API issue")
        return
    data = response.json()
    if "results" not in data:
        price_label.config(text="Error: Invalid stock symbol or API issue")
        return
    results = data["results"]
    prices = [result["c"] for result in results]
    price_label.config(text=f"Prices: {prices}")
    plt.plot(prices, label=symbol)
    plt.xlabel("Days")
    plt.ylabel("Price")
    plt.title(f"Historical Prices")
    plt.legend()
    plt.clf()
    plt.show()
    chart_image = tk.PhotoImage(file="chart.png")
    chart_canvas.create_image(0, 0, anchor="nw", image=chart_image)
    chart_canvas.configure(scrollregion=chart_canvas.bbox("all"))
    cursor = mplcursors.cursor(hover=True)
    cursor.connect("add", lambda sel: sel.annotation.set_text(f"Price: {sel.target[1]:.2f}"))

    # Connect to WebSocket to get real-time price updates
    def on_message(ws, message):
        data = json.loads(message)
        price = data["p"]
        price_label.config(text=f"Current price: {price}")

    ws = websocket.WebSocketApp(f"wss://socket.polygon.io/stocks/trades/{symbol}/last?apiKey=yohjrjGDzw16Mt80pajyhHQBr4eAWOD2",
                                on_message=on_message)
    ws.run_forever()

button = tk.Button(win, text="Get Prices", command=get_price)
button.pack()

# Add a label to display the prices
price_label = tk.Label(win, text="")
price_label.pack()

# Add a button to save the prices
def save_prices():
    symbol = entry.get()
    time_range = time_range_var.get()
    if time_range == "1 month":
        days = 30
    elif time_range == "3 months":
        days = 90
    elif time_range == "6 months":
        days = 180
    elif time_range == "1 year":
        days = 365
    end_date = "2023-01-09"
    start_date = (datetime.datetime.strptime(end_date, "%Y-%m-%d") - datetime.timedelta(days=days)).strftime("%Y-%m-%d")
    response = requests.get(f"https://api.polygon.io/v2/aggs/ticker/{symbol}/range/1/day/{start_date}/{end_date}?adjusted=true&sort=asc&limit=120&apiKey=yohjrjGDzw16Mt80pajyhHQBr4eAWOD2")
    if response.status_code != 200:
        price_label.config(text="Error: Invalid stock symbol or API issue")
        return
    data = response.json()
    if "results" not in data:
        price_label.config(text="Error: Invalid stock symbol or API issue")
        return
    results = data["results"]
    with open(f"{symbol}_prices.csv", "w", newline="") as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(["Date", "Price"])
        for result in results:
            writer.writerow([result["t"], result["c"]])

save_button = tk.Button(win, text="Save Prices", command=save_prices)
save_button.pack()

# Add a button to get financial information
def get_financial_info():
    symbol = entry.get()
    response = requests.get(f"https://api.polygon.io/v1/meta/symbols/{symbol}/company?apiKey=yohjrjGDzw16Mt80pajyhHQBr4eAWOD2")
    if response.status_code != 200:
        financial_info_label.config(text="Error: Invalid stock symbol or API issue")
        return
    data = response.json()
    pe_ratio = data["peRatio"]
    market_cap = data["marketcap"]
    dividend_yield = data["dividendYield"]
    financial_info_label.config(text=f"P/E Ratio: {pe_ratio}\nMarket Cap: {market_cap}\nDividend Yield: {dividend_yield}")

    # Get earnings data
    earnings_response = requests.get(f"https://api.polygon.io/v2/reference/financials/{symbol}?type=TTM&apiKey=yohjrjGDzw16Mt80pajyhHQBr4eAWOD2")
    if earnings_response.status_code == 200:
        earnings_data = earnings_response.json()
        earnings = earnings_data["results"]
        earnings_label.config(text=f"Earnings: {earnings}")
    else:
        earnings_label.config(text="Error: Invalid stock symbol or API issue")

    # Get dividend data
    dividend_response = requests.get(f"https://api.polygon.io/v2/reference/dividends/{symbol}?apiKey=yohjrjGDzw16Mt80pajyhHQBr4eAWOD2")
    if dividend_response.status_code == 200:
        dividend_data = dividend_response.json()
        dividends = dividend_data["results"]
        dividends_label.config(text=f"Dividends: {dividends}")
    else:
        dividends_label.config(text="Error: Invalid stock symbol or API issue")

financial_info_button = tk.Button(win, text="Get Financial Info", command=get_financial_info)
financial_info_button.pack()

# Add a label to display the financial information
financial_info_label = tk.Label(win, text="")
financial_info_label.pack()

# Add a label to display the earnings data
earnings_label = tk.Label(win, text="")
earnings_label.pack()

# Add a label to display the dividend data
dividends_label = tk.Label(win, text="")
dividends_label.pack()

# Run the event loop
win.mainloop()