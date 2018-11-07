import pandas as pd


def approx_left_join(left, right, left_join_col, right_join_col):
    """
    Approximate left join.

    This function joins two Pandas DataFrames on two columns whose values
    do not always overlap. The way they are joined is approximate and is
    based on the closeness of the values in the columns where the join
    happens.

    The joining is executed by finding the closest value of the joining
    column of the left DataFrame that precedes the value of the joining
    column of the right DataFrame.

    If the values are the same, the preceding value of the right DataFrame
    is taken.

    Here is an example where the two following DataFrames are approximately
    joined over the columns A and D:

    Left                Right                 Approximate Left Join
    +---+---+---+---+   +---+---+---+         +---+---+---+---+-----+-----+
    |   | A | B | C |   |   | D | E |         |   | A | B | C |  D  |  E  |
    +---+---+---+---+   +---+---+---+         +---+---+---+---+-----+-----+
    | 0 | 7 | 5 | 1 |   | 0 | 7 | 7 | ----->  | 0 | 7 | 5 | 1 |  4  |  2  |
    | 1 | 8 | 7 | 8 |   | 1 | 9 | 8 |         | 1 | 8 | 7 | 8 |  7  |  7  |
    | 2 | 2 | 9 | 7 |   | 2 | 4 | 2 |         | 2 | 2 | 9 | 7 | NaN | NaN |
    +---+---+---+---+   +---+---+---+         +---+---+---+---+-----+-----+

    The last row of the joined DataFrame has NaNs because there is no value
    in column D of the right DataFrame that is lower than the value in
    column A of the last row of the left DataFrame.

    Parameters
    ----------
    left: pandas.DataFrame
        left data frame
    right: pandas.DataFrame
        right data frame
    left_join_col: str
        column of the left pandas.DataFrame where used for the join
    right_join_col: str
        column of the right pandas.DataFrame where used for the join

    Returns
    -------
    pandas.DataFrame
        Approximate left join Pandas DataFrame

    """

    # Make a copy of the columns over which to join both dataframes
    # and concatenate them.
    left_join = left[[left_join_col]].rename(columns={left_join_col: 'join_col'}).copy()
    right_join = right[[right_join_col]].rename(columns={right_join_col: 'join_col'}).copy()

    left_join['is_right'] = False
    right_join['is_right'] = True

    concat = pd.concat([left_join, right_join])
    del left_join, right_join

    # Sort values according to join_col and is_right.
    # Note that True > False for sorting. So, if join_col
    # has the same value for left and right, right will
    # be placed first.
    concat.sort_values(['join_col', 'is_right'], inplace=True)

    # Write the index of the sorted right dataframe.
    # Taking the sum of the True values of is_right after sorting
    # and subtracting 1, returns the index of the previous row
    # in the left dataframe for all the rows of the concat
    # dataframe.
    concat['right_sorted_index'] = concat.is_right.cumsum() - 1

    # Create the mapping between right and left dataframe indices
    left_right_map = concat[concat.is_right == False].drop(['join_col', 'is_right'], axis=1)
    del concat

    # Sort right dataframe, reset index and make copy
    right_sorted = right.sort_values(right_join_col).reset_index(drop=True)

    # Join right_sorted to left_right_map
    join_to_left = pd.merge(left_right_map,
                            right_sorted,
                            left_on='right_sorted_index',
                            right_index=True).drop('right_sorted_index', axis=1)

    return left.join(join_to_left)
