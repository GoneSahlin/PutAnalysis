import pandas as pd
from io import StringIO

from pattern_detector import collect
from pattern_detector import utils



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
    tickers = utils.get_wilshire_tickers()

    for ticker in tickers:
        try:
            # collect data
            link = collect.get_download_link(ticker)
            data_str = collect.get_data(link)

            # check that data is found, else skip ticker
            if not data_str:
                break

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
        except Exception as e:
            pass


if __name__ == "__main__":
    main()
