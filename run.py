from domestique.domestique import Domestique
from domestique.util.utils import save_df


def run():

    _domestique = Domestique()
    url = str(input("\nEnter a race URL (copy & paste): "))
    year = str(input("\nYear to collect rider stats from: "))

    print(f"\n\nAttempting to create stats ...hold tight this could take a few minutes...")

    stats_df = _domestique.main(url, year)

    save_df(stats_df, url, year)

    print(f'\nAll done! \n \nCSV created in the data directory\n***\n')

    return

if __name__ == '__main__':

    run()
