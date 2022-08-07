from multiprocessing.pool import ThreadPool
import os, sys, time, glob, json
from cup_data import (
    CupBase,
    HellmouthCup,
    PseudoCup,
    ToroidalCup,
    #DragonCup,
    #RainbowCup,
    StarCup,
    KleinCup,
)
from instrumented_simulators import (
    HellmouthGOL_Instrumented,
    PseudoGOL_Instrumented,
    ToroidalGOL_Instrumented,
    #DragonGOL_Instrumented,
    #RainbowGOL_Instrumented,
    StarGOL_Instrumented,
    KleinGOL_Instrumented,
)
from utils import get_cup_rule_b, get_cup_rule_s


class SpiceManager(object):

    CupDataClass = CupBase

    def __init__(
            self, 
            fixed_ngenerations=0
        ):
        self.fixed_ngenerations = fixed_ngenerations
        self.season0max = self.CupDataClass.GOLLYX_MAX_SEASON0
        self.test_mode = os.environ.get("GOLLYX_SPICE_TEST_MODE", "")
        if 'GOLLY_SPICE_TEST_MODE' in os.environ.keys():
            raise Exception("ERROR: You specified GOLLY_SPICE_TEST_MODE but you must use GOLLYX_SPICE_TEST_MODE (with an X)!")

    def simulate_game(self, game, fixed_ngenerations, season_output_dir):
        """
        Simulate a single game. If fixed_ngeneations is 0,
        use the default stopping critera, otherwise stop the
        simulation after fixed_ngenerations generations.

        Stopping criteria is not determined here.
        Each cup has its own GOL class, and stopping
        criteria is determined/implemented by that class.
        """
        s1 = game['map']['initialConditions1']
        s2 = game['map']['initialConditions2']
        rows = game['map']["rows"]
        columns = game['map']["columns"]

        if 'id' in game.keys():
            gameid = game['id']
        elif 'gameid' in game.keys():
            gameid = game['gameid']

        print(f"Starting spice simulation of {gameid}")
        start = time.time()

        cup = self.CupDataClass.name.lower()
        if cup=="hellmouth":
            rule_b = get_cup_rule_b(cup)
            rule_s = get_cup_rule_s(cup)
            gol = HellmouthGOL_Instrumented(
                monitor_dir=season_output_dir,
                gameid=gameid,
                s1=s1, s2=s2, rows=rows, columns=columns, rule_b=rule_b, rule_s=rule_s
            )
        elif cup=="toroidal":
            rule_b = get_cup_rule_b(cup)
            rule_s = get_cup_rule_s(cup)
            gol = ToroidalGOL_Instrumented(
                monitor_dir=season_output_dir,
                gameid=gameid,
                s1=s1, s2=s2, rows=rows, columns=columns, rule_b=rule_b, rule_s=rule_s
            )
        elif cup=="pseudo":
            rule_b = get_cup_rule_b(cup)
            rule_s = get_cup_rule_s(cup)
            import pdb; pdb.set_trace()
            gol = PseudoGOL_Instrumented(
                monitor_dir=season_output_dir,
                gameid=gameid,
                s1=s1, s2=s2, rows=rows, columns=columns, rule_b=rule_b, rule_s=rule_s
            )
        # Rainbow?
        # Dragon?
        elif cup=="star":
            rule_b = get_cup_rule_b(cup)
            rule_s = get_cup_rule_s(cup)
            rule_c = get_cup_rule_c(cup)
            gol = StarGOLGenerations_Instrumented(
                monitor_dir=season_output_dir,
                gameid=gameid,
                s1=s1, s2=s2, rows=rows, columns=columns, rule_b=rule_b, rule_s=rule_s, rule_c=rule_c
            )
        elif cup=="klein":
            rule_b = get_cup_rule_b(cup)
            rule_s = get_cup_rule_s(cup)
            gol = KleinGOL_Instrumented(
                monitor_dir=season_output_dir,
                gameid=gameid,
                s1=s1, s2=s2, rows=rows, columns=columns, rule_b=rule_b, rule_s=rule_s
            )
        else:
            raise ValueError(f"Unrecognized cup: {cup}")

        while (fixed_ngenerations == 0 and gol.running) or (
            fixed_ngenerations > 0 and gol.generation < fixed_ngenerations
        ):
            gol.next_step()

        # Extract the information to be exported...


        # Output game to tmpdir/<game-id>.json
        gamejson = os.path.join(self.tmpdir, game["id"] + ".json")
        with open(gamejson, "w") as f:
            json.dump(game, f, indent=4)

        time.sleep(1)
        print(f"{prefix}Wrote game data to {gamejson}")


    def map(self, threadpoolsize=2):
        """
        Run simulations of each game, one season per batch.
        This method fills the threadpool with all the games
        to be simulated for a particular season, then runs
        each thread in the threadpool until they're all done.
        (That's the map step, there is no reduce step.)

        The instrumented simulator class will write the finished
        simulation time series to <uuid>.json
        Don't need to do that here
        """
        cup = self.CupDataClass.name.lower()
        
        for season0 in range(0, self.season0max):

            # These are parameters required by the instrumented simulator
            input_dir = os.path.abspath(os.path.join('..', 'data', f'gollyx-{cup}-data', f'season{season0}'))
            season_output_dir = os.path.abspath(os.path.join('..', 'instrument_data', f'{cup}', f'season{season0}'))

            if not os.path.exists(input_dir):
                raise FileNotFoundError(f"Error: could not find specified input data directory {input_dir}")
            if not os.path.exists(season_output_dir):
                print(f"Output directory does not exist, creating it:  {season_output_dir}")
                os.makedirs(season_output_dir)

            seasonfile = os.path.join(input_dir, 'season.json')
            with open(seasonfile, 'r') as f:
                seasondat = json.load(f)

            postfile = os.path.join(input_dir, 'postseason.json')
            with open(postfile, 'r') as f:
                postdat = json.load(f)

            # Assemble a list of games to simulate, and games already simulated
            all_games = {}

            # Regular season games:
            for day in seasondat:
                for game in day:
                    if 'id' in game.keys():
                        gameid = game['id']
                    elif 'gameid' in game.keys():
                        gameid = game['gameid']
                    all_games[gameid] = game

            # Postseason games:
            for series in postdat:
                miniseason = postdat[series]
                for day in miniseason:
                    for game in day:
                        if 'id' in game.keys():
                            gameid = game['id']
                        elif 'gameid' in game.keys():
                            gameid = game['gameid']
                        all_games[gameid] = game

            all_gameids = set(all_games.keys())

            # Get the list of all <uuid>.json files and strip the extension 
            # to get the list of game uuids that have already been simulated
            completed_gameids = {
                os.path.splitext(os.path.basename(j))[0]
                for j in glob.glob(f"{season_output_dir}/*")
            }
            todo_gameids = all_gameids - completed_gameids
            todo_games = {k: v for k, v in all_games.items() if k in todo_gameids}

            # When running in multithread method, this function will wait
            # until the threadpool is empty before returning, so it really is
            # working in one-season batches
            self._fill_threadpool(threadpoolsize, todo_games, season_output_dir)

        print("=====================================")
        print("========== CONGRATULATIONS ==========")
        print("==========  YOU ARE DONE   ==========")
        print("=====================================")

    def _fill_threadpool(self, threadpoolsize, todo_games, season_output_dir):

        if self.test_mode == "" or self.test_mode == "multithread":
            # multithread mode means, multi-threaded, running real simulations
            pool = ThreadPool(threadpoolsize)
            threadholder = []
            for gameid, game in todo_games.items():
                print(
                    f"    Processing game {gameid} (season0={game['season']} day0={game['day']} fixed_ngenerations={self.fixed_ngenerations})"
                )
                args = [game, self.fixed_ngenerations, season_output_dir]
                threadholder.append(
                    pool.apply_async(self.simulate_game, args=args)
                )
            # Wait until pool is completely empty
            print("    Waiting for thread pool to close...")
            [t.wait() for t in threadholder]
            pool.close()
            pool.join()
            print("    Thread pool has been closed.")
            print(" *** Congratulations, the season is finished! *** ")

        elif self.test_mode == "fake":
            # Fake mode means, single-threaded, not running simulations
            for gameid, game in todo_games.items():
                print(
                    f"    Processing game {gameid} (season0={game['season']} day0={game['day']} fixed_ngenerations={self.fixed_ngenerations})"
                )
                self.fake_simulate_game(game, self.fixed_ngenerations, season_output_dir)

        elif self.test_mode == "real":
            # real mode means, single-threaded, running actual simulations
            for gameid, game in todo_games.items():
                print(
                    f"    Processing game {gameid} (season0={game['season']} day0={game['day']} fixed_ngenerations={self.fixed_ngenerations})"
                )
                # kludge to prevent stuck in infinite loop
                game['patternName'] = 'random'
                self.simulate_game(game, self.fixed_ngenerations, season_output_dir)

        else:
            raise Exception(f"Error: could not determine mode from {self.test_mode}")

class HellmouthSpiceManager(SpiceManager):
    CupDataClass = HellmouthCup

class PseudoSpiceManager(SpiceManager):
    CupDataClass = PseudoCup

class ToroidalSpiceManager(SpiceManager):
    CupDataClass = ToroidalCup

#class DragonSpiceManager(SpiceManager):
#    CupDataClass = DragonCup

#class RainbowSpiceManager(SpiceManager):
#    CupDataClass = RainbowCup

class StarSpiceManager(SpiceManager):
    CupDataClass = StarCup

class KleinSpiceManager(SpiceManager):
    CupDataClass = KleinCup
