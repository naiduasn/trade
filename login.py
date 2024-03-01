from snapi_py_client.snapi_bridge import StocknoteAPIPythonBridge
import json
import utils
from utils import symbol_map
import os
from dotenv import load_dotenv

latest_data = {}
def handle_data(self,data):
    # Process and format the data
        stock_data = json.loads(data)
        security_id = stock_data['response']['data']['sym']
        symbol = symbol_map[security_id.split('_')[0]]
        # Update latest data for the symbol
        global latest_data
        latest_data[symbol] = stock_data['response']['data']
        print(latest_data)
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
    samco.start_streaming()

if __name__ == "__main__":
    main()