import requests
import pandas as pd
from io import StringIO
import json


def get_download_link(ticker: str) -> str:
    """
    *Deprecated*
    Gets the yahoo link to download the data for all time

    Parameters:
        ticker(str): ticker to download data for

    Returns:
        link(str): link to call yahoo api
    """
    period_1 = "1"
    period_2 = "9999999999"

    link = (
        "https://query1.finance.yahoo.com/v7/finance/download/"
        + ticker
        + "?period1="
        + period_1
        + "&period2="
        + period_2
        + "&interval=1d&events=history&includeAdjustedClose=true"
    )

    return link


def get_data_from_download_link(link: str) -> pd.DataFrame:
    """*Deprecated*
    Uses the link to download all historical data

    Parameters:
        link(str): link to yahoo api

    Returns:
        df(pd.DataFrame): DataFrame containing the data
    """
    try:
        response = requests.get(link, headers={"User-agent": "Mozilla/5.0"})
        response.raise_for_status()

    except requests.exceptions.RequestException as e:
        print(e.response.text)

        return pd.DataFrame()

    # convert text to string io
    data_str = response.text
    string_io = StringIO(data_str)

    df = pd.read_csv(string_io)

    return df


def get_data(ticker: str) -> pd.DataFrame:
    """Gets all historical data for the ticker

    Parameters:
        ticker(str): stock ticker

    Returns:
        df(pd.DataFrame): DataFrame with cols=["timestamp", "adjclose"]
    """
    period_1 = "1"
    period_2 = "9999999999"

    link = (
        f"https://query1.finance.yahoo.com/v8/finance/chart/{ticker}"
        "?events=capitalGain%7Cdiv%7Csplit&formatted=true&includeAdjustedClose="
        f"true&interval=1d&period1={period_1}&period2={period_2}&symbol={ticker}"
        "&userYfid=true&lang=en-US&region=US"
    )

    try:
        response = requests.get(link, headers={"User-agent": "Mozilla/5.0"})
        response.raise_for_status()

    except requests.exceptions.RequestException as e:
        print(e.response.text)

    json_obj = json.loads(response.text)

    # extract from json
    timestamps = json_obj["chart"]["result"][0]["timestamp"]
    adj_close = json_obj["chart"]["result"][0]["indicators"]["adjclose"][0]["adjclose"]

    # load as df
    df_init_dict = {"timestamp": timestamps, "adjclose": adj_close}
    df = pd.DataFrame(df_init_dict)

    return df
