#!/usr/bin/env python3
"""Losuje hasło z polskiej listy Diceware. Działa na Windowsie, macOS i Linuxie (Python 3.6+).

Użycie:
  python3 haslo.py              # 7 słów z listy bez polskich znaków
  python3 haslo.py 8            # 8 słów
  python3 haslo.py --ogonki     # lista z polskimi znakami
  python3 haslo.py 6 -s -       # 6 słów, rozdzielone myślnikiem
"""
import argparse, math, os, secrets

HERE = os.path.dirname(os.path.abspath(__file__))

def main():
    p = argparse.ArgumentParser(description="Losuje hasło z polskiej listy Diceware.")
    p.add_argument("slowa", nargs="?", type=int, default=7, help="liczba słów (domyślnie 7)")
    p.add_argument("--ogonki", action="store_true", help="użyj listy z polskimi znakami")
    p.add_argument("-s", "--separator", default=" ", help="znak między słowami (domyślnie spacja)")
    p.add_argument("-l", "--lista", help="ścieżka do własnej listy")
    a = p.parse_args()

    name = "diceware-pl-ogonki.txt" if a.ogonki else "diceware-pl.txt"
    path = a.lista or os.path.join(HERE, "lists", name)
    with open(path, encoding="utf-8") as f:
        words = [line.split()[-1] for line in f if line.strip()]

    # secrets = kryptograficzny generator liczb losowych systemu (odpowiednik uczciwej kostki)
    print(a.separator.join(secrets.choice(words) for _ in range(a.slowa)))
    bits = a.slowa * math.log2(len(words))
    print(f"(siła: ok. {bits:.0f} bitów, lista: {len(words)} słów)", file=__import__("sys").stderr)

if __name__ == "__main__":
    main()
