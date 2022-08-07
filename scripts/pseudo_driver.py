import os
from spice_managers import PseudoSpiceManager


# single thread
os.environ['GOLLYX_SPICE_TEST_MODE'] = "real"

## multithread
#os.environ['GOLLYX_SPICE_TEST_MODE'] = "multithread"


p = PseudoSpiceManager(fixed_ngenerations = 100)
p.map(threadpoolsize=4)
# There is no reduce step
