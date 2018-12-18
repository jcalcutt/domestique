import pandas as pd
from scraper import DomestiqueScraper

race_url = "https://www.britishcycling.org.uk/events/details/173396/Crits-at-the-Park--9"


def main():
    """Do the magic!

    Get person_id url for each rider - their 'points page'
    For each person_id url, extract data from their 'points table' and create some summary statistics from this,
    such as; points per race or number of top 10 finishes. Export to CSV

    :return summary_stats.csv:
    """
    _domestique_scraper = DomestiqueScraper()

    _domestique_scraper.get_data(race_url)

    summary_lst = []
    for key, value in _domestique_scraper.rider_data.items():

        summary_lst.append(create_summary_stats(key, _domestique_scraper.rider_data[key]['points_df']))


    df_final = pd.DataFrame(summary_lst, columns=['Name', 'Races', 'Total Points', 'Points per Race', 'Top 10 Count',
                                                  'Wins'])

    df_final.to_csv('test.csv')  # TODO - prompt for name of output file, or dynamic

    print('All Done! Summary CSV created')
    return

def create_summary_stats(person, points_df):

    num_races = len(points_df)
    total_points = points_df.Points.sum()
    try:
        points_per_race = round(total_points / num_races, 2)
        top_tens = points_df[(points_df.Position < 10) & (points_df.Position > 0)]['Position'].count()
        wins = points_df[(points_df.Position == 1)]['Position'].count()
    except:
        points_per_race = 0
        top_tens = 0
        wins = 0

    # create list with all metrics
    stat_lst = [person, num_races, total_points, points_per_race, top_tens, wins]

    return stat_lst


if __name__ == '__main__':

    main()