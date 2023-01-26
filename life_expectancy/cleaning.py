import argparse
import pandas as pd

def load_data():
    """
    Function to load the raw data from eu life expectancy

    :return df: Returns pandas df with the raw data
    """
    df=pd.read_csv('./life_expectancy/data/eu_life_expectancy_raw.tsv', sep='\t|,',engine ='python')
    return df

def clean_data(df):
    """
    Function to clean the raw data from eu life expectancy

    :param df: Pandas df with the raw data
    :return df: Returns a clean pandas df
    """
    df=pd.melt(df, id_vars=df.columns[0:4], value_vars=df.columns[4:], var_name='year')
    df.rename(columns={'geo\\time':'region'},inplace=True)
    df = df.astype({"year": int})
    df.value = df.value.str.extract(r"(\d+\.\d+)")  #cleans value column using a regex operator that only accepts strings with a float like format 00.0
    df.dropna(inplace=True)
    df = df.astype({"value": float})
    return df

def save_data(df,region):
    """
    Function to save the cleaned data from life expectancy for a specific region

    :param df: Pandas df with the raw data
    :param region: Region string to filter by
    """
    df_filter_by_region=df[df.region==region]
    df_filter_by_region.to_csv('./life_expectancy/data/pt_life_expectancy.csv',index=False)

def main(region='PT'):
    """
    Calls all the functions to load, clean and save the data from life expectancy

    :param region: Optional region string parameter that defaults into 'PT'
    """
    # pylint: disable=redefined-outer-name
    raw_df=load_data()
    clean_df=clean_data(raw_df)
    save_data(clean_df,region)

if __name__ == "__main__":  # pragma: no cover
    parser = argparse.ArgumentParser(description='Region input processing.')
    parser.add_argument('region', metavar='region', \
            type=str, nargs='?',help='region string (example for Portugal: \'PT\')',default='PT')
    args = parser.parse_args()
    raw_df=load_data()
    clean_df=clean_data(raw_df)
    save_data(clean_df,args.region)
