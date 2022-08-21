import os
from spice_managers import HellmouthSpiceManager


## single thread
#os.environ['GOLLYX_SPICE_TEST_MODE'] = "real"

# multithread
os.environ['GOLLYX_SPICE_TEST_MODE'] = "multithread"


h = HellmouthSpiceManager()
h.map(threadpoolsize=8)
