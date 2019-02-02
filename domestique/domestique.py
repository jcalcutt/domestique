import pandas as pd
import googlemaps
from datetime import datetime
from domestique.scraper import DomestiqueScraper
from domestique.secret import GOOGLE_API_KEY


class Domestique:

    _domestique_scraper = DomestiqueScraper()
    _gmaps = googlemaps.Client(key=GOOGLE_API_KEY)

    def main(self, race_url, year, from_location):
        """Do the magic!

        Get person_id url for each rider - their 'points page'
        For each person_id url, extract data from their 'points table' and create some summary statistics from this,
        such as; points per race or number of top 10 finishes. Export to CSV

        :return summary_stats.csv:
        """

        Domestique._domestique_scraper.get_data(race_url, year)

        summary_lst = []
        for key, value in Domestique._domestique_scraper.rider_data.items():

            summary_lst.append(self.create_summary_stats(key, Domestique._domestique_scraper.rider_data[key]['points_df']))

        df_final = pd.DataFrame(summary_lst, columns=['Name', 'Races', 'Total Points', 'Points per Race',
                                                      'Top 10 Count', 'Wins'])

        self.call_google_maps_api(from_location)

        return df_final

    def create_summary_stats(self, person, points_df):
        """From each rider points DataFrame create summary stats i.e. average points per race, number of wins etc.

        :param person: string, rider name
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
        stat_lst = [person, num_races, total_points, points_per_race, top_tens, wins]

        return stat_lst

    def call_google_maps_api(self, from_location):

        venue = Domestique._domestique_scraper.location
        if venue:

            directions_result = Domestique._gmaps.distance_matrix(origins=from_location, destinations=venue,
                                                                  mode="driving", departure_time=datetime.now())
            # placeholder for now...
            print(f"\n\nLocation data: {directions_result}")

        else:
            print("\nSorry, no distance calculation available")


