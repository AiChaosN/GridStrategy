import random
import matplotlib.pyplot as plt


class GridStrategy:
    def __init__(self, config, prices):
        """
        初始化网格策略参数
        :param config: 网格策略的配置参数
        :param prices: 价格数据
        """
        self.upper_bound = config["upper_bound"]
        self.lower_bound = config["lower_bound"]
        self.num_grids = config["num_grids"]
        self.mode = config["mode"]
        self.investment = config["investment"]
        self.leverage = config["leverage"]
        self.prices = prices

        # 二级信息
        self.grid_prices = self.generate_grid()
        self.grid_stocks = [0 for _ in range(len(self.grid_prices))]
        self.strategy = [0 if price <= prices[0] else 1 for price in self.grid_prices]
        self.cash_balance = self.investment
        self.total_assets = []

        # 每网格购买的股票量
        grid_median_price = (self.upper_bound + self.lower_bound) / 2
        self.grid_stock_amount = (self.investment * self.leverage) / (grid_median_price * self.num_grids)

    def generate_grid(self):
        """
        生成网格价格
        :return: 网格价格列表
        """
        if self.mode == "arithmetic":
            step = (self.upper_bound - self.lower_bound) / (self.num_grids - 1)
            grid_prices = [self.lower_bound + i * step for i in range(self.num_grids)]
        elif self.mode == "geometric":
            ratio = (self.upper_bound / self.lower_bound) ** (1 / (self.num_grids - 1))
            grid_prices = [self.lower_bound * (ratio ** i) for i in range(self.num_grids)]
        else:
            raise ValueError("Invalid mode. Choose 'arithmetic' or 'geometric'.")
        return grid_prices

    def break_line(self, now_price, now_stock_nums):
        """
        计算爆仓线
        :param now_price: 当前价格
        :param now_stock_nums: 当前持仓股票总量
        :return: 爆仓价格
        """
        total_stock_nums = now_stock_nums + sum(self.grid_stocks)
        agv_hold_price = (
            (now_price * now_stock_nums + sum([price * stock_nums for price, stock_nums in zip(self.grid_prices, self.grid_stocks)]))
            / total_stock_nums
        )
        return (1 - (1 / self.leverage)) * agv_hold_price

    def execute_trade(self, index, current_price):
        """
        执行网格交易
        :param index: 当前网格的索引
        :param current_price: 当前价格
        """
        if self.strategy[index] == 0:
            # 买入逻辑
            cost = self.grid_prices[index] * self.grid_stock_amount
            if self.cash_balance >= cost:
                self.cash_balance -= cost
                self.grid_stocks[index] += self.grid_stock_amount
                self.strategy[index] = 1
        else:
            # 卖出逻辑
            revenue = self.grid_prices[index] * self.grid_stocks[index]
            self.cash_balance += revenue
            self.grid_stocks[index] = 0
            self.strategy[index] = 0

        # 更新总资产
        total_stocks_value = sum(stock * current_price for stock in self.grid_stocks)
        self.total_assets.append(self.cash_balance + total_stocks_value)
    
    def run_strategy(self):
        """
        执行网格策略
        """
        for i in range(1, len(self.prices)):
            previous_price, current_price = self.prices[i - 1], self.prices[i]
            for j, grid_price in enumerate(self.grid_prices):
                if previous_price <= grid_price <= current_price or current_price <= grid_price <= previous_price:
                    self.execute_trade(j, current_price)
    
    def plot_results(self):
        """
        绘制策略结果，包括价格趋势、总资产变化以及爆仓线
        """
        fig, axs = plt.subplots(2, 1, figsize=(10, 8))

        # 价格走势
        axs[0].plot(self.prices, label="Price", color="blue", marker="o")
        
        # 计算并绘制爆仓线
        now_stock_nums = sum(self.grid_stocks)
        break_price = self.break_line(self.prices[-1], now_stock_nums)
        axs[0].axhline(break_price, color="red", linestyle="--", label=f"Break Line: {break_price:.2f}")

        axs[0].set_title("Price Trend and Break Line")
        axs[0].set_xlabel("Time")
        axs[0].set_ylabel("Price")
        axs[0].legend()
        axs[0].grid()

        # 总资产变化
        axs[1].plot(self.total_assets, label="Total Assets", color="green", marker="o")
        axs[1].set_title("Total Asset Trend")
        axs[1].set_xlabel("Time")
        axs[1].set_ylabel("Assets")
        axs[1].legend()
        axs[1].grid()

        plt.tight_layout()
        plt.show()


def generate_prices(length, min_value, max_value):
    """
    生成一个随机数列表，每个数字有一位小数，相邻两个数不同
    """
    if min_value >= max_value:
        raise ValueError("min_value must be less than max_value")

    prices = []
    prev_price = None

    while len(prices) < length:
        price = round(random.uniform(min_value, max_value), 1)
        if price != prev_price:
            prices.append(price)
            prev_price = price

    return prices


# 使用示例
if __name__ == "__main__":
    random.seed(42)
    prices = generate_prices(length=20, min_value=1.0, max_value=10.0)
    prices = [3.5] + prices
    print("Prices:", prices)

    config = {
        "lower_bound": 1,
        "upper_bound": 10,
        "num_grids": 10,
        "leverage": 1.5,
        "investment": 1000,
        "mode": "arithmetic"
    }

    strategy = GridStrategy(config, prices)
    strategy.run_strategy()
    strategy.plot_results()
