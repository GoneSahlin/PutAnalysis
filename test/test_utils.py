import pandas as pd
from datetime import date
import numpy as np
import polars as pl
import pytest

from pattern_detector import utils


def load_test_df(full=False, clean=True):
    if full:
        df = pl.read_csv("test/data/full_test.csv")
    else:
        df = pl.read_csv("test/data/test.csv")

    df = df.select(
        pl.col("Date").cast(date).alias("date"), pl.col("Adj Close").alias("NVDA")
    )

    if clean:
        df = utils.convert_to_percentage(df)

    return df


@pytest.mark.skip
def test_clean_df():
    # load and clean data
    df = load_test_df()
    df = utils.clean_df(df)

    # test percent_chg
    assert "percent_chg" in df

    correct_val = (3.000000 - 3.510000) / 3.510000
    assert np.isclose(df["percent_chg"].iloc[0], correct_val)

    # test date
    assert type(df["Date"].iloc[0]) is date


def test_convert_to_percentage():
    df = load_test_df(clean=False)

    percent_df = utils.convert_to_percentage(df)

    assert type(percent_df) == pl.DataFrame

    assert percent_df.null_count().sum_horizontal()[0] == 0

    assert percent_df.columns == ["date", "NVDA"]

    assert np.isclose(percent_df["NVDA"][0], -0.14529914529914525)


def test_generate_pattern_from_date():
    # load and clean data
    df = load_test_df()

    initial_date = date.fromisoformat("2023-05-03")
    dates = df["date"]
    pattern = utils.generate_pattern_from_date(initial_date, dates)

    # test output
    correct_pattern = [
        date.fromisoformat(x)
        for x in ["2023-05-03", "2023-08-03", "2023-11-03", "2024-02-05"]
    ]
    assert pattern == correct_pattern


def test_generate_possible_patterns():
    # load and clean data
    df = load_test_df()
    dates = df["date"]

    possible_patterns = utils.generate_possible_patterns(dates)

    # test output
    assert type(possible_patterns) == list

    correct_first_pattern = [
        date.fromisoformat(x)
        for x in ["2023-05-03", "2023-08-03", "2023-11-03", "2024-02-05"]
    ]
    assert possible_patterns[0] == correct_first_pattern

    correct_last_pattern = [date.fromisoformat("2024-05-02")]
    assert possible_patterns[-1] == correct_last_pattern

    assert len(possible_patterns) == 366


def test_summarize_pattern():
    # setup
    df = load_test_df()
    df = df.select("date", pl.col("NVDA").alias("value"))

    pattern = [
        date.fromisoformat(x)
        for x in ["2023-05-03", "2023-08-03", "2023-11-03", "2024-02-05"]
    ]

    days_decreased, mean, stdev = utils.summarize_pattern(pattern, df)

    assert days_decreased == 2
    assert np.isclose(mean, -0.0365305)
    assert np.isclose(stdev, 0.06466027494721935)


def test_summarize_pattern_next_day():
    # setup
    df = load_test_df()
    df = df.select("date", pl.col("NVDA").alias("value"))

    pattern = [
        date.fromisoformat(x)
        for x in ["2023-05-03", "2023-08-03", "2023-11-03", "2024-02-05"]
    ]

    days_decreased, mean, stdev = utils.summarize_pattern_next_day(pattern, df)

    assert days_decreased == 2
    assert np.isclose(mean, 0.00632875275090846)
    assert np.isclose(stdev, 0.03385370464431046)


def test_evaluate_pattern():
    # setup
    df = load_test_df(full=True)
    df = df.select("date", pl.col("NVDA").alias("value"))
    pattern = [
        date(2021, 2, 16),
        date(2021, 5, 17),
        date(2021, 8, 16),
        date(2021, 11, 16),
        date(2022, 2, 16),
        date(2022, 5, 16),
        date(2022, 8, 16),
        date(2022, 11, 16),
        date(2023, 2, 16),
        date(2023, 5, 16),
        date(2023, 8, 16),
        date(2023, 11, 16),
        date(2024, 2, 16),
    ]

    result = utils.evaluate_pattern(pattern, df)

    assert type(result) == bool
    assert result


def test_find_good_patterns():
    # load and clean data
    df = load_test_df(full=True)
    df = df.select("date", pl.col("NVDA").alias("value"))

    # find patterns
    patterns = utils.find_good_patterns(df)

    # test to ensure that the pattern starting on 2-16-2021 is found
    assert any([pattern[0] == date(2021, 2, 16) for pattern in patterns])


def test_prune_patterns():
    patterns = [
        [
            date(2021, 2, 16),
            date(2021, 5, 17),
            date(2021, 8, 16),
            date(2021, 11, 16),
            date(2022, 2, 16),
            date(2022, 5, 16),
            date(2022, 8, 16),
            date(2022, 11, 16),
            date(2023, 2, 16),
            date(2023, 5, 16),
            date(2023, 8, 16),
            date(2023, 11, 16),
            date(2024, 2, 16),
        ],
        [
            date(2021, 2, 18),
            date(2021, 5, 18),
            date(2021, 8, 18),
            date(2021, 11, 18),
            date(2022, 2, 18),
            date(2022, 5, 18),
            date(2022, 8, 18),
            date(2022, 11, 18),
            date(2023, 2, 21),
            date(2023, 5, 18),
            date(2023, 8, 18),
            date(2023, 11, 20),
            date(2024, 2, 20),
        ],
        [
            date(2021, 5, 17),
            date(2021, 8, 16),
            date(2021, 11, 16),
            date(2022, 2, 16),
            date(2022, 5, 16),
            date(2022, 8, 16),
            date(2022, 11, 16),
            date(2023, 2, 16),
            date(2023, 5, 16),
            date(2023, 8, 16),
            date(2023, 11, 16),
            date(2024, 2, 16),
        ],
        [
            date(2021, 5, 18),
            date(2021, 8, 18),
            date(2021, 11, 18),
            date(2022, 2, 18),
            date(2022, 5, 18),
            date(2022, 8, 18),
            date(2022, 11, 18),
            date(2023, 2, 21),
            date(2023, 5, 18),
            date(2023, 8, 18),
            date(2023, 11, 20),
            date(2024, 2, 20),
        ],
        [
            date(2021, 8, 16),
            date(2021, 11, 16),
            date(2022, 2, 16),
            date(2022, 5, 16),
            date(2022, 8, 16),
            date(2022, 11, 16),
            date(2023, 2, 16),
            date(2023, 5, 16),
            date(2023, 8, 16),
            date(2023, 11, 16),
            date(2024, 2, 16),
        ],
        [
            date(2021, 11, 16),
            date(2022, 2, 16),
            date(2022, 5, 16),
            date(2022, 8, 16),
            date(2022, 11, 16),
            date(2023, 2, 16),
            date(2023, 5, 16),
            date(2023, 8, 16),
            date(2023, 11, 16),
            date(2024, 2, 16),
        ],
        [
            date(2022, 2, 16),
            date(2022, 5, 16),
            date(2022, 8, 16),
            date(2022, 11, 16),
            date(2023, 2, 16),
            date(2023, 5, 16),
            date(2023, 8, 16),
            date(2023, 11, 16),
            date(2024, 2, 16),
        ],
        [
            date(2022, 2, 17),
            date(2022, 5, 17),
            date(2022, 8, 17),
            date(2022, 11, 17),
            date(2023, 2, 17),
            date(2023, 5, 17),
            date(2023, 8, 17),
            date(2023, 11, 17),
            date(2024, 2, 20),
        ],
        [
            date(2022, 2, 18),
            date(2022, 5, 18),
            date(2022, 8, 18),
            date(2022, 11, 18),
            date(2023, 2, 21),
            date(2023, 5, 18),
            date(2023, 8, 18),
            date(2023, 11, 20),
            date(2024, 2, 20),
        ],
        [
            date(2022, 5, 16),
            date(2022, 8, 16),
            date(2022, 11, 16),
            date(2023, 2, 16),
            date(2023, 5, 16),
            date(2023, 8, 16),
            date(2023, 11, 16),
            date(2024, 2, 16),
        ],
        [
            date(2022, 5, 17),
            date(2022, 8, 17),
            date(2022, 11, 17),
            date(2023, 2, 17),
            date(2023, 5, 17),
            date(2023, 8, 17),
            date(2023, 11, 17),
            date(2024, 2, 20),
        ],
        [
            date(2022, 5, 18),
            date(2022, 8, 18),
            date(2022, 11, 18),
            date(2023, 2, 21),
            date(2023, 5, 18),
            date(2023, 8, 18),
            date(2023, 11, 20),
            date(2024, 2, 20),
        ],
    ]

    # prune patterns
    pruned_patterns = utils.prune_patterns(patterns)

    # test to ensure that the pattern starting on 2-16-2021 is found
    assert any([pattern[0] == date(2021, 2, 16) for pattern in pruned_patterns])

    # test to ensure no dates are repeated in patterns
    all_dates = []
    for pattern in pruned_patterns:
        all_dates.extend(pattern)
    assert len(set(all_dates)) == len(all_dates)


def test_get_wilshire_tickers():
    tickers = utils.get_wilshire_tickers()

    assert type(tickers) is list
    assert len(tickers) == 3481
    assert tickers[0] == "A"
    assert tickers[-1] == "ZNGA"
