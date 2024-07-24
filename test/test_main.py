import os
from datetime import date
import pandas as pd

from pattern_detector import main, utils
from test_utils import load_test_df


def test_get_wilshire_tickers():
    tickers = main.get_wilshire_tickers()

    assert type(tickers) == list
    assert len(tickers) == 3481
    assert tickers[0] == "A"
    assert tickers[-1] == "ZNGA"


# contents of test_image.py
def test_log_pattern():
    # create temporary filepath for testing
    tmp_filepath = os.path.join("data", "good_patterns.csv")
    if os.path.exists(tmp_filepath):
        os.remove(tmp_filepath)
    
    # test parameters
    ticker = "TEST"
    pattern = [
        date.fromisoformat(x)
        for x in ["2023-05-03", "2023-08-03", "2023-11-03", "2024-02-05"]
    ]
    df = load_test_df()
    df = utils.clean_df(df)

    # test log_pattern
    main.log_pattern(ticker, pattern, df, filepath=tmp_filepath)
    main.log_pattern(ticker, pattern, df, filepath=tmp_filepath)
    
    # check output in temp log file
    with open(tmp_filepath, "r") as tmp_file:
        lines = tmp_file.readlines()

    assert type(lines) == list
    assert len(lines) == 2
    assert lines[0] == "TEST;[datetime.date(2023, 5, 3), datetime.date(2023, 8, 3), datetime.date(2023, 11, 3), datetime.date(2024, 2, 5)];2;-0.036530455825662556;0.06466039255725796;2;0.00632875275090846;0.03385370464431046\n"
