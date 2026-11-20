"""Polish Diceware word lists (7776 words each) and a passphrase generator.

    >>> import diceware_polski
    >>> diceware_polski.generate()                      # 7 words, no Polish diacritics
    >>> diceware_polski.generate(words=8, diacritics=True, separator="-")
    >>> diceware_polski.lookup("43136")                 # word for a five-dice roll
"""
import math
import secrets
from functools import lru_cache
from importlib import resources

__version__ = "1.0.0"
__all__ = ["generate", "lookup", "entropy_bits", "words", "dice_table", "LIST_SIZE"]

LIST_SIZE = 7776
DEFAULT_WORDS = 7
_FILES = {False: "diceware-pl.txt", True: "diceware-pl-ogonki.txt"}


@lru_cache(maxsize=None)
def dice_table(diacritics=False):
    """Return a dict mapping five-dice rolls ("11111".."66666") to words."""
    text = resources.files(__package__).joinpath("lists", _FILES[bool(diacritics)]).read_text(encoding="utf-8")
    table = {}
    for line in text.splitlines():
        if line.strip():
            roll, word = line.split("\t")
            table[roll] = word.strip()
    if len(table) != LIST_SIZE:
        raise RuntimeError(f"expected {LIST_SIZE} words, got {len(table)}")
    return table


def words(diacritics=False):
    """Return the word list as a tuple."""
    return tuple(dice_table(diacritics).values())


def generate(words=DEFAULT_WORDS, diacritics=False, separator=" "):
    """Return a passphrase of `words` words chosen with the `secrets` module."""
    if not isinstance(words, int) or isinstance(words, bool) or words < 1:
        raise ValueError("words must be a positive integer")
    pool = _words(diacritics)
    return separator.join(secrets.choice(pool) for _ in range(words))


def lookup(roll, diacritics=False):
    """Return the word for a five-dice roll such as "43136"."""
    roll = str(roll)
    if len(roll) != 5 or any(c not in "123456" for c in roll):
        raise ValueError("roll must be five digits from 1 to 6")
    return dice_table(diacritics)[roll]


def entropy_bits(words=DEFAULT_WORDS):
    """Approximate passphrase strength in bits."""
    return words * math.log2(LIST_SIZE)


_words = words
