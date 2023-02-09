"""Tests for the cleaning module"""
import pandas as pd
from life_expectancy.cleaning import main,save_data
from . import OUTPUT_DIR
import life_expectancy.cleaning  
import unittest
from unittest.mock import patch 

     
@patch('life_expectancy.cleaning.pd.DataFrame.to_csv',return_value=None)
def test_save(mock):
    mock.side_effect = print(
      "Output not saved to file, because it is a test."    )
    #self.assertTrue(life_expectancy.cleaning.pd.DataFrame.to_csv().called)



def test_clean_data(pt_life_expectancy_expected,sample_data):
    """Run the `main` function from cleaning.py and compare the output to the expected output"""
    df=main(path=sample_data)
    # pt_life_expectancy_actual = pd.read_csv(
    #     OUTPUT_DIR / "pt_life_expectancy.csv"
    # )
    print(pt_life_expectancy_expected)
    pd.testing.assert_frame_equal(
        df, pt_life_expectancy_expected
    )
