import pandas as pd
from datetime import date
import numpy as np
import pytest

from utils import utils


def load_test_df(full=False):
  if full:
    df = pd.read_csv("test/data/full_test.csv")
  else:
    df = pd.read_csv("test/data/test.csv")

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


def test_generate_pattern_from_date():
  # load and clean data
  df = load_test_df()
  df = utils.clean_df(df)

  initial_date = date.fromisoformat("2023-05-03")
  pattern = utils.generate_pattern_from_date(initial_date, df)

  # test output
  correct_pattern = [date.fromisoformat(x) for x in ["2023-05-03", "2023-08-03", 
                                                     "2023-11-03", "2024-02-05"]]
  assert pattern == correct_pattern
  

def test_generate_possible_patterns():
  # load and clean data
  df = load_test_df()
  df = utils.clean_df(df)

  possible_patterns = utils.generate_possible_patterns(df)

  # test output
  correct_first_pattern = [date.fromisoformat(x) for x in ["2023-05-03", "2023-08-03", 
                                                           "2023-11-03", "2024-02-05"]]
  assert possible_patterns[0] == correct_first_pattern

  correct_last_pattern = [date.fromisoformat("2024-05-02")]
  assert possible_patterns[-1] == correct_last_pattern

  assert len(possible_patterns) == 366


def test_summarize_pattern():
  # setup
  df = load_test_df()
  df = utils.clean_df(df)

  pattern = [date.fromisoformat(x) for x in ["2023-05-03", "2023-08-03", "2023-11-03", "2024-02-05"]]

  days_decreased, mean, stdev = utils.summarize_pattern(pattern, df)

  assert days_decreased == 2
  assert np.isclose(mean, -0.0365305)
  assert np.isclose(stdev, 0.06466027494721935)


def test_summarize_pattern_next_day():
  # setup
  df = load_test_df()
  df = utils.clean_df(df)

  pattern = [date.fromisoformat(x) for x in ["2023-05-03", "2023-08-03", "2023-11-03", "2024-02-05"]]

  days_decreased, mean, stdev = utils.summarize_pattern_next_day(pattern, df)

  assert days_decreased == 2
  assert np.isclose(mean, 0.00632875275090846)
  assert np.isclose(stdev, 0.03385370464431046)


def test_find_good_patterns():
  # load and clean data
  df = load_test_df(full=True)
  df = utils.clean_df(df)

  # find patterns
  patterns = utils.find_good_patterns(df)

  # test to ensure that the pattern starting on 2-16-2021 is found
  assert any([pattern[0] == date(2021, 2, 16) for pattern in patterns])


def test_prune_patterns():
  # load and clean data, and find patterns
  df = load_test_df(full=True)
  df = utils.clean_df(df)
  patterns = utils.find_good_patterns(df)

  # prune patterns
  pruned_patterns = utils.prune_patterns(patterns)

  # test to ensure that the pattern starting on 2-16-2021 is found
  assert any([pattern[0] == date(2021, 2, 16) for pattern in patterns])

  # test to ensure no dates are repeated in patterns
  all_dates = []
  for pattern in pruned_patterns:
    all_dates.extend(pattern)
  assert len(set(all_dates)) == len(all_dates)
