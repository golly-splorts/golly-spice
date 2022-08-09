import os
from spice_managers import HellmouthSpiceManager


## single thread
#os.environ['GOLLYX_SPICE_TEST_MODE'] = "real"

# multithread
os.environ['GOLLYX_SPICE_TEST_MODE'] = "multithread"


h = HellmouthSpiceManager()
#h = HellmouthSpiceManager(season0end=4)
#h = HellmouthSpiceManager(season0start=5)
h.map(threadpoolsize=8)
