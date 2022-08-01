import os, sys, json, time


cups = ['hellmouth', 'pseudo', 'toroidal', 'rainbow', 'dragon', 'star', 'klein']


class SimulatorInput(object):
    """
    This is a high-level input class.

    It points to the location of the data,
    and which season to extract.

    It is used by the batch manager classes to
    get the data directory, to get regular season
    or postseason data, and to extract a list of all
    game IDs from regular season and/or postseason.
    """
    def __init__(self, pkg_root, cup, season0):
        """
        Do some validation of the input parameters, and store them
        """

        if os.path.exists(pkg_root):
            self.pkg_root = pkg_root
        else:
            raise FileNotFoundError(f"could not find specified root directory where pkg/ is located: {pkg_root}")

        cup = cup.lower()
        if cup in valid_cups:
            self.cup = cup
        else:
            raise ValueError(f"could not find cup {cup}, try one of {', '.join(valid_cups)}")

        if season0 >= 0:
            self.season0 = season0
        else:
            raise ValueError(f"season must not be a negative number")

    def get_data_path(self):
        """
        Use the pkg root provided to the constructor to find the path
        to the data directory for season0
        """
        datadir = os.path.join(pkg_root, "data", f"gollyx-{self.cup}-data", f"season{self.season0}")
        if not os.path.exists(datadir):
            raise FileNotFoundError(f"could not find data directory: {datadir}")
        return datadir

    def get_season_data(self):
        datadir = self.get_data_path()
        season_json = os.path.join(datadir, "season.json")
        if not os.path.exists(season_json):
            raise FileNotFoundError(f"could not find season data json: {season_json}")
        with open(season_json, 'r') as f:
            season = json.load(season_json)
        return season

    def get_postseason_data(self):
        """
        Return a sorted list of postseason game IDs for season0
        """
        datadir = self.get_data_path()
        post_json = os.path.join(datadir, "postseason.json")
        if not os.path.exists(post_json):
            raise FileNotFoundError(f"could not find postseason data json: {post_json}")
        with open(post_json, 'r') as f:
            post = json.load(post_json)
        return post

    def get_all_data(self):
        return (self.get_season_data(), self.get_postseason_data())

    def get_regular_season_gameids():
        """
        Return a sorted list of regular season game IDs for season0
        """
        season = self.get_season_data()
        gameids = set()
        for day in season:
            for game in day:
                if 'id' in game.keys():
                    gameid = game['id']
                elif 'gameid' in game.keys():
                    gameid = game['gameid']
                else:
                    print("Game data is missing id or gameid field")
                gameids.add(gameid)
        return sorted(list(gameids))

    def get_postseason_gameids():
        post = self.get_postseason_data()
        gameids = set()
        for label in post:
            miniseason = post[label]
            for day in miniseason:
                for game in day:
                    if 'id' in game.keys():
                        gameid = game['id']
                    elif 'gameid' in game.keys():
                        gameid = game['gameid']
                    else:
                        print("Game data is missing id or gameid field")
                    gameids.add(gameid)
        return sorted(list(gameids))

    def get_all_gameids():
        """
        Return a sorted list of all game IDs for season0,
        regular season and postseason.
        """
        r = self.get_regular_season_gameids()
        p = self.get_postseason_gameids()
        return sorted(r + p)

