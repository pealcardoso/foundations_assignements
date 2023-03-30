from abc import ABC, abstractmethod
import zipfile
import pandas as pd
from life_expectancy.countries import Country

class FileReader(ABC):
    """
    Abstract class for reading different types of files
    """
    ext=''
    @abstractmethod
    def read_file(self, file_path):
        """
        Abstract method for reading different types of files
        """
        pass

class TsvFileReader(FileReader):
    """
    Class to read tsv files that inherits from the FileReader abstract class
    """
    def read_file(self, file_path: str) -> pd.DataFrame:
        # code to read CSV file
        df=pd.read_csv(file_path, sep='\t|,',engine ='python')
        return df

class ZippedJsonFileReader(FileReader):
    """
    Class to read zipped json files that inherits from the FileReader abstract class
    """
    def read_file(self, file_path: str) -> pd.DataFrame:
        # code to read zipped JSON file
        with zipfile.ZipFile(file_path) as zip_file:
            json_file_name = None
            for name in zip_file.namelist():
                if name.endswith('.json'):
                    json_file_name = name
                    break

            if json_file_name:
                with zip_file.open(json_file_name) as json_file:
                    df=pd.read_json(json_file)
        return df

def save_data(df:pd.DataFrame, country: Country) -> pd.DataFrame:
    """
    Function to save the cleaned data from life expectancy for a specific region

    :param df: Pandas df with the raw data
    :param country: Country enum object
    :return df_filter_by_region: Returns the same Pandas df that was saved, with the region filter applyed
    """
    df_filter_by_region=df[df.region==country.value]
    df_filter_by_region.to_csv('./life_expectancy/data/pt_life_expectancy.csv',index=False)
    return df_filter_by_region.reset_index(drop=True)
