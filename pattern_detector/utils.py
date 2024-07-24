import pandas as pd
from datetime import date
from datetime import timedelta


def clean_df(df: pd.DataFrame):
    """Cleans DataFrame."""
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


def generate_pattern_from_date(initial_date: date, df: pd.DataFrame):
    """Generates a pattern of dates, starting from the initial_date
    Parameters:
        initial_date(datetime.date): starting date
        df(DataFrame): stock price data with columns [Date, percent_chg]

    Returns:
        pattern(list): list of dates
    """
    max_date = df["Date"].iloc[-1]

    cur_date = initial_date
    pattern = []
    i = 0

    dates_set = set(df["Date"])

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


def generate_possible_patterns(df: pd.DataFrame):
    """Generates a list of all possible patterns.

    Parameters:
        df(DataFrame): stock price data with columns [Date, percent_chg]

    Returns:
        patterns(list): list of list of dates
    """
    possible_patterns = []

    # range of dates
    min_date = df["Date"].iloc[0]
    max_date = df["Date"].iloc[-1]

    initial_date = min_date
    # loop for all possible initial dates, initial_date does not necessarily have to be
    # in the dataset
    while initial_date <= max_date:
        pattern = generate_pattern_from_date(initial_date, df)

        # append created pattern to possible patterns
        possible_patterns.append(pattern)

        # increment initial_date
        initial_date = (initial_date + pd.DateOffset(days=1)).date()

    return possible_patterns


def summarize_pattern(pattern: list, df: pd.DataFrame):
    """summarizes a pattern, finding the number of days the stock decreased, mean, and
    standard deviation.

    Parameters:
        pattern(list): list of dates
        df(DataFrame): stock price data with columns [Date, percent_chg]

    Returns:
        days_decreased(int)
        mean(float): mean of percent_chg
        stdev: standard deviation of percent_chg
    """
    # get rows in pattern
    rows = df[df["Date"].isin(pattern)]

    days_decreased = 0
    for index, row in rows.iterrows():
        if row["percent_chg"] <= 0:
            days_decreased += 1

    mean = rows["percent_chg"].mean()
    stdev = rows["percent_chg"].std(ddof=0)  # population instead of sample

    return days_decreased, mean, stdev


def summarize_pattern_next_day(pattern: list, df: pd.DataFrame):
    """summarizes the following days of a pattern, finding the number of days the stock
    decreased, mean, and standard deviation.

    Parameters:
        pattern(list): list of dates
        df(DataFrame): stock price data with columns [Date, percent_chg]

    Returns:
        days_decreased(int)
        mean(float): mean of percent_chg
        stdev: standard deviation of percent_chg
    """
    # get rows in pattern
    shifted_df = df.shift(-1)
    rows = shifted_df[df["Date"].isin(pattern)]

    days_decreased = 0
    for index, row in rows.iterrows():
        if row["percent_chg"] <= 0:
            days_decreased += 1

    mean = rows["percent_chg"].mean()
    stdev = rows["percent_chg"].std(ddof=0)  # population instead of sample

    return days_decreased, mean, stdev


def evaluate_pattern(pattern: list, df: pd.DataFrame):
    """Evaluated whether a pattern is 'good' or 'bad'

    Parameters:
        pattern(list): list of dates
        df(DataFrame): stock price data with columns[Date, percent_chg]

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


def find_good_patterns(df: pd.DataFrame):
    """Find patterns in stock prices.

    Parameters:
        df(DataFrame): stock price data with columns [Date, percent_chg]

    Returns:
        good_patterns(list): patterns that have been evaluated as 'good'
    """
    possible_patterns = generate_possible_patterns(df)

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
