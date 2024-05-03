import pandas as pd


def clean_df(df: pd.DataFrame):
  """Cleans DataFrame."""
  # calculate percent change
  df["prev_close"] = df["Close"].shift(1)
  df["percent_chg"] = (df["Close"] - df["prev_close"]) / df["prev_close"]

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
