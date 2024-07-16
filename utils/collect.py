import requests


def get_download_link(ticker):
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
    try:
        response = requests.get(link, headers={"User-agent": "Mozilla/5.0"})
        response.raise_for_status()

        return response.text
    except requests.exceptions.RequestException as e:
        print(e.response.text)
