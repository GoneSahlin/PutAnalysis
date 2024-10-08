import pytest

from pattern_detector import collect


def test_get_download_link():
    ticker = "NVDA"
    link = collect.get_download_link(ticker)

    correct_link = (
        "https://query1.finance.yahoo.com/v7/finance/download/NVDA?period1"
        "=1&period2=9999999999&interval=1d&events=history&"
        "includeAdjustedClose=true"
    )
    assert link == correct_link


@pytest.mark.xfail
def test_get_data_from_download_link():
    link = (
        "https://query1.finance.yahoo.com/v7/finance/download/NVDA?period1"
        "=1721170601&period2=1721602520&interval=1d&events=history&"
        "includeAdjustedClose=true"
    )

    data = collect.get_data_from_download_link(link)

    # compare with downloaded data
    with open("test/data/test_get_data.csv", "r") as infile:
        correct_data = infile.read()

        assert data == correct_data


def test_get_data():
    df = collect.get_data("NVDA")

    assert not df.empty
    assert df.columns.to_list() == ["timestamp", "adjclose"]
    assert not df.isnull().any().any()  # no null values in any columns
