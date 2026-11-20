import argparse
import sys

from . import DEFAULT_WORDS, __version__, entropy_bits, generate


def main(argv=None):
    p = argparse.ArgumentParser(prog="diceware-polski", description="Losuje hasło z polskiej listy Diceware.")
    p.add_argument("slowa", nargs="?", type=int, default=DEFAULT_WORDS, help="liczba słów (domyślnie 7)")
    p.add_argument("-o", "--ogonki", action="store_true", help="lista z polskimi znakami")
    p.add_argument("-s", "--separator", default=" ", help="znak między słowami (domyślnie spacja)")
    p.add_argument("-v", "--version", action="version", version=__version__)
    a = p.parse_args(argv)
    if a.slowa < 1:
        p.error("liczba słów musi być dodatnia")
    print(generate(words=a.slowa, diacritics=a.ogonki, separator=a.separator))
    print(f"(siła: ok. {entropy_bits(a.slowa):.0f} bitów)", file=sys.stderr)


if __name__ == "__main__":
    main()
