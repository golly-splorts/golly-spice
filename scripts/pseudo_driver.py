import os
from spice_managers import (
    HellmouthSpiceManager,
    PseudoSpiceManager,
)


# single thread
os.environ['GOLLYX_SPICE_TEST_MODE'] = "real"

## multithread
#os.environ['GOLLYX_SPICE_TEST_MODE'] = "multithread"


p = HellmouthSpiceManager(fixed_ngenerations = 100)
print(p.map(threadpoolsize=1))
#p.map(threadpoolsize=4)
# There is no reduce step
