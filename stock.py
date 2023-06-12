import json
import requests
import datetime
import dotenv
import os


dotenv.load_dotenv()
KEY = os.getenv("API_KEY")

class Stock:
    """
    A class for retrieving historical and real-time stock prices.

    Attributes:
        symbol (str): The stock symbol.
    """

    def __init__(self, symbol):
        """
        Initializes the Stock object.

        Args:
            symbol (str): The stock symbol.
        """
        self.symbol = symbol

    def get_price(self, time_range):
        """
        Retrieves the historical prices for the selected stock symbol and time range.

        Args:
            time_range (str): The selected time range.

        Returns:
            list: A list of tuples containing the timestamp and closing price for each day.
        """
        if time_range == "1 month":
            days = 30
        elif time_range == "3 months":
            days = 90
        elif time_range == "6 months":
            days = 180
        elif time_range == "1 year":
            days = 365
        else:
            days = 30  # Default to 30 days if time_range is not valid

        end_date = datetime.datetime.now().strftime("%Y-%m-%d")
        start_date = (datetime.datetime.strptime(end_date, "%Y-%m-%d") - datetime.timedelta(days=days)).strftime("%Y-%m-%d")
        try:
            response = requests.get(f"https://api.polygon.io/v2/aggs/ticker/{self.symbol}/range/1/day/{start_date}/{end_date}?adjusted=true&sort=asc&limit=120&apiKey={KEY}")
            if response.status_code != 200:
                return None
            data = response.json()
            if "results" not in data:
                return None
            results = data["results"]
            if len(results) == 0:
                return None
            prices = [(result["t"], result["c"]) for result in results]
            return prices
        except:
            return None

    def on_message(self, ws, message, label):
        """
        Callback function for handling real-time stock price updates.

        Args:
            ws (websocket.WebSocketApp): The WebSocketApp object.
            message (str): The message received from the WebSocket.
            label (tk.Label): The label for displaying the real-time price.
        """
        data = json.loads(message)
        if "ev" in data and data["ev"] == "T":
            price = data["p"]
            label.config(text=f"Realtime Price: {price}")