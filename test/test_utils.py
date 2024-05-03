import pandas as pd

from utils import utils


def test_clean_df():
  df = pd.read_csv("data/NRDY.csv")

  df = utils.clean_df(df)

  assert "percent_chg" in df


def test_find_pattern():
  df = pd.read_csv("data/NRDY.csv")
  df = utils.clean_df(df)

  pattern = utils.find_pattern(df)

  correct_pattern = ["2023-05-15", "2023-08-15", "2023-11-15", "2024-02-15"]

  assert pattern == correct_pattern
