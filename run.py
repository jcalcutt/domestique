from domestique.domestique import Domestique


def run():

    _domestique = Domestique()
    url = input("Enter a race URL: ")
    print("Attempting to create stats ...hold tight this could take a few minutes...")

    stats_df = _domestique.main(str(url))

    csv_name = url.split('/')[-1]

    stats_df.to_csv(f'data/{csv_name}.csv')

    print(f'\nAll done! \n \nCSV created: data/{csv_name}.csv\n***\n')

    return

if __name__ == '__main__':

    run()