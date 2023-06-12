import matplotlib.pyplot as plt
import mplcursors

class Chart:
    def __init__(self, canvas):
        self.canvas = canvas

    def plot_data(self, data):
        # Clear the chart
        self.canvas.delete("all")

        # Plot the data
        fig, ax = plt.subplots()
        ax.plot(data["dates"], data["prices"])
        ax.set_xlabel("Date")
        ax.set_ylabel("Price")
        ax.set_title("Stock Prices")

        # Add cursor hover functionality
        mplcursors.cursor(ax)

        # Display the chart on the canvas
        fig_canvas = FigureCanvasTkAgg(fig, master=self.canvas)
        fig_canvas.draw()
        fig_canvas.get_tk_widget().pack(side="top", fill="both", expand=1)