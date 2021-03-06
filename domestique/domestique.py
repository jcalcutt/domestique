import pandas as pd
from domestique.scraper import DomestiqueScraper


class Domestique:

    _domestique_scraper = DomestiqueScraper()

    def __init__(self):
        pass

    def main(self, race_url, year):
        """Do the magic!

        Get person_id url for each rider - their 'points page'
        For each person_id url, extract data from their 'points table' and create some summary statistics from this,
        such as; points per race or number of top 10 finishes.

        :return df_final: pandas DataFrame of rider stats
        """

        rider_field = Domestique._domestique_scraper.get_data(race_url, year)

        summary_lst = []
        for rider in rider_field.field:

            summary_lst.append(Domestique.create_summary_stats(rider.name, rider.club, rider.points_df))

        df_final = pd.DataFrame(summary_lst, columns=['Name', 'Club', 'Races', 'Total Points', 'Points per Race',
                                                      'Top 10 Count', 'Wins'])

        return df_final

    @staticmethod
    def create_summary_stats(person, club, points_df):
        """From each rider points DataFrame create summary stats i.e. average points per race, number of wins etc.

        :param person: string, rider name
        :param club: string, rider club
        :param points_df: DataFrame, rider points table
        :return stat_lst: list of summary stats
        """

        num_races = len(points_df)

        try:
            total_points = points_df.Points.sum()
            points_per_race = round(total_points / num_races, 2)
            top_tens = points_df[(points_df.Position < 10) & (points_df.Position > 0)]['Position'].count()
            wins = points_df[(points_df.Position == 1)]['Position'].count()
        except (AttributeError, ZeroDivisionError):
            total_points = 0
            points_per_race = 0
            top_tens = 0
            wins = 0

        # create list with all metrics
        stat_lst = [person, club, num_races, total_points, points_per_race, top_tens, wins]

        return stat_lst
