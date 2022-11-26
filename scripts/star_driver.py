import os
from spice_managers import StarSpiceManager


## single thread
#os.environ['GOLLYX_SPICE_TEST_MODE'] = "real"

# multithread
os.environ['GOLLYX_SPICE_TEST_MODE'] = "multithread"


s = StarSpiceManager()
s.map(threadpoolsize=8)
