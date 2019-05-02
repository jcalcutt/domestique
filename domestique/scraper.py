import requests
from bs4 import BeautifulSoup
import pandas as pd
import numpy as np
import time
from domestique.util.scraper_constants import ScraperConstants
from domestique.util.data_classes import Rider, RaceField

sc = ScraperConstants()


class DomestiqueScraper:

    def __init__(self):
        pass

    def get_data(self, bc_race_url, year):
        """from event page url, create dictionary with keys for each rider, with their points table (DataFrame) and club
        as values

        :param bc_race_url: string
        :param year: string
        :return rider_data: dictionary - keys as rider names, values: club, points table
        """

        rider_df = DomestiqueScraper._get_rider_urls(bc_race_url)

        # format df
        rider_df['id_lst'] = rider_df['name_href'].str.split('person_id=', expand=True)[1].str.split('&', expand=False)
        rider_df['name_id'] = rider_df['id_lst'].apply(lambda x: DomestiqueScraper.get_id(x))

        field = []
        # create rider and race field data class, get points data for each rider
        for index, row in rider_df.iterrows():

            rider = row['name']

            if not pd.isnull(row['name_id']):
                rider_id = str(row['name_id'])
                field.append(Rider(rider, row['club'], DomestiqueScraper._get_data_from_points_page(rider_id, year)))
            else:
                field.append(Rider(rider, 'No Club', pd.DataFrame()))

            # be kind, I've been temporarily banned a few times...
            time.sleep(5)

        return RaceField(field=field)

    @staticmethod
    def _get_rider_urls(bc_race_url):
        """
        from event url create dataframe of riders and their points page url
        :return:
        """

        events_response = requests.get(bc_race_url)
        event_soup = BeautifulSoup(events_response.content, 'html.parser')

        # obtain race id
        race_id = event_soup.find(sc.EVENT_PAGE_RACE_ID_NAME, attrs=sc.EVENT_PAGE_RACE_ATTR)[sc.EVENT_PAGE_RACE_ATTR_TAG]

        # get the startlist page and convert to a list
        startlist_page = requests.get(sc.BC_STARLIST_PAGE_URL + race_id)

        startlist_soup = BeautifulSoup(startlist_page.content, 'html.parser')

        rider_table = startlist_soup.findAll('tr')[1:]
        rider_club_href_lst = []

        for i in range(len(rider_table)):
            rider_name = rider_table[i].findAll('td')[0].text.replace("\n", "")
            rider_club = rider_table[i].findAll('td')[1].text.replace("\n", "")
            try:
                rider_href = rider_table[i].findAll('a')[0]['href']
            except IndexError:
                rider_href = np.NaN

            try:
                club_href = rider_table[i].findAll('a')[1]['href']
            except IndexError:
                club_href = np.NaN

            rider_lst = [rider_name, rider_club, rider_href, club_href]
            rider_club_href_lst.append(rider_lst)

        return pd.DataFrame(rider_club_href_lst, columns=['name', 'club', 'name_href', 'club_href'])

    @staticmethod
    def _get_data_from_points_page(rider_id, year):
        """retrieve rider points page as a dataframe

        :param rider_id: string
        :param year: string
        :return: pandas df
        """
        try:
            points_page = requests.get(sc.BC_POINTS_PAGE_URL.format(rider_id, year))

            points_df = pd.read_html(points_page.content)[0]
            points_df = points_df[:-1]
            points_df.Position = points_df.Position.astype(float)

        except ValueError:
            # if there's no data for a rider for the chosen year, return empty DataFrame
            points_df = pd.DataFrame(columns=['Position', 'Points'])

        return points_df

    @staticmethod
    def get_id(lst):

        if isinstance(lst, list):
            x = lst[0]
        else:
            x = np.NaN
        return x
