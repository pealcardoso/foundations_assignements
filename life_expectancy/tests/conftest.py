"""Pytest configuration file"""
import pandas as pd
import pytest

from . import FIXTURES_DIR, OUTPUT_DIR

@pytest.fixture(scope="session")
def pt_life_expectancy_expected() -> pd.DataFrame:
    """Fixture to load the expected output of the cleaning script"""
    return pd.read_csv(FIXTURES_DIR / "pt_life_expectancy_sample_expected.csv")

@pytest.fixture()
def sample_data():
    """Fixture to create a sample of the data"""
    sample_path=OUTPUT_DIR / "sample.tsv"
    if not sample_path.exists():
        df=pd.read_csv(OUTPUT_DIR / "eu_life_expectancy_raw.tsv", sep='\t|,',engine ='python')
        sample=df.sample(frac=0.1,random_state=1)
        sample.to_csv(sample_path,index=False)
    return sample_path.as_posix()
