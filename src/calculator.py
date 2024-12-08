
def get_profit_rate(before_price, after_price):
    return (after_price - before_price) / before_price

def unit_grid_profit(profit_rate, stock_nums):
    return profit_rate * stock_nums

# 重仓均价 

# 爆仓线
# 每个网格购买股票量 = (投资金额 * 杠杆) / (网格中位数价格 * 网格数量)

def average_hold_price(now_price, now_stock_nums, grid_prices, grid_stock_nums):
    """
    计算加权平均持仓成本
    :param now_price: 当前价格
    :param now_stock_nums: 当前市场价格下持有的股票数量
    :param grid_prices: 网格价格列表
    :param grid_stock_nums: 各网格持仓股票数量列表
    :return: 平均持仓成本
    """
    total_stock_nums = now_stock_nums + sum(grid_stock_nums)  # 总持仓股票数量
    if total_stock_nums == 0:
        return 0  # 如果没有持仓，平均成本为 0
    
    # 计算加权平均持仓成本
    total_value = (now_price * now_stock_nums + 
                   sum(price * stock_nums for price, stock_nums in zip(grid_prices, grid_stock_nums)))
    return total_value / total_stock_nums


def break_line(now_price, now_stock_nums, grid_prices, grid_stock_nums, leverage):
    """
    计算爆仓线
    :param now_price: 当前价格
    :param now_stock_nums: 当前市场价格下持有的股票数量
    :param grid_prices: 网格价格列表
    :param grid_stock_nums: 各网格持仓股票数量列表
    :param leverage: 杠杆比例
    :return: 爆仓线价格
    """
    # 计算加权平均持仓成本
    agv_hold_price = average_hold_price(now_price, now_stock_nums, grid_prices, grid_stock_nums)
    
    # 计算爆仓线
    return (1 - (1 / leverage)) * agv_hold_price
