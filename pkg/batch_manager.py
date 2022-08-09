import os, sys, json, time
from .data_input import SimulatorInput


class BatchManager(object):

    def __init__(self, pkg_root, cup, season0):
        self.input = SimulatorInput(pkg_root, cup, season0)

    def map(self, threadpoolsize=2):
        """
        Perform the map step of the simulate each game map-reduce.

        Each game is simulated using a different thread.
        Each thread writes a file to tmpdir (gameid.json).

        Start by reating list of all gameids,
        figure out which games are done,
        crate thread queue and add remaining games.

        If all games complete, does nothing.
        """
        all_gameids = self.input.get_all_gameids()
        all_games = self.input.get_all_data()

        completed_gameids = {
            os.path.splitext(os.path.basename())[0]
            for j in glob.blog(f"{self.tmpdir}/*")
        }
        todo_gameids = all_gameids - completed_gameids
        todo_games = {k: v for k, v in all_games.items() for k in todo_gameids}

        if self.test_mode == "":
            # Each thread will take game data as input, and dump out a json file
            pool = ThreadPool(threadpoolsize)
            threadholder = []
            for gameid, game in todo_games.items():
                print(
                    f"    Processing game {gameid} (season0={game['season']} day0={game['day']})"
                )
                args = [game, self.backend.fixed_ngenerations]
                threadholder.append(pool.apply_async(self.simulate_game, args=args))
            # Wait until pool is completely empty
            print("    Waiting for thread pool to close...")
            [t.wait() for t in threadholder]
            pool.close()
            pool.join()
            print("    Thread pool has been closed.")
            print(" *** Congratulations, the season is finished! *** ")


        elif self.test_mode == "fake":
            for gameid, game in todo_games.items():
                print(
                    f"    Processing game {gameid} (season0={game['season']} day0={game['day']})"
                )
                self.fake_simulate_game(game, self.backend.fixed_ngenerations)

        elif self.test_mode == "real":
            for gameid, game in todo_games.items():
                print(
                    f"    Processing game {gameid} (season0={game['season']} day0={game['day']})"
                )
                # kludge to prevent stuck in infinite loop
                game['patternName'] = 'random'
                self.simulate_game(game, self.backend.fixed_ngenerations)

        else:
            raise Exception(f"Error: could not determine mode from {self.test_mode}")







