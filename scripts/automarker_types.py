from typing import Callable, List

Automarker = Callable[[List[dict], int], tuple[int, str] | None]
