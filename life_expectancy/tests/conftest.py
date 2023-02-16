"""Pytest configuration file"""
import pandas as pd
import pytest

from . import FIXTURES_DIR, OUTPUT_DIR


# @pytest.fixture(autouse=True)
# def run_before_and_after_tests() -> None:
#     """Fixture to execute commands before and after a test is run"""
#     # Setup: fill with any logic you want

#     yield # this is where the testing happens

#     # Teardown : fill with any logic you want
#     file_path = OUTPUT_DIR / "pt_life_expectancy.csv"
#     if file_path.exists():
#         file_path.unlink()


@pytest.fixture(scope="session")
def pt_life_expectancy_expected() -> pd.DataFrame:
    """Fixture to load the expected output of the cleaning script"""
    return pd.read_csv(FIXTURES_DIR / "pt_life_expectancy_sample_expected.csv")

@pytest.fixture()
def sample_data() -> str:
    """Fixture to create a sample of the data"""
    sample_path=OUTPUT_DIR / "sample.tsv"
    if not sample_path.exists():
        df=pd.read_csv(OUTPUT_DIR / "eu_life_expectancy_raw.tsv", sep='\t|,',engine ='python')
        sample=df.sample(frac=0.1,random_state=1)
        sample.to_csv(sample_path,index=False)
    return sample_path
