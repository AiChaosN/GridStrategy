
def get_profit_rate(before_price, after_price):
    return (after_price - before_price) / before_price

def unit_grid_profit(profit_rate, stock_nums):
    return profit_rate * stock_nums


# 爆仓线
def break_line(now_price, now_stock_nums, grid_prices, grid_stock_nums, leverage, total_stock_nums):
    agv_hold_price = (now_price * now_stock_nums + sum([price * stock_nums for price, stock_nums in zip(grid_prices, grid_stock_nums)])) / total_stock_nums
    return (1-(1/leverage)) * agv_hold_price


