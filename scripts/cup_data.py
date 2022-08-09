import os
import re
from datetime import datetime, timedelta


class CupBase(object):
    MAX_SEASONS = 24


class HellmouthCup(CupBase):
    GOLLYX_START_DATE = "2020-12-09"
    GOLLYX_START_HOUR = "9"
    GOLLYX_MAX_SEASON_LENGTH_HOURS = 96 + 7
    GOLLYX_MAX_SEASON0 = 23
    DPS = 49
    name = "Hellmouth"
    leagues_divisions = {"Cold": ["Fire", "Water"], "Hot": ["Fire", "Water"]}
    post_labels = ['LDS', 'LCS', 'HCS']
    post_series = {
        "LDS": "League Division Series",
        "LCS": "League Championship Series",
        "HCS": "Hellmouth Cup",
    }


class PseudoCup(CupBase):
    GOLLYX_START_DATE = "2021-05-23"
    GOLLYX_START_HOUR = "21"
    GOLLYX_MAX_SEASON_LENGTH_HOURS = 48 + 7
    GOLLYX_MAX_SEASON0 = 23
    DPS = 9
    name = "Pseudo"
    leagues_divisions = {
        "Monterey Bay": ["High", "Low"],
        "San Francisco Bay": ["High", "Low"],
    }
    post_labels = ['LDS', 'LCS', 'HCS']
    post_series = {
        'LDS': "Egalitarian Eight",
        "LCS": "Fortuitous Four",
        "HCS": "Pseudo Cup",
    }


class ToroidalCup(CupBase):
    GOLLYX_START_DATE = "2021-05-27"
    GOLLYX_START_HOUR = "21"
    GOLLYX_MAX_SEASON_LENGTH_HOURS = 72 + 7
    GOLLYX_MAX_SEASON0 = 23
    DPS = 9
    name = "Toroidal"
    leagues_divisions = {"Cold": ["Fire", "Water"], "Hot": ["Fire", "Water"]}
    post_labels = ['LDS', 'LCS', 'HCS']
    post_series = {
        'LDS': "League Division Series",
        "LCS": "League Championship Series",
        "HCS": "Toroidal Cup",
    }


class DragonCup(CupBase):
    GOLLYX_START_DATE = "2021-10-13"
    GOLLYX_START_HOUR = "9"
    GOLLYX_MAX_SEASON_LENGTH_HOURS = 96 + 7
    GOLLYX_MAX_SEASON0 = 23
    DPS = 49
    name = "Dragon"
    leagues_divisions = {
        "Monterey Bay": ["High", "Low"],
        "San Francisco Bay": ["High", "Low"],
    }
    post_labels = ['LDS', 'LCS', 'DCS']
    post_series = {
        'LDS': "League Division Series",
        "LCS": "League Championship Series",
        "DCS": "Dragon Cup",
    }


class RainbowCup(CupBase):
    GOLLYX_START_DATE = "2021-10-11"
    GOLLYX_START_HOUR = "9"
    GOLLYX_MAX_SEASON_LENGTH_HOURS = 48 + 9
    GOLLYX_MAX_SEASON0 = 23
    DPS = 9
    name = "Rainbow"
    leagues_divisions = {
        "Unwest": ["Cold", "South", "Northeast"],
        "West": ["Mountain", "Southwest", "Pacific"],
    }
    post_labels = ['LCS', 'RCS']
    post_series = {
        "LCS": "League Championship Series",
        "RCS": "Rainbow Cup",
    }


class KleinCup(CupBase):
    GOLLYX_START_DATE = "2022-03-28"
    GOLLYX_START_HOUR = "9"
    GOLLYX_MAX_SEASON_LENGTH_HOURS = 48 + 4
    GOLLYX_MAX_SEASON0 = 23
    DPS = 11
    name = "Klein"
    leagues_divisions = {"Cold": ["Fire", "Water"], "Hot": ["Fire", "Water"]}
    post_labels = ['LDS', 'LCS', 'KCS']
    post_series = {
        "LDS": "League Division Series",
        "LCS": "League Championship Series",
        "KCS": "Klein Cup",
    }


class StarCup(CupBase):
    GOLLYX_START_DATE = "2022-04-01"
    GOLLYX_START_HOUR = "9"
    GOLLYX_MAX_SEASON_LENGTH_HOURS = 48 + 4
    GOLLYX_MAX_SEASON0 = 23
    DPS = 11
    name = "Star"
    leagues_divisions = {
        "Monterey Bay": ["High", "Low"],
        "San Francisco Bay": ["High", "Low"],
    }
    post_labels = ['LDS', 'LCS', 'SCS']
    post_series = {
        "LDS": "League Division Series",
        "LCS": "League Championship Series",
        "SCS": "Star Cup",
    }
