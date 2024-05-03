import pandas as pd

from utils import utils


def test_clean_df():
  df = pd.read_csv("data/NRDY.csv")

  df = utils.clean_df()

  assert df


def test_find_pattern():
  df = pd.read_csv("data/NRDY.csv")
  df = utils.clean_df(df)

  utils.find_pattern(df)