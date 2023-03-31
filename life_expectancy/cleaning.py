import argparse
from abc import ABC, abstractmethod
from pathlib import Path
import pandas as pd
from life_expectancy.i_o import save_data, FileReader, TsvFileReader, ZippedJsonFileReader
from life_expectancy.countries import Country

class FileCleaner(ABC):
    """
    Abstract class for reading different types of files
    """
    @abstractmethod
    def clean_data(self, df: pd.DataFrame):
        """
        Abstract method for reading different types of files
        """
        pass

class TsvFileCleaner(FileCleaner):
    """
    Class to clean tsv files that inherits from the FileCleaner abstract class
    """
    def clean_data(self, df: pd.DataFrame) -> pd.DataFrame:
        df=pd.melt(df, id_vars=df.columns[0:4], value_vars=df.columns[4:], var_name='year')
        df.rename(columns={'geo\\time':'region'},inplace=True)
        df = df.astype({"year": int})
        df.value = df.value.str.extract(r"(\d+\.\d+)") #clean value column using a regex operator that only accepts strings with a float like format 00.0
        df.dropna(inplace=True)
        df = df.astype({"value": float})
        return df

class ZippedJsonCleaner(FileCleaner):
    """
    Class to clean zipped json files that inherits from the FileCleaner abstract class
    """
    def clean_data(self, df: pd.DataFrame) -> pd.DataFrame:
        df.rename(columns={'life_expectancy':'value'},inplace=True)
        df.drop(['flag','flag_detail'],inplace=True)
        df.dropna(inplace=True)
        return df

class Strategy:
    """
    Class to chose between readers and cleaners based on type of file
    """
    tsv = (TsvFileReader(), TsvFileCleaner())
    zip = (ZippedJsonFileReader(), ZippedJsonCleaner())

    @classmethod
    def from_file(cls, filepath: Path) -> (FileReader, FileCleaner):
        """
        Get file path, extract the file extension and return the corresponding reader and cleaners
        """
        for member in vars(cls).keys():
            if '.'+member == filepath.suffix:
                return getattr(cls, member)
        raise ValueError(f"No member found with suffix {filepath.suffix}")

def main(region: str = 'PT', path: Path =Path('./life_expectancy/data/eu_life_expectancy_raw.tsv')) -> pd.DataFrame:
    """
    Calls all the functions to load, clean and save the data from life expectancy

    :param region: Optional region string parameter that defaults into 'PT'
    """
    # pylint: disable=redefined-outer-name
    strategy=Strategy()
    reader, cleaner = strategy.from_file(path)
    raw_df=reader.read_file(path)
    clean_df=cleaner.clean_data(raw_df)

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
    main(region=args.region,path=Path(args.path))
