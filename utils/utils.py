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
  """Generates a list of all possible patterns.
  
  Parameters:
    df(DataFrame): stock price data with columns [Date, percent_chg]

  Returns:
    patterns(list): list of list of dates    
  """
  possible_patterns = []

  # range of dates
  min_date = df['Date'].iloc[0]
  max_date = df['Date'].iloc[-1]

  dates_set = set(df['Date'])

  initial_date = min_date
  # loop for all possible initial dates, initial_date does not necessarily have to be in the dataset
  while initial_date <= max_date:
    cur_date = initial_date
    pattern = []
    i = 0

    # construct pattern of dates one quarter apart by looping while cur_date is within dataset
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

    # append created pattern to possible patterns
    possible_patterns.append(pattern)
    
    # increment initial_date
    initial_date = (initial_date + pd.DateOffset(days=1)).date()    

  return possible_patterns


def evaluate_pattern(pattern: list, df: pd.DataFrame):
  """Evaluates a pattern, finding the number of days the stock decreased, mean, and standard deviation.
  
  Parameters:
    pattern(list): list of dates
    df(DataFrame): stock price data with columns [Date, percent_chg]

  Returns:
    days_decreased(int)
    mean(float): mean of percent_chg
    stdev: standard deviation of percent_chg
  """
  # get rows in pattern
  rows = df[df['Date'].isin(pattern)]
  
  days_decreased = 0
  for index, row in rows.iterrows():
    if row['percent_chg'] <= 0:
      days_decreased += 1

  mean = rows['percent_chg'].mean()
  stdev = rows['percent_chg'].std(ddof=0)  # population instead of sample  

  return days_decreased, mean, stdev


def find_pattern(df: pd.DataFrame):
  """
  Find patterns in stock prices.

  Parameters:
    df(DataFrame): stock price data with columns [Date, percent_chg]

  Returns:
    pattern(list): dates with reoccurring changes    
  """
  possible_patterns = generate_possible_patterns(df)

  pattern = []

  return pattern
