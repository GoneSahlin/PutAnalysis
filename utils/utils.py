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

  return df


def generate_possible_patterns(df: pd.DataFrame):
  """Generates a list of all possible patterns."""
  possible_patterns = []

  max_date = df['Date'].iloc[-1]

  dates_set = set(df['Date'])

  for index, row in df.iterrows():
    first_date = row['Date']

    i = 0  # first_date should be the first date in the pattern
    pattern = []
    cur_date = first_date

    # loop while cur_date is still within dataset, building a pattern of dates one quarter apart
    while cur_date <= max_date:
      # find closest date in df
      while cur_date not in dates_set and cur_date <= max_date:
        cur_date = (cur_date + pd.DateOffset(days=1)).date()

      # check cur_date has not left range
      if cur_date <= max_date:
        pattern.append(cur_date)
      
      # create new date i quarters from first date, format as datetime.date
      i += 1
      cur_date = (first_date + pd.DateOffset(months=(3 * i))).date()

    # append created pattern to possible patterns
    possible_patterns.append(pattern)

  return possible_patterns


def find_pattern(df: pd.DataFrame):
  """
  Find patterns in stock prices.

  Parameters:
    df(DataFrame): stock price data with columns [Date, percent_chg]

  Returns:
    pattern(list): dates with reoccurring changes    
  """

  pattern = []

  return pattern
