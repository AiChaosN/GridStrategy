class TradingConfig:
    def __init__(self, 
                 start_time=None,
                 end_time=None,
                 price_lower=None,
                 price_upper=None,
                 grid_size=None,
                 contract_size=None,
                 leverage=None,
                 initial_capital=None,
                 fee_rate=None):
        self.start_time = start_time
        self.end_time = end_time
        self.price_lower = price_lower
        self.price_upper = price_upper
        self.grid_size = grid_size
        self.contract_size = contract_size
        self.leverage = leverage
        self.initial_capital = initial_capital
        self.fee_rate = fee_rate

    def validate(self):
        if not all([self.price_lower, self.price_upper, self.grid_size, 
                   self.contract_size, self.leverage, self.initial_capital]):
            raise ValueError("All trading parameters must be set")
        if self.price_lower >= self.price_upper:
            raise ValueError("Upper price must be greater than lower price")
        if self.grid_size <= 0:
            raise ValueError("Grid size must be positive")
        if self.leverage <= 0:
            raise ValueError("Leverage must be positive")