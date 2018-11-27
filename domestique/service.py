import requests
from bs4 import BeautifulSoup
import pandas as pd
import sys
import time


# TODO - get person_id url from another method, i.e. selenium. Currently semi-manual, creating a 'copy & paste' csv


def create_summary_stats(person_club_url):
    """Create a dataframe of summary metrics for each rider

    :param person_club_url: list, 3 item list containing strings: rider name, club, perons_id url
    :return stat_lst: list, containing rider name, club and some of their summary statistics of their current season
    """
    # TODO - split this up into two functions: one to turn their points table into a dataframe, the other to compute
    # metrics from this
    points_page = requests.get('{}{}'.format(base_url, person_club_url[2]))
    points_soup = BeautifulSoup(points_page.text, 'html.parser')
    points_lst = points_soup.find_all('td')

    # extract info from 'table' (points_lst) on the riders points page, essentially convert this into a dataframe
    date = []
    cat = []
    race = []
    pos = []
    points = []
    i = 0
    while i < len(points_lst) - 5:
        date.append(points_lst[i].text)
        cat.append(points_lst[i + 1].text)
        race.append(points_lst[i + 2].text)
        pos.append(points_lst[i + 3].text)
        points.append(points_lst[i + 4].text)
        i += 5

    points_df = pd.DataFrame({'date': date, 'cat': cat, 'race': race, 'pos': pos, 'points': points})
    points_df[['points', 'pos']] = points_df[['points', 'pos']].apply(pd.to_numeric)

    # rider summary metric calculations, quite self-explanatory
    num_races = len(points_df)
    total_points = points_df.points.sum()
    try:
        points_per_race = round(total_points/num_races, 2)
        top_tens = points_df[(points_df.pos < 10) & (points_df.pos > 0)]['pos'].count()
        wins = points_df[(points_df.pos == 1)]['pos'].count()
    except:
        points_per_race = 0
        top_tens = 0
        wins = 0

    # create list with all metrics
    stat_lst = [person_club_url[0], person_club_url[1], num_races, total_points, points_per_race, top_tens, wins]

    print("Created stats for: {}".format(person_club_url[0]))
    return stat_lst



