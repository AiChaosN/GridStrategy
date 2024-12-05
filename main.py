from config import TradingConfig
from market_data import MarketData
from grid_calculator import GridCalculator
from risk_metrics import RiskMetrics
from visualization import GridVisualizer

import matplotlib
matplotlib.use("Agg")  # 强制使用无 GUI 的后端


def main():
    # Initialize configuration
    config = TradingConfig(
        price_lower=20000,
        price_upper=30000,
        grid_size=500,
        contract_size=0.1,
        leverage=5,
        initial_capital=10000,
        fee_rate=0.0004
    )
    
    try:
        # Validate configuration
        config.validate()
        
        # Initialize components
        market_data = MarketData(config)
        grid_calc = GridCalculator(config)
        risk_metrics = RiskMetrics(config)
        visualizer = GridVisualizer(config)
        
        # Generate or fetch market data
        prices, timestamps = market_data.generate_simulated_data()
        
        # Process price updates
        trades = []
        equity_curve = [config.initial_capital]
        
        for i, (price, timestamp) in enumerate(zip(prices, timestamps)):
            realized_pnl, unrealized_pnl = grid_calc.process_price_update(price, timestamp)
            current_equity = config.initial_capital + realized_pnl + unrealized_pnl
            equity_curve.append(current_equity)
            risk_metrics.update_equity_curve(current_equity)
            
            if grid_calc.trades:
                trades.append((timestamp, price, grid_calc.trades[-1].side))
        
        # Calculate risk metrics
        max_drawdown = risk_metrics.calculate_max_drawdown()
        sharpe_ratio = risk_metrics.calculate_sharpe_ratio()
        
        # Print results
        print(f"\nTrading Results:")
        print(f"Initial Capital: ${config.initial_capital:,.2f}")
        print(f"Final Equity: ${equity_curve[-1]:,.2f}")
        print(f"Total Return: {((equity_curve[-1]/config.initial_capital - 1) * 100):,.2f}%")
        print(f"Maximum Drawdown: {max_drawdown*100:.2f}%")
        print(f"Sharpe Ratio: {sharpe_ratio:.2f}")
        
        # Visualize results
        visualizer.plot_trading_view(prices, timestamps, trades)
        visualizer.plot_equity_curve(equity_curve, timestamps)
        
    except ValueError as e:
        print(f"Configuration Error: {str(e)}")
    except Exception as e:
        print(f"An error occurred: {str(e)}")

if __name__ == "__main__":
    main()