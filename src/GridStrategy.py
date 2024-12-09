import random
# import matplotlib.pyplot as plt
from .calculator import Calculator

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
        self.grid_prices = self._generate_grid()   # 网格价格
        self.grid_median_price = (self.upper_bound + self.lower_bound) / 2   # 网格中间价格
        self.grid_stock_amount = (self.investment * self.leverage) / (self.grid_median_price * self.num_grids)   # 每网格购买的股票量
        print("每网格购买的股票量:", self.grid_stock_amount)
        self.grid_stocks = [self.grid_stock_amount for _ in range(len(self.grid_prices))]    # 各网格持仓股票数量
        self.strategy = [0 if price <= prices[0] else 1 for price in self.grid_prices] # 各网格 0: 买入 1: 卖出
        self.hold_stocks = sum(i*j for i, j in zip(self.strategy, self.grid_stocks))  # 持有股票数量

        self.cash_balance = self.investment 
        self.total_assets = []

        # 指标
        self.average_hold_price = 0
        self.break_line = 0

        # 计算指标
        self._begin()


    def _begin(self):
        """
        最初开始状态
        """
        self.average_hold_price = Calculator.get_average_hold_price(self.prices[0], sum(self.grid_stocks), self.grid_prices, self.grid_stocks)
        self.break_line = Calculator.break_line(self.leverage, self.average_hold_price)

        # 股票数量 amount

    def _generate_grid(self):
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

    def execute_trade(self, index, current_price):
        """
        执行网格交易，包含买入和卖出逻辑。
        :param index: 当前网格的索引
        :param current_price: 当前价格
        """
        grid_price = self.grid_prices[index]

        # 买入逻辑
        if self.strategy[index] == 0:
            cost = grid_price * self.grid_stock_amount
            if self.cash_balance >= cost:
                self.cash_balance -= cost
                self.grid_stocks[index] += self.grid_stock_amount
                self.strategy[index] = 1  # 更新为可卖出状态
                self._log_transaction("buy", index, grid_price, cost, current_price)
            else:
                print(f"Insufficient balance to buy at grid {index}. Cash: {self.cash_balance}, Cost: {cost}")
        
        # 卖出逻辑
        elif self.strategy[index] == 1:
            revenue = grid_price * self.grid_stocks[index]
            self.cash_balance += revenue
            self.grid_stocks[index] = 0
            self.strategy[index] = 0  # 更新为可买入状态
            self._log_transaction("sell", index, grid_price, revenue, current_price)
        
        # 更新总资产
        total_stocks_value = sum(stock * current_price for stock in self.grid_stocks)
        self.total_assets.append(self.cash_balance + total_stocks_value)

    def _log_transaction(self, action, index, grid_price, amount, current_price):
        """
        记录交易日志（内部辅助方法）。
        """
        print(f"Action: {action.upper()}, Grid Index: {index}, Grid Price: {grid_price:.2f}, "
            f"Amount: {amount:.2f}, Current Price: {current_price:.2f}, "
            f"Cash Balance: {self.cash_balance:.2f}")
    
    def run_strategy(self):
        """
        执行网格交易策略，按时间顺序遍历价格，检查跨越的网格并执行交易。
        """
        for i in range(1, len(self.prices)):
            previous_price, current_price = self.prices[i - 1], self.prices[i]
            
            # 找出当前价格区间内被跨越的网格
            crossed_grids = [
                index for index, grid_price in enumerate(self.grid_prices)
                if min(previous_price, current_price) <= grid_price <= max(previous_price, current_price)
            ]
            
            # 如果没有网格被跨越，跳过本次循环
            if not crossed_grids:
                continue
            
            # 按顺序执行跨越网格的交易
            for index in crossed_grids:
                self.execute_trade(index, current_price)

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
        "leverage": 10,
        "investment": 50,
        "mode": "arithmetic"
    }

    strategy = GridStrategy(config, prices)
    print("网格价格:", strategy.grid_prices)
    print("中位数价格:", strategy.grid_median_price)
    print("网格持仓股票数量:", strategy.grid_stocks)
    print("当前股票数量:", strategy.hold_stocks)
    print("平均持仓成本:", strategy.average_hold_price)
    print("爆仓线:", strategy.break_line)
    strategy.run_strategy()
    strategy.plot_results()
