import pandas as pd


def clean_df(df):
  """Cleans DataFrame."""
  df["chg"] = df["Close"] - df["Close"].shift(1)

  df["percent_chg"] = df["delta"] / df["Close"].shift(1)

  return df


def find_pattern(df):
  """
  Find patterns in stock prices.

  Parameters:
    df(DataFrame): stock price data with columns [Date, percent_chg]

  Returns:
    pattern(list): dates with reoccurring changes    
  """
  pass
