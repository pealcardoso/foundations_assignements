"""Tests for the cleaning module"""
from unittest.mock import patch
import pandas as pd
from life_expectancy.cleaning import main
from life_expectancy.i_o import save_data
from life_expectancy.countries import Country

# pylint: disable=assignment-from-no-return
@patch('life_expectancy.i_o.pd.DataFrame.to_csv', return_value=None)
def test_save(mock_to_csv):
    """
    Mock function to patch pandas to_csv method
    """
    def print_message():
        print("Output not saved to file, because it is a test.")
    mock_to_csv.side_effect = print_message()
    df = pd.DataFrame({"region": "PT", "col": [[100]]})
    file_path = './life_expectancy/data/pt_life_expectancy.csv'
    save_data(df, Country('PT'))
    mock_to_csv.assert_called_once_with(file_path, index=False)

@patch('life_expectancy.cleaning.load_data', autospec=True)
def test_load(mock_load_data):
    """
    Mock function to patch and test the load_data function
    """
    def print_message():
        print("Input not loaded, because it is a test.")
    mock_load_data.side_effect = print_message()
    file_path = './life_expectancy/data/sample.tsv'
    mock_load_data.return_value= pd.DataFrame({"region": "PT", "1": "100", "2": "200", "3": "300", "4": "400", "5": "500", "6": "600"},index=[0])
    df=main('PT',file_path)
    #df=load_data(file_path)
    mock_load_data.assert_called_once_with(file_path)
    assert isinstance(df, pd.DataFrame)


def test_clean_data(pt_life_expectancy_expected,sample_data):
    """
    Run the `main` function from cleaning.py and compare the output to the expected output
    """
    df=main(path=sample_data)
    pd.testing.assert_frame_equal(
        df, pt_life_expectancy_expected
    )

def test_list_of_countries():
    """
    Test if the list of countries class method from the enum Country returns the expected result
    """
    expected_countries = [
        'AT', 'BE', 'BG', 'CH', 'CY', 'CZ', 'DK', 'EE', 'EL', 'ES', 'FI', 'FR',
        'HR', 'HU', 'IS', 'IT', 'LI', 'LT', 'LU', 'LV', 'MT', 'NL', 'NO', 'PL',
        'PT', 'RO', 'SE', 'SI', 'SK', 'DE', 'AL', 'IE', 'ME', 'MK', 'RS', 'AM',
        'AZ', 'GE', 'TR', 'UA', 'BY', 'UK', 'XK', 'FX', 'MD', 'SM', 'RU'
    ]
    assert Country.list_of_countries() == expected_countries
