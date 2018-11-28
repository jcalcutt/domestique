import requests
from bs4 import BeautifulSoup
import pandas as pd
import numpy as np


class DomestiqueScraper:

    def __init__(self, bc_race_url):

        self.bc_race_url = bc_race_url
        self.startlist_base_url = "https://www.britishcycling.org.uk/events_version_2/ajax_race_entrants_dialog?race_id="
        self.points_url = "https://www.britishcycling.org.uk/points?person_id={}&year=2018&d=4"
        self.rider_data ={}


    def get_data(self):

        # from event page url, create dictionary with keys for each rider
        # rider_data[rider]['info'] = [name, cat, club]


        rider_df = self.get_rider_urls()

        # format df
        rider_df['id_lst'] = rider_df['name_href'].str.split('person_id=', expand=True)[1].str.split('&', expand=False)
        rider_df['name_id'] = rider_df['id_lst'].apply(lambda x: DomestiqueScraper.get_id(x))

        # create dictionary for each rider
        for index, row in rider_df.iterrows():

            rider = row['name']
            self.rider_data[rider] = {}
            if row['id']:
                rider_id = str(row['id'])
                self.rider_data[rider]['points_df'] = self.get_data_from_points_page(rider_id)




    def get_rider_urls(self):
        """
        from event url create dataframe of riders and their points page url
        :return:
        """

        events_response = requests.get(self.bc_race_url)
        event_soup = BeautifulSoup(events_response.content, 'html.parser')

        # obtain race id
        race_id = event_soup.find('a', attrs={"class": "load_race_entrants button button--small button--secondary"})[
            'data-race-id']

        # get the startlist page and convert to a list
        startlist_page = requests.get(self.startlist_base_url + race_id)

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


    def get_data_from_points_page(self, rider_id):
        """retrieve rider points page as a dataframe

        :param rider_id: string
        :return: pandas df
        """

        points_page = requests.get(self.points_url.format(rider_id))

        points_df = pd.read_html(points_page.content)[0]

        return points_df


    @staticmethod
    def get_id(lst):
        if type(lst) == type(list()):
            x = lst[0]
        else:
            x = np.NaN
        return x
