import os, json
from gollyx_python.manager import (
    HellmouthGOL,
    PseudoGOL,
    ToroidalGOL,
    #DragonCA,
    RainbowGOL,
    StarGOLGenerations,
    KleinGOL,
)


class InstrumentedBase(object):
    live_counts_keys = ['generation','victoryPct','liveCells1','liveCells2'] #, 'last3']

    def _config(self, **kwargs):

        if 'monitor_dir' not in kwargs.keys() or not os.path.isdir(kwargs['monitor_dir']):
            raise KeyError("Error: keyword arg 'monitor_dir' must be provided and must point to a directory that exists")
        self.monitor_dir = kwargs['monitor_dir']

        if 'gameid' not in kwargs.keys():
            raise KeyError("Error: keyword arg 'gameid' must be provided to dump monitoring output to a file")

        self.gameid = kwargs['gameid']

    def _init_live_counts(self, obj):
        self.live_counts = []
        new_stats = obj.count()
        self._save_live_counts(new_stats)

    def _save_live_counts(self, new_stats):
        new_live_count = {k : new_stats[k] for k in self.live_counts_keys}
        self.live_counts.append(new_live_count)

    def export(self):
        # Strip out the data we're most interested in: scores
        t1s = [j['liveCells1'] for j in self.live_counts]
        t2s = [j['liveCells2'] for j in self.live_counts]
        export_dat = {
            self.gameid: [
                t1s,
                t2s
            ]
        }
        # Export this dictionary to <game uuid>.json
        jname = os.path.join(self.monitor_dir, self.gameid+".json")
        with open(jname, 'w') as f:
            json.dump(export_dat, f)


class HellmouthGOL_Instrumented(InstrumentedBase, HellmouthGOL):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._config(**kwargs)
        self._init_live_counts(self)

    def next_step(self):
        new_stats = super().next_step()
        self._save_live_counts(new_stats)
        return new_stats


class PseudoGOL_Instrumented(InstrumentedBase, PseudoGOL):

    def __init__(self, *args, **kwargs):
        super().__init__(**kwargs)
        self._config(**kwargs)
        self._init_live_counts(self)

    def next_step(self):
        new_stats = super().next_step()
        self._save_live_counts(new_stats)
        return new_stats


class ToroidalGOL_Instrumented(InstrumentedBase, ToroidalGOL):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._config(**kwargs)
        self._init_live_counts(self)

    def next_step(self):
        new_stats = super().next_step()
        self._save_live_counts(new_stats)
        return new_stats


#class DragonGOL_Instrumented(InstrumentedBase, DragonCA):
#
#    def __init__(self, *args, **kwargs):
#        super().__init__(*args, **kwargs)
#        self._config(**kwargs)
#        self._init_live_counts(self)
#
#    def next_step(self):
#        new_stats = super().next_step()
#        self._save_live_counts(new_stats)
#        return new_stats


class RainbowGOL_Instrumented(InstrumentedBase, RainbowGOL):
    live_counts_keys = ['generation','victoryPct','liveCells1','liveCells2','liveCells3','liveCells4'] #, 'last3'] 

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._config(**kwargs)
        self._init_live_counts(self)

    def next_step(self):
        new_stats = super().next_step()
        self._save_live_counts(new_stats)
        return new_stats

    def export(self):
        # Strip out the data we're most interested in: scores
        t1s = [j['liveCells1'] for j in self.live_counts]
        t2s = [j['liveCells2'] for j in self.live_counts]
        t3s = [j['liveCells3'] for j in self.live_counts]
        t4s = [j['liveCells4'] for j in self.live_counts]
        export_dat = {
            gameid: [
                t1s,
                t2s,
                t3s,
                t4s,
            ]
        }
        # Export this dictionary to <game uuid>.json
        jname = os.path.join(self.monitor_dir, gameid+".json")
        with open(jname, 'w') as f:
            json.dump(f, export_dat)


class StarGOL_Instrumented(InstrumentedBase, StarGOLGenerations):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._config(**kwargs)
        self._init_live_counts(self)

    def next_step(self):
        new_stats = super().next_step()
        self._save_live_counts(new_stats)
        return new_stats


class KleinGOL_Instrumented(InstrumentedBase, KleinGOL):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._config(**kwargs)
        self._init_live_counts(self)

    def next_step(self):
        new_stats = super().next_step()
        self._save_live_counts(new_stats)
        return new_stats

