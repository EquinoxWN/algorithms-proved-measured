"""Classic algorithms, each checked against shared vectors and a brute-force oracle."""

from algorithms_proved_measured.dp import edit_distance
from algorithms_proved_measured.graphs import dijkstra
from algorithms_proved_measured.search import lower_bound
from algorithms_proved_measured.sorting import merge_sort
from algorithms_proved_measured.strings import find_all

__all__ = ["dijkstra", "edit_distance", "find_all", "lower_bound", "merge_sort"]
__version__ = "0.1.0"
