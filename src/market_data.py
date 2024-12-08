import requests


# 需要修改整体构造, 传入参数: url, parmars, 传出参数: return_data
# TODO
class MarketData:
    def __init__(self, config):
        self.config = config
        self.prices = []
        self.timestamps = []
        self.data = None

    

    def fetch_real_data(self):
        """
        Fetch BTC price history from Livecoinwatch API and return a list of prices.
        
        :param config: Configuration JSON object containing API parameters
            - api_key: Your API key for Livecoinwatch
            - currency: Currency code (e.g., "USD")
            - code: Cryptocurrency code (e.g., "BTC")
            - start: Start timestamp in milliseconds
            - end: End timestamp in milliseconds
        :return: List of BTC prices during the given time period
        """
        config = self.config
        url = config["url"]
        headers = {
            "content-type": "application/json",
            "x-api-key": config["api_key"]
        }
        payload = {
            "currency": config.get("currency", "USD"),
            "code": config.get("code", "BTC"),
            "start": config.get("start"),
            "end": config.get("end"),
            "meta": True
        }
        
        try:
            response = requests.post(url, headers=headers, json=payload)
            response.raise_for_status()  # Raise an error for HTTP errors
            data = response.json()
            history = data.get("history", [])
            prices = [entry["rate"] for entry in history]
            time = [entry["date"] for entry in history]
            self.data = data
            return prices, time
        except requests.exceptions.RequestException as e:
            print(f"Error fetching data: {e}")
            return []
    
    def get_data(self):
        return self.data

# 示例配置和调用
import os
if __name__ == "__main__":
    
    # Example usage
    config = {
        "url": "https://api.livecoinwatch.com/coins/single/history",
        "api_key": os.getenv("LIVECOINWATCH_API_KEY"),
        "currency": "USD",
        "code": "BTC",
        "start": 1617035100000,
        "end": 1617035400000
    }
    prices, time = MarketData(config).fetch_real_data()
    print(prices)
    print(time)

    print("Prices:", prices[:5])
    print("Time:", time[:5])
