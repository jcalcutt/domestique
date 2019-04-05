class ScraperConstants:
    """The scraper relies on webpages and html attributes in an exact format
    - These are laid out here"""

    def __init__(self):

        self.BC_STARLIST_PAGE_URL = "https://www.britishcycling.org.uk/events_version_2/ajax_race_entrants_dialog?race_id="
        self.BC_POINTS_PAGE_URL = "https://www.britishcycling.org.uk/points?person_id={}&year={}&d=4"
        self.EVENT_PAGE_RACE_ID_NAME = "a"
        self.EVENT_PAGE_RACE_ATTR_KEY = "class"
        self.EVENT_PAGE_RACE_ATTR_VALUE = "load_race_entrants button button--small button--secondary"
        self.EVENT_PAGE_RACE_ATTR_TAG = "data-race-id"
