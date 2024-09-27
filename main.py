from typing import Union
from logger import logger
from fastapi import FastAPI, Response, BackgroundTasks
from pydantic import BaseModel
import os
import json

app = FastAPI()

stock_data = {}

# Example usage
@app.get("/")
def read_root():
    return {"Hello": "World"}

def load_file():
    current_directory = os.getcwd()

    # Name of your JSON file
    file_name = 'stocks.json'

    # Construct the full file path
    file_path = os.path.join(current_directory, file_name)

    # Open the file in read mode
    with open(file_path, 'r') as file:
        # Load the JSON data
        data = json.load(file)
    return data

@app.get("/metrics")
async def metrics(response: Response):

    metrics_data = []
    stock_data = load_file()
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
    logger.info(prometheus_metrics)
    response.headers["Content-Type"] = "text/plain; version=0.0.4"
    return Response(content=prometheus_metrics)
    #return Response(content=file_content)
    # Return metrics in Prometheus format
    #return response_body