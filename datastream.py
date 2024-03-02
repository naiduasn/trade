from snapi_py_client.snapi_bridge import StocknoteAPIPythonBridge
import json
import utils
from utils import symbol_map
import os
from dotenv import load_dotenv
import threading

latest_data = {}
count = 0
lock = threading.Lock()

def close_connection(self):
    print("Closing connection")
    self.logout()

def on_error(self):
    print("on error")


def handle_data(data):
    global count, latest_data

    with lock:
        count += 1
        stock_data = json.loads(data)
        security_id = stock_data['response']['data']['sym']
        symbol = symbol_map[security_id.split('_')[0]]
        latest_data[symbol] = stock_data['response']['data']
        
        if count >= 500:
            count = 0
            write_to_file()

def write_to_file():
    global latest_data

    # File name to save JSON content
    file_name = "stocks.json"

    # Get the current working directory
    current_directory = os.getcwd()

    # Create the full file path
    file_path = os.path.join(current_directory, file_name)

    # Write JSON data to file
    with open(file_path, "w") as json_file:
        json.dump(latest_data, json_file, indent=4)
                
    #print(data)
def main():
    load_dotenv()
    userId = os.getenv("USER_ID")
    password = os.getenv("SECRET_KEY")
    yob = os.getenv("YOB")
    url = os.getenv("NIFTY500")

    samco=StocknoteAPIPythonBridge()
    login=samco.login(body={"userId": userId,'password':password,'yob':yob})
    print("Login details",login)
    ##this will return a user details and generated session token
    login_data = json.loads(login)
    login_session_token = login_data['sessionToken']
    samco.set_session_token(login_session_token)

    data = utils.get_csv_data_from_url(url)
    json_data = utils.convert_csv_to_json(data)
    samco.set_streaming_data(json_data)
    samco.on_message = handle_data
    samco.on_close = close_connection
    streaming_thread = threading.Thread(target=samco.start_streaming)
    streaming_thread.start()

if __name__ == "__main__":
    main()