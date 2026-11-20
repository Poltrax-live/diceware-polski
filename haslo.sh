#!/bin/sh
# Losuje hasło z polskiej listy Diceware (Linux; na macOS użyj haslo.py).
# Użycie: ./haslo.sh [liczba_słów] [ogonki]
n="${1:-7}"
list="$(dirname "$0")/lists/diceware-pl.txt"
[ "$2" = "ogonki" ] && list="$(dirname "$0")/lists/diceware-pl-ogonki.txt"
cut -f2 "$list" | shuf -r -n "$n" --random-source=/dev/urandom | paste -sd' ' -
