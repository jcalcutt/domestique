import requests
from bs4 import BeautifulSoup
import time
import pandas as pd

# input -


class DomestiqueScraper:

    def __init__(self, bc_race_url):

        self.bc_race_url = bc_race_url

    def get_rider_points_data(self):


