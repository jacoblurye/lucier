import random
import math
from typing import Generator, List, TypeVar

T = TypeVar("T")


def random_iter(values: List[T]) -> Generator[T, None, None]:
    while True:
        yield random.choice(values)


def random_fragments(fragments: List[List[T]]) -> Generator[List[T], None, None]:
    while True:
        fragment = random.choice(fragments)
        for value in fragment:
            yield value


def coin_flip(p: float) -> bool:
    return p > random.random()


def every_n_ticks(n, tick, offset=0):
    return not (tick - offset) % n


def major_scale(root: int) -> List[int]:
    return [root, root + 2, root + 4, root + 5, root + 7, root + 9, root + 11]


def maybe_8va(odds: int) -> Generator[int, None, None]:
    return random_iter([0] * odds + [12])


def sine(tick: int, min: int, max: int, period: int, shift: int = 0) -> int:
    x = (tick - shift) / period * 2 * math.pi
    y = math.sin(x) * 0.5 + 0.5
    return int(y * (max - min) + min)


def incperc(tick: int, scale: float):
    scaled_tick = tick * scale
    return scaled_tick / (scaled_tick + 1)


# So you don't have to import the python random module separately
r = random