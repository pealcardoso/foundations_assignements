import pandas as pd

def load_data(path):
    """
    Function to load the raw data from eu life expectancy

    :return df: Returns pandas df with the raw data
    """
    df=pd.read_csv(path, sep='\t|,',engine ='python')
    return df

def save_data(df,region):
    """
    Function to save the cleaned data from life expectancy for a specific region

    :param df: Pandas df with the raw data
    :param region: Region string to filter by
    """
    df_filter_by_region=df[df.region==region]
    df_filter_by_region.to_csv('./life_expectancy/data/pt_life_expectancy.csv',index=False)
    return df_filter_by_region.reset_index(drop=True)
