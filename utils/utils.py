import pandas as pd
from datetime import date


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


def find_pattern(df: pd.DataFrame):
  """
  Find patterns in stock prices.

  Parameters:
    df(DataFrame): stock price data with columns [Date, percent_chg]

  Returns:
    pattern(list): dates with reoccurring changes    
  """
  for row in df.iterrows():
    pass


  pattern = []

  return pattern
