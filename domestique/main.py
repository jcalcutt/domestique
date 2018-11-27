import pandas as pd
from scraper import DomestiqueScraper
import outline

STARTLIST = "../data/input/cyclopark_2.txt"
START_DF = pd.read_csv(STARTLIST, header=None, names=['name', 'club'])

_domestique_scraper = DomestiqueScraper

def main():
    """Do the magic!

    Get person_id url for each rider - their 'points page'
    For each person_id url, extract data from their 'points table' and create some summary statistics from this,
    such as; points per race or number of top 10 finishes. Export to CSV

    :return summary_stats.csv:
    """

    id_lst = _domestique_scraper.get_person_id(START_DF)

    summary_lst = []
    for rider_club_url in id_lst:
        summary_lst.append(outline.create_summary_stats(rider_club_url))

        # wait 5 seconds before making the next request in the create_summary_stats function
        time.sleep(5)

    df_final = pd.DataFrame(summary_lst, columns=['Name', 'Club', 'Races', 'Total Points', 'Points per Race',
                                                  'Top 10 Count', 'Wins'])
    df_final.to_csv('cyclopark_2_summary_stats.csv')  # TODO - prompt for name of output file, or dynamic

    print('All Done! Summary CSV created')
    return


if __name__ == '__main__':

    sys.exit(main())