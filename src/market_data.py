import requests


# 需要修改整体构造, 传入参数: url, parmars, 传出参数: return_data
# TODO
class MarketData:
    def __init__(self, config):
        self.config = config
        self.prices = []
        self.timestamps = []

        # 从配置中提取必要的字段
        self.symbol = self.config.get("symbol", "BTCUSDT")
        self.productType = self.config.get("productType", "usdt-futures")
        self.granularity = self.config.get("granularity", "1D")
        self.startTime = self.config.get("startTime", None)
        self.endTime = self.config.get("endTime", None)
        self.kLineType = self.config.get("kLineType", None)
        self.limit = self.config.get("limit", 100)  # 默认获取100条数据

    def fetch_real_data(self):
        """Fetch real market data from Bitget API."""
        base_url = "https://api.bitget.com/api/v2/mix/market/candles"
        
        # 请求参数
        params = {
            "symbol": self.symbol,
            "granularity": self.granularity,
            "limit": self.limit,
            "productType": self.productType
        }

        # 添加开始时间和结束时间，如果提供的话
        if self.startTime:
            params["startTime"] = self.startTime
        if self.endTime:
            params["endTime"] = self.endTime

        try:
            # 发送GET请求
            response = requests.get(base_url, params=params)
            response.raise_for_status()  # 如果状态码不是 200，会抛出异常

            # 解析返回的JSON数据
            data = response.json()

            # 如果API返回数据正常，处理数据
            if data["code"] == "00000" and "data" in data:
                candles = data["data"]

                # 提取价格和时间戳
                self.prices = [float(candle[4]) for candle in candles]  # 收盘价
                self.timestamps = [int(candle[0]) for candle in candles]  # 时间戳

                # 打印返回的数据（可选）
                # print("Fetched Data:")
                # print("Timestamps:", self.timestamps)
                # print("Prices:", self.prices)

                return self.prices, self.timestamps
            else:
                print(f"API Error: {data.get('msg', 'Unknown error')}")
                return [], []

        except requests.exceptions.RequestException as e:
            print(f"Error fetching data: {e}")
            return [], []

# 示例配置和调用
if __name__ == "__main__":
    config = {
        "symbol": "BTCUSDT",
        "productType": "usdt-futures",
        "granularity": "5m",  # 5分钟K线
        "limit": 100,  # 获取100条数据
        "startTime": None,
        "endTime": None
    }

    market_data = MarketData(config)
    prices, timestamps = market_data.fetch_real_data()

    print("Prices:", prices)
    print("Timestamps:", timestamps)
