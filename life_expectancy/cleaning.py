import argparse
from abc import ABC, abstractmethod
import pandas as pd
from life_expectancy.i_o import load_data, save_data
from life_expectancy.countries import Country

class FileCleaner(ABC):
    """
    Abstract class for reading different types of files
    """
    ext=''
    @abstractmethod
    def clean_data(self, df: pd.DataFrame):
        """
        Abstract method for reading different types of files
        """
        pass

class TsvFileReadClean(FileCleaner):
    """
    Class to clean tsv files that inherits from the FileCleaner abstract class
    """
    ext='tsv'
    def clean_data(self, df):
        df=pd.melt(df, id_vars=df.columns[0:4], value_vars=df.columns[4:], var_name='year')
        df.rename(columns={'geo\\time':'region'},inplace=True)
        df = df.astype({"year": int})
        df.value = df.value.str.extract(r"(\d+\.\d+)") #clean value column using a regex operator that only accepts strings with a float like format 00.0
        df.dropna(inplace=True)
        df = df.astype({"value": float})
        return df

class ZippedJsonReadClean(FileCleaner):
    """
    Class to clean zipped json files that inherits from the FileCleaner abstract class
    """
    ext='zip'
    def clean_data(self, df):
        df.rename(columns={'life_expectancy':'value'},inplace=True)
        df.drop(['flag','flag_detail'],inplace=True)
        df.dropna(inplace=True)
        return df

def clean_data(df: pd.DataFrame, ext: str='tsv'):
    """
    Function to clean the raw data from eu life expectancy

    :param df: Pandas df with the raw data
    :return df: Returns a clean pandas df
    """
    if ext=='tsv':
        cleaner=TsvFileReadClean()
    elif ext=='zip':
        cleaner=ZippedJsonReadClean()
    df=cleaner.clean_data(df)
    return df

def main(region: str = 'PT', path: str ='./life_expectancy/data/eu_life_expectancy_raw.tsv'):
    """
    Calls all the functions to load, clean and save the data from life expectancy

    :param region: Optional region string parameter that defaults into 'PT'
    """
    # pylint: disable=redefined-outer-name
    ext=path.split('.')[-1]
    raw_df=load_data(path)
    clean_df=clean_data(raw_df,ext)

    country=Country(region)
    clean_df_region=save_data(clean_df,country)
    return clean_df_region

if __name__ == "__main__":  # pragma: no cover
    parser = argparse.ArgumentParser(description='Input processing.')
    parser.add_argument('path', metavar='path', \
            type=str, nargs='?',help='path to input file',default='./life_expectancy/data/eu_life_expectancy_raw.tsv')
    parser.add_argument('region', metavar='region', \
            type=str, nargs='?',help='region string (example for Portugal: \'PT\')',default='PT')
    args = parser.parse_args()
    main(region=args.region,path=args.path)
