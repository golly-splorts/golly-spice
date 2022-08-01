import os
import sys

# hack
pkg_root = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
sys.path.insert(0, pkg_root)

from pkg.winners.champions import StarChampionsTable
from pkg.winners.pennant import StarPennantTable
from pkg.winners.title import StarDivTitleTable


