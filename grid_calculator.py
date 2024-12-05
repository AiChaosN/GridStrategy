import random
import matplotlib.pyplot as plt


class GridCalculator:
    def __init__(self, config, prices):
        # 初始参数
        self.config = config
        self.prices = prices
        self.begin_price = prices[0]
        self.initial_investment = config["investment"]
        self.investments = []

        self.grid = []  # 网格价格
        self.strategy = [] # 交易策略 0 买入 1 卖出
        self.Number_stocks = [] # 每个网格的股票数量

    def generate_grid(self):
        # 生成网格
        if self.config["mode"] == 'arithmetic':
            # 等差网格
            step = (self.config["upper_bound"] - self.config["lower_bound"]) / (self.config["num_grids"] - 1)
            grid = [self.config["lower_bound"] + i * step for i in range(self.config["num_grids"])]
        elif self.config["mode"] == 'geometric':
            # 等比网格
            ratio = (self.config["upper_bound"] / self.config["lower_bound"]) ** (1 / (self.config["num_grids"] - 1))
            grid = [self.config["lower_bound"] * (ratio ** i) for i in range(self.config["num_grids"])]
        self.grid = grid
        # 生成交易策略 生成每个网格可卖股票状态 (0没有股票 1有股票)
        for i in range(self.config["num_grids"]):
            if self.grid[i] <= self.begin_price:
                self.strategy.append(0)
                self.Number_stocks.append(0)
            else:
                self.strategy.append(1)
                self.Number_stocks.append(1)

        print("网格价格", self.grid)
        print("交易策略", self.strategy)
        print("每个网格的股票数量", self.Number_stocks)

        # 初始买入
        nums = sum(self.Number_stocks)
        self.config["investment"] -= self.begin_price * nums
        print("初始买入", "股票数量", nums, "现金资产", self.config["investment"])

    def run(self):
        for i in range(1, len(self.prices)):
            # 当前价格 和 之前价格之间的所有网格
            grid_indices = [index for index, grid_price in enumerate(self.grid) if (self.prices[i-1] <= grid_price <= self.prices[i]) or (self.prices[i] <= grid_price <= self.prices[i-1])]
            if(len(grid_indices) == 0):
                continue
            print("之前价格", self.prices[i-1], "当前价格", self.prices[i], "跨越区间价格:", grid_indices)
            for index in grid_indices:
                self.transaction(index)
         
    def transaction(self, index, price):
        if self.strategy[index] == 0:
            if self.strategy[index] == 1: return
            # 买入
            self.config['investment'] -= self.grid[index]
            self.Number_stocks[index] += 1
            print(f"买入价格: {self.grid[index]}, 股票数量: {self.Number_stocks[index]}, 现金资产: {self.config['investment']}")
            if price < self.grid[index]:
                self.strategy[index] = 1
                print("价格低于网格，之后可卖出")
        else:
            # 卖出
            self.config['investment'] += self.grid[index] * self.Number_stocks[index]
            self.Number_stocks[index] = 0
            print(f"卖出价格: {self.grid[index]}, 股票数量: {self.Number_stocks[index]}, 现金资产: {self.config['investment']}")
            if price > self.grid[index]:
                self.strategy[index] = 0
                print("价格超过网格，之后可买入")

        self.investments.append(self.config['investment'])   

    def conclusion(self):
        print("结束交易")
        print("现金资产", self.config["investment"] + self.prices[-1] * sum(self.Number_stocks))
        # self.investments.append(self.config["investment"] + self.prices[-1] * sum(self.Number_stocks))
        self.investments.append(self.config["investment"] )
        fig, axs = plt.subplots(3, 1, figsize=(8, 12))

        # 第一个图：价格走势
        axs[0].plot(self.prices, label="Price", color="blue", marker="o")
        axs[0].set_xlabel("Timestamp")
        axs[0].set_ylabel("Price")
        axs[0].set_title("Price Trend")
        axs[0].legend()
        axs[0].grid()

        # 第二个图：投资次数现金变化
        axs[1].plot(self.investments, label="Investments", color="green", marker="o")
        axs[1].set_xlabel("Timestamp")
        axs[1].set_ylabel("Investments")
        axs[1].set_title("Investments Over Time")
        axs[1].legend()
        axs[1].grid()

        # 第三个图：网格结束后股票数量
        axs[2].bar(range(len(self.Number_stocks)), self.Number_stocks, color="orange", label="Number of Stocks")
        axs[2].set_xlabel("Grid")
        axs[2].set_ylabel("Number of Stocks")
        axs[2].set_title("Number of Stocks in Each Grid")
        axs[2].legend()
        axs[2].grid(axis='y')

        # 调整布局并显示
        plt.tight_layout()
        plt.show()  

def generate_prices(length, min_value, max_value):
    """
    生成一个随机数列表，每个数字有一位小数，相邻两个数不同。

    :param length: 随机数列表的长度
    :param min_value: 随机数的最小值（含）
    :param max_value: 随机数的最大值（含）
    :return: 满足条件的随机数列表
    """
    if min_value >= max_value:
        raise ValueError("min_value must be less than max_value")

    prices = []
    prev_price = None

    while len(prices) < length:
        # 生成一个具有一位小数的随机数
        price = round(random.uniform(min_value, max_value), 1)
        
        # 确保当前价格与前一个价格不同
        if price != prev_price:
            prices.append(price)
            prev_price = price

    return prices


# 使用示例
if __name__ == "__main__":
    seed = 42
    random.seed(seed)
    prices = generate_prices(length=10, min_value=1.0, max_value=10.0)
    prices = [3.5] + prices
    print("prices:", prices)
    config = {
        "lower_bound": 1,
        "upper_bound": 10,
        "num_grids": 10,
        "leverage": 1,
        "investment": 100,
        "mode": "arithmetic"
    }
    grid_calc = GridCalculator(config, prices)
    grid_calc.generate_grid()

    print("开始交易")
    grid_calc.run()

    grid_calc.conclusion()
