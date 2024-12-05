import numpy as np
from typing import List

class RiskMetrics:
    def __init__(self, config):
        self.config = config
        self.equity_curve: List[float] = []
        
    def calculate_max_drawdown(self) -> float:
        """Calculate maximum drawdown from equity curve"""
        if not self.equity_curve:
            return 0
        
        peak = self.equity_curve[0]
        max_dd = 0
        
        for equity in self.equity_curve:
            if equity > peak:
                peak = equity
            dd = (peak - equity) / peak
            max_dd = max(max_dd, dd)
            
        return max_dd

    def calculate_sharpe_ratio(self, risk_free_rate: float = 0.02) -> float:
        """Calculate Sharpe ratio"""
        if len(self.equity_curve) < 2:
            return 0
            
        returns = np.diff(self.equity_curve) / self.equity_curve[:-1]
        excess_returns = returns - risk_free_rate/252  # Assuming daily data
        
        if np.std(excess_returns) == 0:
            return 0
            
        return np.sqrt(252) * np.mean(excess_returns) / np.std(excess_returns)

    def update_equity_curve(self, equity: float):
        """Update equity curve with new equity value"""
        self.equity_curve.append(equity)