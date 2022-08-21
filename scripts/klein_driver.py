import os
from spice_managers import KleinSpiceManager


## single thread
#os.environ['GOLLYX_SPICE_TEST_MODE'] = "real"

# multithread
os.environ['GOLLYX_SPICE_TEST_MODE'] = "multithread"


s = KleinSpiceManager()
s.map(threadpoolsize=8)
