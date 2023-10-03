import sys
sys.path.append(
    "/Users/itech88/Desktop/Projects/Palmdale/Python/revolution_report_transform/"
)
from transform_data_add_col import transform_data_add_col as tdac
import numpy as np
import pandas as pd
import pytest
from unittest.mock import mock_open, patch
from icecream import ic, install
install() # this installs ic project wise to other modules

read_data_values = ['test_column', 'value_for_column']

def side_effect(arg):
    return mock_open(read_data=read_data_values.pop(0))()

with patch("builtins.open", side_effect):
    df = pd.DataFrame({"A": [1, 2], "B": [3, 4]})
    transformed_df = tdac(df)


# def test_transform_data_add_col():
#     pass



def test_column_addition_with_value():

    # Mock data for column name and value
    mock_new_col_name = mock_open(read_data='test_column')
    mock_new_col_value = mock_open(read_data='value_for_column')

    # Mock the reading of the files
    with patch("builtins.open", mock_new_col_name):
        with patch("builtins.open", mock_new_col_value):
            df = pd.DataFrame({"A": [1, 2], "B": [3, 4]})
            transformed_df = tdac(df)


    # Assert column was added
    assert "test_column" in transformed_df.columns

    # Assert values in new column are correct
    assert transformed_df["test_column"].tolist() == ["value_for_column", "value_for_column"]
