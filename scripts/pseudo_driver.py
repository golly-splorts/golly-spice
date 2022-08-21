import os
from spice_managers import PseudoSpiceManager


## single thread
#os.environ['GOLLYX_SPICE_TEST_MODE'] = "real"

# multithread
os.environ['GOLLYX_SPICE_TEST_MODE'] = "multithread"


p = PseudoSpiceManager()
p.map(threadpoolsize=8)
