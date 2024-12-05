import random


class GridCalculator:
    def __init__(self, config, prices):
        # 初始参数
        self.config = config
        self.prices = prices
        self.begin_price = prices[0]

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
            if i < self.begin_price:
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
        self.config["initial_investment"] -= self.begin_price * nums
        print("初始买入", "股票数量", nums, "总资产", self.config["initial_investment"])

    
    def run(self):
        for i in range(1, len(self.prices)):
            price = self.prices[i]
            if price in self.grid:
                index = self.grid.index(price)
                if self.strategy[index] == 0:
                    # 买入
                    self.Number_stocks[index] = self.config["initial_investment"] / price
                    self.strategy[index] = 1
                    print("买入价格", price, "股票数量", self.Number_stocks[index], "总资产", self.config["initial_investment"])
                else:
                    # 卖出
                    self.Number_stocks[index] = 0
                    self.strategy[index] = 0
                    print("卖出价格", price, "股票数量", self.Number_stocks[index], "总资产", self.config["initial_investment"])




# 使用示例
if __name__ == "__main__":

    prices = [random.randint(1, 9) for _ in range(10)]
    print("prices:", prices)


    config = {
        "lower_bound": 1,
        "upper_bound": 10,
        "num_grids": 10,
        "leverage": 1,
        "initial_investment": 1000,
        "mode": "arithmetic"
    }
    grid_calc = GridCalculator(config, prices)
    grid_calc.generate_grid()

    print("开始交易")
    grid_calc.run()