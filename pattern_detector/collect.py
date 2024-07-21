import requests


def get_download_link(ticker):
    """Gets the yahoo link to download the data for all time

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


def get_data(link):
    """Uses the link to download all historical data

    Parameters:
        link(str): link to yahoo api

    Returns:
        data_str(str): response body containing the data
    """
    try:
        response = requests.get(link, headers={"User-agent": "Mozilla/5.0"})
        response.raise_for_status()

        data_str = response.text
        return data_str
    except requests.exceptions.RequestException as e:
        print(e.response.text)
