import os, sys, subprocess, json, time
from pprint import pprint

from .cup_data import PseudoCup
from gollyx_python.manager import PseudoGOL


class PseudoGOL_Instrumented(PseudoGOL):
    live_counts_keys = ['generation','victoryPct','liveCells1','liveCells2', 'last3']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.live_counts = []
        new_stats = self.life.get_stats()
        new_live_count = {k : new_stats[k] for k in self.live_counts_keys}
        self.live_counts.append(new_live_count)

    def next_step(self):
        new_stats = super().next_step()
        new_live_count = {k : new_stats[k] for k in self.live_counts_keys}
        self.live_counts.append(new_live_count)
        return new_stats

    def export(self):
        pass


class PseudoSpice(object):
    CupClass = PseudoCup

    def __init__(self, *args, **kwargs):
        pass






CupClass = PseudoCup

cup = 'pseudo'
cup_key = 'HCS'

for season0 in range(0, 24):

    seas_file = os.path.join('data', f'gollyx-{cup}-data', f'season{season0}', 'season.json')
    post_file = os.path.join('data', f'gollyx-{cup}-data', f'season{season0}', 'postseason.json')

    with open(seas_file, 'r') as f:
        seas_dat = json.load(f)

    with open(post_file, 'r') as f:
        post_dat = json.load(f)




pseudo_cup = season0_post[cup_key]


# Analysis of last day

last_day = pseudo_cup[-1]
last_game = last_day[0]

ic1 = last_game['map']['initialConditions1']
ic2 = last_game['map']['initialConditions2']
gameid = last_game['gameid']

inst = PseudoGOL_Instrumented(
    s1=ic1,
    s2=ic2,
    rows=100,
    columns=120,
    halt=True,
)

N = 0

tic = time.time()
while inst.running:
    N += 1
    inst.next_step()
toc = time.time()
diff = toc-tic

print(f"{N} steps took {diff:0.2f} s")












