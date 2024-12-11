class Calculator:
    def get_profit_rate(before_price, after_price):
        return (after_price - before_price) / before_price

    def unit_grid_profit(profit_rate, stock_nums):
        return profit_rate * stock_nums

    def get_average_hold_price(now_price, now_stock_nums, grid_prices, grid_stock_nums):
        """
        计算加权平均持仓成本
        :param now_price: 当前价格
        :param now_stock_nums: 当前市场价格下持有的股票数量
        :param grid_prices: 网格价格列表
        :param grid_stock_nums: 各网格持仓股票数量列表
        :return: 平均持仓成本
        平均持仓成本 = (当前价格 * 当前持仓股票数量 + 低于当前的(网格价格 * 网格持仓股票数量)之和 / 总持仓股票数量
        """
        total_stock_nums = now_stock_nums
        total_cost = now_price * now_stock_nums
        for i in range(len(grid_prices)):
            if grid_prices[i] < now_price:
                total_stock_nums += grid_stock_nums[i]
                total_cost += grid_prices[i] * grid_stock_nums[i]
        return total_cost / total_stock_nums


    def break_line(leverage, average_hold_price):
        """
        计算爆仓线
        :leverage: 杠杆
        :average_hold_price: 加权平均持仓成本
        :return: 爆仓线价格
        爆仓线 = (1 - (1 / 杠杆)) * 平均持仓成本
        """
        return (1 - (1 / leverage)) * average_hold_price



    # 套利次数是指在一次套利中，买入和卖出的次数
    def Arbitrage_frequency():
        pass