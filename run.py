from domestique.domestique import Domestique
import os


def run():

    _domestique = Domestique()
    url = input("\nEnter a race URL (copy & paste): ")
    year = input("\nYear to collect rider stats from: ")

    print(f"\n\nAttempting to create stats ...hold tight this could take a few minutes...")

    stats_df = _domestique.main(str(url), str(year))

    csv_name = f"{url.split('/')[-1]}_{str(year)}"

    if not os.path.exists('data'):
        os.makedirs('data')

    stats_df.to_csv(f'data/{csv_name}.csv')

    print(f'\nAll done! \n \nCSV created: data/{csv_name}.csv\n***\n')

    return

if __name__ == '__main__':

    run()
