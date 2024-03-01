import csv
import requests

symbol_map = {}

def get_csv_data_from_url(url):
  """
  Fetches CSV data from a given URL and returns it as a list of lists.

  Args:
      url: The URL of the CSV file.

  Returns:
      A list of lists containing the CSV data, or None if an error occurs.
  """
  try:
    response = requests.get(url)
    response.raise_for_status()  # Raise an exception for non-2xx status codes

    reader = csv.reader(response.content.decode('utf-8').splitlines())
    data = list(reader)
    return data
  except requests.exceptions.RequestException as e:
    return None, f"Error fetching data from URL: {e}"
  except Exception as e:  # Catch any other unexpected errors
    return None, f"Unexpected error: {e}"

def convert_csv_to_json(csv_data):
    """Converts a list of lists representing CSV data into an array of JSON objects.

    Args:
        csv_data: A list of lists containing the CSV data, where each inner list represents a row.

    Returns:
        A list of JSON objects with the specified format:
        [{"symbol": "13_NSE"}, {"symbol": "22_NSE"}, ...]
    """

    json_data = []
    for symbol, value in csv_data:
        # Combine symbol and exchange with an underscore separator
        print(symbol, value)
        symbol_map[value] = symbol
        combined_symbol = f"{value}_{'NSE'}"  # Assuming NSE exchange

        json_object = {"symbol": combined_symbol}
        json_data.append(json_object)

    return json_data