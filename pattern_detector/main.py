import pandas as pd
from io import StringIO

from pattern_detector import collect
from pattern_detector import utils


def get_wilshire_tickers():
    """Gets the tickers for the companies in the wilshire 5000 as listed in
    data/Wilshire-5000-Stocks.csv from
    https://github.com/derekbanas/Python4Finance/blob/main/Wilshire-5000-Stocks.csv
    """
    wilshire_df = pd.read_csv("data/Wilshire-5000-Stocks.csv")

    tickers = wilshire_df["Ticker"].to_list()

    return tickers


def log_pattern(ticker, pattern, df, filepath=None):
    """Logs the pattern and its summarizations
    Parameters:
        ticker(str): the stock ticker
        pattern(list): list of dates
        df(DataFrame): stock price data
        filepath(os.path): path to output log
    """
    if filepath is None:
        filepath = "data/good_patterns.csv"

    with open(filepath, "a") as outfile:
        row = []
        row.append(ticker)
        row.append(pattern)
        row.extend(utils.summarize_pattern(pattern, df))
        row.extend(utils.summarize_pattern_next_day(pattern, df))

        # format row as strings
        row = [str(x) for x in row]

        outfile.write(";".join(row) + "\n")


def main():
    tickers = get_wilshire_tickers()

    for ticker in tickers:
        # collect data
        link = collect.get_download_link(ticker)
        data_str = collect.get_data(link)

        # format as df
        string_io = StringIO(data_str)
        df = pd.read_csv(string_io)

        # clean df
        df = utils.clean_df(df)

        # find good patterns
        patterns = utils.find_good_patterns(df)

        # log patterns
        for pattern in patterns:
            log_pattern(ticker, pattern, df)


if __name__ == "__main__":
    main()
