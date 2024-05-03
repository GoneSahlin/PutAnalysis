import pandas as pd
from datetime import date
import numpy as np

from utils import utils


def test_clean_df():
  # load and clean data
  df = pd.read_csv("data/NRDY.csv")
  df = utils.clean_df(df)

  # test percent_chg
  assert "percent_chg" in df
  
  correct_val = (3.000000 - 3.510000) / 3.510000
  assert np.isclose(df["percent_chg"].iloc[0], correct_val)

  # test date
  assert type(df["Date"].iloc[0]) == date
  


def test_find_pattern():
  # load and clean data
  df = pd.read_csv("data/NRDY.csv")
  df = utils.clean_df(df)

  # find pattern
  pattern = utils.find_pattern(df)

  # test pattern
  correct_pattern = ["2023-05-15", "2023-08-15", "2023-11-15", "2024-02-15"]
  assert pattern == correct_pattern
