import pandas as pd
from datetime import date
import numpy as np

from utils import utils


def load_test_df():
  df = pd.read_csv("data/NRDY.csv")

  return df

def test_clean_df():
  # load and clean data
  df = load_test_df()
  df = utils.clean_df(df)

  # test percent_chg
  assert "percent_chg" in df
  
  correct_val = (3.000000 - 3.510000) / 3.510000
  assert np.isclose(df["percent_chg"].iloc[0], correct_val)

  # test date
  assert type(df["Date"].iloc[0]) == date
  

def test_generate_possible_patterns():
  # load and clean data
  df = load_test_df()
  df = utils.clean_df(df)

  possible_patterns = utils.generate_possible_patterns(df)

  # test output
  correct_first_pattern = [date.fromisoformat(x) for x in ["2023-05-03", "2023-08-03", "2023-11-03", "2024-02-05"]]
  assert possible_patterns[0] == correct_first_pattern

  correct_last_pattern = [date.fromisoformat("2024-05-02")]
  assert possible_patterns[-1] == correct_last_pattern

  assert len(possible_patterns) == 252


def test_find_pattern():
  # load and clean data
  df = load_test_df()
  df = utils.clean_df(df)

  # find pattern
  pattern = utils.find_pattern(df)

  # test pattern
  correct_pattern = ["2023-05-15", "2023-08-15", "2023-11-15", "2024-02-15"]
  assert pattern == correct_pattern
