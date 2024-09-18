import pandas as pd
from datetime import date
from datetime import timedelta
import polars as pl


def clean_df(df: pd.DataFrame):
    """*Deprecated* Cleans DataFrame."""
    # calculate percent change
    prev_close = df["Close"].shift(1)
    df["percent_chg"] = (df["Close"] - prev_close) / prev_close

    # format date column
    df["Date"] = df["Date"].apply(date.fromisoformat)

    # delete rows with missing data
    df.dropna(inplace=True)

    # shorten to include only 10 years
    max_date = df["Date"].iloc[-1]
    min_date = max_date.replace(year=max_date.year - 10)
    df = df.loc[df["Date"] > min_date]

    return df


def convert_to_percentage(df: pl.DataFrame):
    """Converts the df to percentage change for all but date column
    
    Parameters:
        df(pl.DataFrame): has column date

    Returns:
        percent_df(pl.DataFrame): same columns as df
    """
    percent_df = df.select(
        pl.col("date"),
        pl.all().exclude("date").pct_change()
    )

    # drop first row
    percent_df = percent_df[1:]

    return percent_df


def generate_pattern_from_date(initial_date: date, dates: pl.Series):
    """Generates a pattern of dates, starting from the initial_date
    Parameters:
        initial_date(datetime.date): starting date
        df(DataFrame): stock price data with columns [Date, percent_chg]

    Returns:
        pattern(list): list of dates
    """
    max_date = dates[-1]

    cur_date = initial_date
    pattern = []
    i = 0

    dates_set = set(dates)

    # construct pattern of dates one quarter apart by looping while cur_date is within
    # dataset
    while cur_date <= max_date:
        # find closest date in df
        while cur_date not in dates_set and cur_date <= max_date:
            cur_date = (cur_date + pd.DateOffset(days=1)).date()

        # check cur_date has not left range
        if cur_date <= max_date:
            pattern.append(cur_date)

        # create new date i quarters from first date, format as datetime.date
        i += 1
        cur_date = (initial_date + pd.DateOffset(months=(3 * i))).date()

    return pattern


def generate_possible_patterns(dates: pl.Series):
    """Generates a list of all possible patterns.

    Parameters:
        dates(pl.Series): all dates as type datetime.date

    Returns:
        patterns(list): list of list of dates
    """
    possible_patterns = []

    # range of dates
    min_date = dates[0]
    max_date = dates[-1]

    initial_date = min_date
    # loop for all possible initial dates, initial_date does not necessarily have to be
    # in the dataset
    while initial_date <= max_date:
        pattern = generate_pattern_from_date(initial_date, dates)

        # append created pattern to possible patterns
        possible_patterns.append(pattern)

        # increment initial_date
        initial_date = (initial_date + pd.DateOffset(days=1)).date()

    return possible_patterns


def summarize_pattern(pattern: list, df: pl.DataFrame):
    """summarizes a pattern, finding the number of days the stock decreased, mean, and
    standard deviation.

    Parameters:
        pattern(list): list of dates
        df(DataFrame): stock price data with columns [date, value]

    Returns:
        days_decreased(int)
        mean(float): mean of percent_chg
        stdev: standard deviation of percent_chg
    """
    # get rows in pattern
    rows = df.filter(pl.col("date").is_in(pattern))

    days_decreased = rows.filter(pl.col("value") < 0).height

    mean = rows["value"].mean()
    stdev = rows["value"].std(ddof=0)

    return days_decreased, mean, stdev


def summarize_pattern_next_day(pattern: list, df: pl.DataFrame):
    """summarizes the following days of a pattern, finding the number of days the stock
    decreased, mean, and standard deviation.

    Parameters:
        pattern(list): list of dates
        df(DataFrame): stock price data with columns [date, value]

    Returns:
        days_decreased(int)
        mean(float): mean of percent_chg
        stdev: standard deviation of percent_chg
    """
    # shift value column
    df = df.select(
        "date",
        pl.col("value").shift(-1)
        )
    
    # call summarize_pattern
    return summarize_pattern(pattern, df)


def evaluate_pattern(pattern: list, df: pl.DataFrame) -> bool:
    """Evaluated whether a pattern is 'good' or 'bad'

    Parameters:
        pattern(list): list of dates
        df(DataFrame): stock price data with columns[date, value]

    Returns:
        evaluation(boolean): if the pattern is 'good'
    """
    days_decreased, mean, stdev = summarize_pattern(pattern, df)
    next_days_decreased, next_mean, next_stdev = summarize_pattern_next_day(pattern, df)

    # must be longer than two years
    if len(pattern) < 8:
        return False

    # mean must be < 0
    if mean >= 0.01:
        return False

    # percentage of days decreased must be >= .9
    if days_decreased / len(pattern) <= 0.75:
        return False

    # next days mean must also be < 0
    if next_mean >= 0.01:
        return False

    # next days percentage of days decreased must be >= .75
    if next_days_decreased / len(pattern) <= 0.75:
        return False

    return True


def find_good_patterns(df: pl.DataFrame) -> list:
    """Find patterns in stock prices.

    Parameters:
        df(DataFrame): stock price data with columns [date, value]

    Returns:
        good_patterns(list): patterns that have been evaluated as 'good'
    """
    dates = df["date"]
    possible_patterns = generate_possible_patterns(dates)

    good_patterns = []
    for pattern in possible_patterns:
        evaluation = evaluate_pattern(pattern, df)

        if evaluation:
            good_patterns.append(pattern)

    return good_patterns


def prune_patterns(patterns: list):
    """Prunes away patterns that are a subset of other longer patterns or are the
    following days of other patterns.

    Parameters:
        patterns(list): list of list of dates

    Returns:
        pruned_patterns(list): list of list of dates
    """
    patterns.sort(key=lambda x: len(x), reverse=True)
    pruned_patterns = []
    for pattern in patterns:
        new_pattern = True
        for date_1 in pattern:
            for pruned_pattern in pruned_patterns:
                for date_2 in pruned_pattern:
                    # remove if date is either same as pruned_date or within 5 days
                    # after pruned_date
                    if date_1 - timedelta(days=5) < date_2 and date_1 >= date_2:
                        new_pattern = False
        if new_pattern:
            pruned_patterns.append(pattern)

    return pruned_patterns


def get_wilshire_tickers():
    """Gets the tickers for the companies in the wilshire 5000 as listed in
    data/Wilshire-5000-Stocks.csv from
    https://github.com/derekbanas/Python4Finance/blob/main/Wilshire-5000-Stocks.csv
    """
    wilshire_df = pd.read_csv("data/Wilshire-5000-Stocks.csv")

    tickers = wilshire_df["Ticker"].to_list()

    return tickers
