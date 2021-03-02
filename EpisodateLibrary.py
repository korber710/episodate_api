##########################################################################
#
#   Episodate API
#   developed by Steve Korber
#   korbersa@outlook.com
#
##########################################################################

# import libraries
import urllib.parse as urlparse
from urllib.parse import urlencode
import requests

# helper functions

def get_season_episodes(show, season):
    """
    Creates a list of episode objects from show details.

    Parameters
    ----------
    show : dict
        Return from TV Search Controller
    season : int
        Season to return

    Returns
    -------
    season_list: list
        List of dict objects
    """

    # initialize season list
    season_list = []

    # loop through and form list from episodes
    # that match the season param
    for episodes in show["episodes"]:
        if episodes["season"] == season:
            season_list.append(episodes)

    # return new list
    return season_list

def get_season_numbers(show):
    """
    Creates a list of season numbers from show details.

    Parameters
    ----------
    show : dict
        Return from TV Search Controller

    Returns
    -------
    season_list: list
        List of season numbers
    """

    # initialize season list
    season_list = []

    # form season list by looping though episodes
    # and add if not in list
    for episodes in show["episodes"]:
        if not episodes["season"] in season_list:
            season_list.append(episodes["season"])

    # return new list
    return season_list

"""
    A class to lookup tv shows and get airdates.

    ...

    Attributes
    ----------
    base_url_search : str
        Base url for searching on episodate
    base_url_lookup : str
        Base url for lookup on episodate
        
    Methods
    -------
    search(name, page=None):
        Returns the shows from search to Episodate
    lookup(id):
        Returns the show details from Episodate
    """
class TVSearchController:
    """
        Constructs all the necessary attributes for the tv search object.

        Parameters
        ----------
            none
        """
    def __init__(self):
        self.base_url_search = "https://www.episodate.com/api/search?"
        self.base_url_lookup = "https://www.episodate.com/api/show-details?"

    def search(self, name, page=None):
        """
        Lookup the given name on episodate.

        If the argument 'page' is passed, then it will use a different lookup page.

        Parameters
        ----------
        name : str
            Name of the show to search
        page : int, optional
            Page to use in search (default is 1)

        Returns
        -------
        return_object : dict
            Dictionary containing information about each show
        """

        # setup response obj
        returnObj = {
            "result": -1,
            "description": "",
            "data": ""
        }

        # create dict from given parameters to be converted into url
        params = {"q": name}
        if page: params["page"] = page

        # form url for request
        url_parts = list(urlparse.urlparse(self.base_url_search))
        query = dict(urlparse.parse_qsl(url_parts[4]))
        query.update(params)
        url_parts[4] = urlencode(query, quote_via=urlparse.quote)

        # send request
        try:
            request_url = urlparse.urlunparse(url_parts)
            response = requests.get(request_url)
        except:
            returnObj["result"] = -1
            returnObj["description"] = "search:: requests error"
            return returnObj

        # check response status code
        if response.status_code != 200:
            returnObj["result"] = -1
            returnObj["description"] = "search:: http status code error"
            return returnObj

        # return json from request
        returnObj["result"] = 0
        returnObj["description"] = "search successful"
        returnObj["data"] = response.json()
        return returnObj

    def lookup(self, id):
        """
        Lookup specific id or name of show on episodate and get details.

        Parameters
        ----------
        id : str
            ID or name of show on episodate

        Returns
        -------
        return_object : dict
            Dictionary containing information about the show
        """
        
        # setup response obj
        returnObj = {
            "result": -1,
            "description": "",
            "data": ""
        }

        # create dict from given parameters to be converted into url
        params = {"q": id}

        # form url for request
        url_parts = list(urlparse.urlparse(self.base_url_lookup))
        query = dict(urlparse.parse_qsl(url_parts[4]))
        query.update(params)
        url_parts[4] = urlencode(query, quote_via=urlparse.quote)

        # send request
        try:
            request_url = urlparse.urlunparse(url_parts)
            response = requests.get(request_url)
        except:
            returnObj["result"] = -1
            returnObj["description"] = "lookup:: requests error"
            return returnObj

        # check response status code
        if response.status_code != 200:
            returnObj["result"] = -1
            returnObj["description"] = "lookup:: http status code error"
            return returnObj

        # return json from request
        returnObj["result"] = 0
        returnObj["description"] = "lookup successful"
        returnObj["data"] = response.json()
        return returnObj

# main - example of usage
if __name__ == "__main__":
    import json
    import difflib

    # setup controller
    test_obj = TVSearchController()
    
    # test search
    search_term = "Big Brother Canada"
    x = test_obj.search(search_term)

    show_obj = x["data"]
    show_list = []

    for show in show_obj["tv_shows"]:
        show_list.append(show["name"])

    best_show = difflib.get_close_matches(search_term, show_list)[0]
    show_index = show_list.index(best_show)

    # test lookup
    x = test_obj.lookup(show_obj["tv_shows"][show_index]["id"])
    show_details = x["data"]["tvShow"]

    # get seasons available
    season_list = get_season_numbers(show_details)
    print(f"seasons: {season_list}")

    # get seasons 9
    season_list = get_season_episodes(show_details, 9)
    print(season_list)