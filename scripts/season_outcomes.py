import os, sys, subprocess, json, time
from pprint import pprint


def main():
    cup = "hellmouth"

    tmpdir = 'tmp'
    if not os.path.exists(tmpdir):
        os.mkdir("tmp")

    for season0 in range(24):
        teams_dat = fetch_teams_data(season0, cup)
        for team_dat in teams_dat:
            team_abbr = team_dat["teamAbbr"]
            result = print_sched_tuples(team_abbr, season0, cup)
            fname = os.path.join("tmp", f"{team_abbr}_{season0+1:02}.txt")
            print(f"Working on {fname}")
            with open(fname, 'w') as f:
                f.write("\n".join(result))


def get_leagues(team_dat):
    leagues = list(set([t["league"] for t in team_dat]))
    return sorted(leagues)


def get_leagues_divisions(team_dat):
    leagues_divs = list(set([(t["league"], t["division"]) for t in team_dat]))
    leagues_divs.sort(key=lambda x: (x[0], x[1]))
    return leagues_divs


def get_league_division_team(team_abbr, team_dat):
    for t in team_dat:
        if t["teamAbbr"] == team_abbr:
            return (t["league"], t["division"])
    return None


def team_name_to_abbr(team_name, team_dat):
    for t in team_dat:
        if t["teamName"].lower() == team_name.lower():
            return t["teamAbbr"]
    return None


def team_abbr_to_name(team_abbr, team_dat):
    for t in team_dat:
        if t["teamAbbr"].upper() == team_abbr.upper():
            return t["teamName"]
    return None


def fetch_season_data(which_season0, cup):
    seas_file = os.path.join(
        "..", "data", f"gollyx-{cup}-data", f"season{which_season0}", "season.json"
    )
    if not os.path.exists(seas_file):
        raise Exception(f"Error: season {which_season0} not valid: {seas_file} does not exist")
    with open(seas_file, "r") as f:
        season0_seas = json.load(f)
    return season0_seas


def filter_season_data(seas_data, team_abbr):
    team_abbr = team_abbr.upper()
    team_seas = []
    for day in seas_data:
        for game in day:
            if game["team1Abbr"] == team_abbr or game["team2Abbr"] == team_abbr:
                team_seas.append(game)
                break
    return team_seas


def schedule_tuples(team_abbr, season0, cup):
    team_abbr = team_abbr.upper()
    dat = filter_season_data(fetch_season_data(season0, cup), team_abbr)
    schedule_tups = []
    for game in dat:
        if "gameid" in game.keys():
            gameid = game["gameid"]
        else:
            gameid = game["id"]
        if game["team1Abbr"] == team_abbr:
            other_team_name = game["team2Name"]
            other_team_abbr = game["team2Abbr"]

            our_points = game["team1Score"]
            other_points = game["team2Score"]

            our_wl = game["team1WinLoss"]
            other_wl = game["team2WinLoss"]

            if game["team2Score"] > game["team1Score"]:
                outcome = "L"
            else:
                outcome = "W"
            homeaway = "H"

        elif game["team2Abbr"] == team_abbr:
            other_team_name = game["team1Name"]
            other_team_abbr = game["team1Abbr"]

            our_points = game["team2Score"]
            other_points = game["team1Score"]

            our_wl = game["team2WinLoss"]
            other_wl = game["team1WinLoss"]

            if game["team1Score"] > game["team2Score"]:
                outcome = "L"
            else:
                outcome = "W"
            homeaway = "A"

        else:
            raise Exception(f"Could not find team {team_abbr} in season {season0}")

        tup = (
            gameid,
            other_team_name,
            other_team_abbr,
            homeaway,
            outcome,
            our_points,
            other_points,
            our_wl,
            other_wl,
        )
        schedule_tups.append(tup)
    return schedule_tups


def print_sched_tuples(team_abbr, season0, cup):
    result = []
    tups = schedule_tuples(team_abbr, season0, cup)
    result.append("")
    result.append(f"Schedule for {team_abbr.upper()}, Season {season0+1}")
    result.append("-" * 40)
    for tup in tups:
        (gameid, oppname, oppabbr, homeaway, outcome, ourpts, theirpts, ourwl, theirwl) = tup
        if homeaway == "H":
            matchup = f"{team_abbr:4} ({ourwl[0]:2} - {ourwl[1]:2}) vs {oppabbr:4} ({theirwl[0]:2} - {theirwl[1]:2})"
        elif homeaway == "A":
            matchup = f"{team_abbr:4} ({ourwl[0]:2} - {ourwl[1]:2})  @ {oppabbr:4} ({theirwl[0]:2} - {theirwl[1]:2})"
        # print(f"{gameid}")
        result.append(f"    {gameid} {matchup}\t{outcome:4}\t{ourpts:4} - {theirpts:4}")
    result.append("")
    return result


def matchup_tuples(team_abbr, opp_abbr, season0):
    team_abbr, opp_abbr = team_abbr.upper(), opp_abbr.upper()
    dat = filter_season_data(fetch_season_data(season0), team_abbr, cup)
    matchup_tups = []
    for game in dat:
        skip = False
        if "gameid" in game.keys():
            gameid = game["gameid"]
        else:
            gameid = game["id"]
        if game["team1Abbr"] == team_abbr and game["team2Abbr"] == opp_abbr:
            other_team_name = game["team2Name"]
            other_team_abbr = game["team2Abbr"]

            our_points = game["team1Score"]
            other_points = game["team2Score"]

            our_wl = game["team1WinLoss"]
            other_wl = game["team2WinLoss"]

            if game["team2Score"] > game["team1Score"]:
                outcome = "L"
            else:
                outcome = "W"
            homeaway = "H"

        elif game["team2Abbr"] == team_abbr and game["team1Abbr"] == opp_abbr:
            other_team_name = game["team1Name"]
            other_team_abbr = game["team1Abbr"]

            our_points = game["team2Score"]
            other_points = game["team1Score"]

            our_wl = game["team2WinLoss"]
            other_wl = game["team1WinLoss"]

            if game["team1Score"] > game["team2Score"]:
                outcome = "L"
            else:
                outcome = "W"
            homeaway = "A"

        else:
            skip = True

        if not skip:
            tup = (
                gameid,
                other_team_name,
                other_team_abbr,
                homeaway,
                outcome,
                our_points,
                other_points,
                our_wl,
                other_wl,
            )
            matchup_tups.append(tup)
    return matchup_tups


def print_matchup_tuples(team_abbr, opp_abbr, season0):
    result = []
    tups = matchup_tuples(team_abbr, opp_abbr, season0)
    result.append("")
    result.append(f"Schedule for {team_abbr.upper()} vs. {opp_abbr.upper()}, Season {season0+1}")
    wins = sum([1 for tup in tups if tup[3] == "W"])
    losses = sum([1 for tup in tups if tup[3] == "L"])
    result.append(f"W-L record for {team_abbr}: {wins}-{losses}")
    for tup in tups:
        (gameid, oppname, oppabbr, homeaway, outcome, ourpts, theirpts, ourwl, theirwl) = tup
        if homeaway == "H":
            matchup = f"{team_abbr:4} ({ourwl[0]:2} - {ourwl[1]:2}) vs {oppabbr:4} ({theirwl[0]:2} - {theirwl[1]:2})"
        elif homeaway == "A":
            matchup = f"{team_abbr:4} ({ourwl[0]:2} - {ourwl[1]:2})  @ {oppabbr:4} ({theirwl[0]:2} - {theirwl[1]:2})"
        result.append(f"    {gameid} {matchup}\t{outcome:4}\t{ourpts:4} - {theirpts:4}")
    result.append("")
    return result


def fetch_teams_data(which_season0, cup):
    cup = cup.lower()
    teams_file = os.path.join(
        "..", "data", f"gollyx-{cup}-data", f"season{which_season0}", "teams.json"
    )
    if not os.path.exists(teams_file):
        raise Exception(f"Error: season {which_season0} not valid: {teams_file} does not exist")
    with open(teams_file, "r") as f:
        season0_teams = json.load(f)
    return season0_teams


if __name__ == "__main__":
    main()
