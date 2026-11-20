# diceware-polski

Pełna polska lista [Diceware](https://world.std.com/~reinhold/diceware.html) (7776 słów) i bezpieczny generator haseł.
Full Polish Diceware word lists (7776 words each) and a secure passphrase generator.

- Bez polskich znaków (domyślnie) albo z nimi (`diacritics`).
- Losowanie kryptograficznym generatorem (`secrets` / `crypto.getRandomValues` / `SecureRandom`).
- 7 słów ≈ 90 bitów.

**Python**

```bash
pip install diceware-polski
diceware-polski 7
```

```python
import diceware_polski
diceware_polski.generate()                                   # 'lustro okoń pościel ...'
diceware_polski.generate(words=8, diacritics=True, separator="-")
diceware_polski.lookup("43136")                              # word for a dice roll
```

**JavaScript (Node.js ≥ 19 / przeglądarka)**

```bash
npm install diceware-polski
npx diceware-polski 7
```

```js
import { generate, lookup } from "diceware-polski";
generate();                                                  // "lustro okoń pościel ..."
generate({ words: 8, diacritics: true, separator: "-" });
lookup("43136");
```

**Ruby:** `gem install diceware-polski`

Generator w przeglądarce, instrukcja z kostką i lista do druku: https://poltrax-live.github.io/diceware-polski/
Źródło, sposób budowy listy i zgłoszenia: https://github.com/Poltrax-live/diceware-polski

Listy: CC BY-SA 4.0 (SJP.pl, FrequencyWords/OpenSubtitles). Kod: MIT. Zrobione w [Poltrax](https://poltrax.live).
