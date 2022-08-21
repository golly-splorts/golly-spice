import os
from spice_managers import ToroidalSpiceManager


## single thread
#os.environ['GOLLYX_SPICE_TEST_MODE'] = "real"

# multithread
os.environ['GOLLYX_SPICE_TEST_MODE'] = "multithread"


t = ToroidalSpiceManager()
t.map(threadpoolsize=8)
