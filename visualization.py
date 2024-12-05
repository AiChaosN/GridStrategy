import matplotlib.pyplot as plt

class GridVisualizer:
    def __init__(self, config):
        self.config = config

    def plot_trading_view(self, prices, timestamps, trades):
        plt.figure(figsize=(10, 6))
        plt.plot(timestamps, prices, label="Price")
        # 添加交易点
        for trade in trades:
            plt.scatter(trade[0], trade[1][1:1001], color="red" if trade[2] == "sell" else "green")
        plt.legend()
        plt.xlabel("Timestamp")
        plt.ylabel("Price")
        plt.title("Trading View")

    def plot_equity_curve(self, equity_curve, timestamps):
        plt.figure(figsize=(10, 6))
        plt.plot(timestamps, equity_curve, label="Equity Curve")
        plt.legend()
        plt.xlabel("Timestamp")
        plt.ylabel("Equity")
        plt.title("Equity Curve")

    def save_fig(self, filename):
        plt.savefig(filename)
        plt.close()
