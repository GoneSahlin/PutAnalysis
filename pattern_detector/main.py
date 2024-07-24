import pandas as pd
from io import StringIO

import collect
import utils


def main():
    # collect data
    link = collect.get_download_link("NVDA")
    data_str = collect.get_data(link)

    # format as df
    string_io = StringIO(data_str)
    df = pd.read_csv(string_io)

    # clean df
    df = utils.clean_df(df)

    # find good patterns
    patterns = utils.find_good_patterns(df)

    print(patterns)

    print(utils.summarize_pattern(patterns[0], df))
    print(utils.summarize_pattern_next_day(patterns[0], df))


if __name__ == "__main__":
    main()
