import argparse
import pandas as pd

def clean_data(region='PT'):
    """Function to clean raw data eu life expectancy and write to csv portugal specific data"""
    df=pd.read_csv('./life_expectancy/data/eu_life_expectancy_raw.tsv', sep='\t|,',engine ='python')
    df=pd.melt(df, id_vars=df.columns[0:4], value_vars=df.columns[4:], var_name='year')
    df.rename(columns={'geo\\time':'region'},inplace=True)
    df = df.astype({"year": int})
    df.value = df.value.str.extract(r"(\d+\.\d+)")
    df.dropna(inplace=True)
    df = df.astype({"value": float})

    portugal=df[df.region==region]
    portugal.to_csv('./life_expectancy/data/pt_life_expectancy.csv',index=False)

if __name__ == "__main__":  # pragma: no cover
    parser = argparse.ArgumentParser(description='Region input processing.')
    parser.add_argument('region', metavar='region', \
            type=str, nargs='?',help='region string',default='PT')
    args = parser.parse_args()
    clean_data(args.region)
