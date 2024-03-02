from typing import Union
import json
from fastapi import FastAPI, Response
from pydantic import BaseModel

app = FastAPI()

stock_data = {
  "PETRONET": {
    "aPr": "282.00",
    "aSz": "2432",
    "avgPr": "282.84",
    "bPr": "281.80",
    "bSz": "520",
    "c": "282.70",
    "ch": "-0.70",
    "chPer": "-0.25",
    "delta": "0.00",
    "gamma": "0.0000",
    "h": "284.25",
    "iv": "0.00",
    "l": "278.90",
    "ltp": "282.00",
    "ltq": "1",
    "ltt": "02 Mar 2024, 12:03:56 PM",
    "lttUTC": "02 Mar 2024, 06:33:56 AM",
    "o": "282.75",
    "oI": "56376000",
    "oIChg": "5.6376e+07",
    "sym": "11351_NSE",
    "tBQ": "118168",
    "tSQ": "157072",
    "theta": "0.00",
    "ttv": "40469878.04",
    "vega": "0.00",
    "vol": "143084",
    "yH": "296.45",
    "yL": "191.70"
  },
  "MAHABANK": {
    "aPr": "60.55",
    "aSz": "10341",
    "avgPr": "60.67",
    "bPr": "60.50",
    "bSz": "1262",
    "c": "60.75",
    "ch": "-0.25",
    "chPer": "-0.41",
    "delta": "0.00",
    "gamma": "0.0000",
    "h": "60.95",
    "iv": "0.00",
    "l": "60.45",
    "ltp": "60.50",
    "ltq": "50",
    "ltt": "02 Mar 2024, 12:03:54 PM",
    "lttUTC": "02 Mar 2024, 06:33:54 AM",
    "o": "60.95",
    "oI": "0",
    "oIChg": "0",
    "sym": "11377_NSE",
    "tBQ": "302235",
    "tSQ": "1076761",
    "theta": "0.00",
    "ttv": "91599563.24",
    "vega": "0.00",
    "vol": "1509800",
    "yH": "69.45",
    "yL": "22.80"
  },
  "POONAWALLA": {
    "aPr": "465.85",
    "aSz": "158",
    "avgPr": "465.42",
    "bPr": "465.50",
    "bSz": "160",
    "c": "462.75",
    "ch": "3.10",
    "chPer": "0.67",
    "delta": "0.00",
    "gamma": "0.0000",
    "h": "470.00",
    "iv": "0.00",
    "l": "460.10",
    "ltp": "465.85",
    "ltq": "21",
    "ltt": "02 Mar 2024, 12:03:57 PM",
    "lttUTC": "02 Mar 2024, 06:33:57 AM",
    "o": "464.70",
    "oI": "0",
    "oIChg": "0",
    "sym": "11403_NSE",
    "tBQ": "24271",
    "tSQ": "57158",
    "theta": "0.00",
    "ttv": "54388982.77",
    "vega": "0.00",
    "vol": "116860",
    "yH": "519.70",
    "yL": "274.65"
  },
  "BHEL": {
    "aPr": "235.90",
    "aSz": "195",
    "avgPr": "236.68",
    "bPr": "235.80",
    "bSz": "540",
    "c": "235.30",
    "ch": "0.50",
    "chPer": "0.21",
    "delta": "0.00",
    "gamma": "0.0000",
    "h": "238.00",
    "iv": "0.00",
    "l": "235.65",
    "ltp": "235.80",
    "ltq": "5",
    "ltt": "02 Mar 2024, 12:03:57 PM",
    "lttUTC": "02 Mar 2024, 06:33:57 AM",
    "o": "236.55",
    "oI": "150428250",
    "oIChg": "1.50428e+08",
    "sym": "438_NSE",
    "tBQ": "296713",
    "tSQ": "1173238",
    "theta": "0.00",
    "ttv": "416476789.27",
    "vega": "0.00",
    "vol": "1759662",
    "yH": "243.25",
    "yL": "66.30"
  },
  "BIRLACORPN": {
    "aPr": "1679.00",
    "aSz": "17",
    "avgPr": "1668.34",
    "bPr": "1677.25",
    "bSz": "24",
    "c": "1648.50",
    "ch": "28.75",
    "chPer": "1.74",
    "delta": "0.00",
    "gamma": "0.0000",
    "h": "1680.00",
    "iv": "0.00",
    "l": "1639.60",
    "ltp": "1677.25",
    "ltq": "1",
    "ltt": "02 Mar 2024, 12:03:58 PM",
    "lttUTC": "02 Mar 2024, 06:33:58 AM",
    "o": "1648.50",
    "oI": "0",
    "oIChg": "0",
    "sym": "480_NSE",
    "tBQ": "4589",
    "tSQ": "6795",
    "theta": "0.00",
    "ttv": "13063101.93",
    "vega": "0.00",
    "vol": "7830",
    "yH": "1802.00",
    "yL": "843.15"
  }
}

class Item(BaseModel):
    name: str
    price: float
    is_offer: Union[bool, None] = None

def read_file(filename):
    try:
        with open(filename, 'r') as file:
            content = file.read()
        return content
    except FileNotFoundError:
        print(f"File '{filename}' not found.")
        return None

# Example usage

@app.get("/")
def read_root():
    return {"Hello": "World"}


@app.get("/items/{item_id}")
def read_item(item_id: int, q: Union[str, None] = None):
    return {"item_id": item_id, "q": q}


@app.put("/items/{item_id}")
def update_item(item_id: int, item: Item):
    return {"item_name": item.name, "item_id": item_id}

@app.get("/metrics")
async def metrics(response: Response):
    # Dynamically generate Prometheus format data
    prometheus_metrics_template = """
# HELP {metric_name} {help_text}
# TYPE {metric_name} {metric_type}
{metric_data}
"""
    metrics_data = []
    for symbol, stock in stock_data.items():
        price = float(stock["ltp"])
        volume = float(stock["vol"])
        change_percent = float(stock["chPer"])
        avg_price = float(stock["avgPr"])
        
        # Set Prometheus metrics
        metrics_data.append({"metric_name": "stock_price", "help_text": f"The current price of {symbol}", "metric_type": "gauge", "metric_data": {"symbol": symbol, "value": price}})
        metrics_data.append({"metric_name": "stock_volume", "help_text": f"The current volume of {symbol}", "metric_type": "gauge", "metric_data": {"symbol": symbol, "value": volume}})
        metrics_data.append({"metric_name": "stock_change_percent", "help_text": f"The change in price of {symbol}", "metric_type": "gauge", "metric_data": {"symbol": symbol, "value": change_percent}})
        metrics_data.append({"metric_name": "stock_avg_price", "help_text": f"The average price of {symbol}", "metric_type": "gauge", "metric_data": {"symbol": symbol, "value": avg_price}})

    prometheus_metrics = ""
    printed_help_lines = set()
    for metric in metrics_data:
        if metric['metric_name'] not in printed_help_lines:
            prometheus_metrics += f"# HELP {metric['metric_name']} {metric['help_text']}\n"
            prometheus_metrics += f"# TYPE {metric['metric_name']} {metric['metric_type']}\n"
            printed_help_lines.add(metric['metric_name'])
        
        prometheus_metrics += metric['metric_name'] + '{' + ', '.join([f'{key}="{value}"' for key, value in metric['metric_data'].items() if key != 'value']) + '} ' + str(metric['metric_data'].get('value', '')) + '\n'

    
    # filename = "/Users/sabarim/codebase/prometheus-2.50.1.darwin-arm64/metrics2.prom"
    # file_content = read_file(filename)
    # print(file_content)

    response.headers["Content-Type"] = "text/plain; version=0.0.4"
    return Response(content=prometheus_metrics)
    #return Response(content=file_content)
    # Return metrics in Prometheus format
    #return response_body