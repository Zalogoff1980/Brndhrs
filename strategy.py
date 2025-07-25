import pandas as pd
import pandas_ta as ta
import requests

API_KEY = "9103d4440a664b8288cdb40f86cc1515"

def get_rsi(symbol="EUR/USD", interval="1min", length=14):
    symbol = symbol.replace("/", "")
    url = f"https://api.twelvedata.com/time_series?symbol={symbol}&interval={interval}&outputsize=100&apikey={API_KEY}"

    try:
        response = requests.get(url, timeout=10)
        data = response.json()

        if "values" not in data:
            print("Ошибка данных:", data)
            return None

        closes = [float(i['close']) for i in data['values']]
        closes.reverse()
        df = pd.DataFrame(closes, columns=["close"])
        rsi_series = ta.rsi(df["close"], length=length)
        return round(rsi_series.iloc[-1], 2)

    except Exception as e:
        print("Ошибка RSI:", e)
        return None
