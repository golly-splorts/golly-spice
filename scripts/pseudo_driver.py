from season_simulators import PseudoSpiceManager


p = PseudoSpiceManager()
p.map(threadpoolsize=8)
# There is no reduce step
