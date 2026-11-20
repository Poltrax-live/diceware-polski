# Jak zmienić listę i wydać nową wersję

1. Popraw słowa: dopisz je do `data/blocklist.txt` (albo popraw oceny w `data/`).
2. `python3 scripts/build.py` - przebudowuje `lists/`.
3. Podbij wersję w `VERSION` (zmiana listy = zmiana numeracji, więc co najmniej minor/patch z opisem w tagu).
4. `python3 scripts/sync_packages.py` - kopiuje listy do paczek i ustawia wersję w Ruby/Python/npm.
5. `python3 scripts/build_web.py` - odświeża stronę w `docs/`.
6. Testy: `ruby -Ilib test/diceware_polski_test.rb`, `cd python && PYTHONPATH=src python3 -m unittest discover -s tests`, `cd js && npm test`.
7. Commit, `git tag -a vX.Y.Z`, push z tagami.
8. Publikacja (konta z 2FA):
   - Ruby: `gem build diceware-polski.gemspec && gem push diceware-polski-X.Y.Z.gem`
   - Python: `cd python && python3 -m build && python3 -m twine upload dist/*`
   - npm: `cd js && npm publish`
