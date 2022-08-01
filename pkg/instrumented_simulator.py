import os, sys, json, time

post_file = os.path.join('data', f'gollyx-{cup}-data', 'season0', 'postseason.json')
with open(post_file, 'r') as f:
    season0_post = json.load(f)
pseudo_cup = season0_post['HCS']
last_day = pseudo_cup[-1]
last_game = last_day[0]
pprint(list(last_game.keys()))
##########
nrows = last_game['map']['rows']
ncols = last_game['map']['columns']

ic1 = last_game['map']['initialConditions1']
ic2 = last_game['map']['initialConditions2']

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

gol = PseudoGOL_Instrumented(
    s1=ic1,
    s2=ic2,
    rows=100,
    columns=120,
    halt=False,
)

N = 0

tic = time.time()
while inst.running:
    N += 1
    inst.next_step()
toc = time.time()
diff = toc-tic

#print(f"{N} steps took {diff:0.2f} s")




