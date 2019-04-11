import os


def save_df(df, url, year):

    csv_name = f"{url.split('/')[-1]}_{year}"

    if not os.path.exists('data'):
        os.makedirs('data')

    df.to_csv(f'data/{csv_name}.csv')
