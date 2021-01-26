import random
import math
from typing import Generator, List, TypeVar

T = TypeVar("T")


def random_iter(values: List[T]) -> Generator[T, None, None]:
    """Yield a random value picked from the provided list of values, forever.

    Args:
        values: A list of possible values to yield.

    Yields:
        A value randomly chosen from the list of values.
    """
    while True:
        yield random.choice(values)


def random_sequences(sequences: List[List[T]]) -> Generator[List[T], None, None]:
    """Yield values from a sequence randomly chosen from a list of sequences, forever.

    Args:
        sequences: A list of lists of values (a.k.a. sequences).

    Yields:
        The next value in the current randomly chosen sequence. Once that sequence is
        exhausted, another sequence will be randomly chosen from the provided list.
    """
    while True:
        fragment = random.choice(sequences)
        for value in fragment:
            yield value


def coin_flip(p: float) -> bool:
    """Flip a biased coin.

    Args:
        p: probability between 0 and 1 of the coin landing heads up.

    Returns:
        True if the coin lands heads up, False otherwise.
    """
    return p > random.random()


def every_n_ticks(n: int, tick: int, offset: int = 0) -> bool:
    """Fire a signal every n ticks.

    Args:
        n: the number of ticks to wait before signalling.
        tick: the current tick number.
        offset: the amount by which to shift the provided tick number.

    Returns:
        True if n ticks have passed, False otherwise.
    """
    return not (tick + offset) % n


def major_scale(root: int) -> List[int]:
    """Build a MIDI major scale from the given root.

    Args:
        root: the MIDI note number to use as the scale's root.

    Returns:
        A list of 7 MIDI notes representing a major scale with the given root.
    """
    assert (
        0 <= root and root < 127
    ), f"the provided root is not a valid MIDI note: {root}"
    return [root, root + 2, root + 4, root + 5, root + 7, root + 9, root + 11]


def maybe_octave(odds: int) -> Generator[int, None, None]:
    """Return either 0 or 12, with variable odds.

    Args:
        odds: the odds of returning 0 instead of 12, e.g., an odds of 5
              will yield 0 five times more often than 12.

    Yields:
        0 or 12, with 0 likelier than 12 according to `odds`.
    """
    assert odds >= 0, f"expected non-negative odds but received: {odds}"
    return random_iter([0] * odds + [12])


def sine(tick: int, min: int, max: int, period: int, shift: int = 0) -> int:
    """A sine wave that is a function of the current tick.

    Args:
        tick: the current tick number.
        min: the minimum value of the sine wave.
        max: the maximum value of the sine wave.
        period: the period of the sine wave in ticks.
        shift: the tick offset of the sine wave.

    Returns:
        The value of the sine wave at the provided tick number.
    """
    x = (tick - shift) / period * 2 * math.pi
    y = math.sin(x) * 0.5 + 0.5
    return int(y * (max - min) + min)


def incrat(tick: int, scale: float):
    """A function of the provided tick whose value asymptotically approaches 1 as tick increases.

    Args:
        tick: the current tick number.
        scale: a positive number for modifying the rate of increase of the function.

    Returns:
        The value of the function for the given tick.
    """
    scaled_tick = tick * scale
    return scaled_tick / (scaled_tick + 1)


# So you don't have to import the python random module separately
r = random