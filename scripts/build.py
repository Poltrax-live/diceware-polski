"""Build the two final 7776-word Diceware lists from rated candidates.

Inputs:  data/candidates.tsv (lemma, corpus score), data/batches2/[bcd]*.txt (rated pool),
         data/batches2/[bcd]*.reject.tsv (rejected lemma, reason), data/safety/*.reject.tsv (second, safety-only pass),
         data/blocklist.txt (manual)
Outputs: lists/diceware-pl.txt (no Polish diacritics), lists/diceware-pl-ogonki.txt (with)
Format:  "11111<TAB>word", alphabetical, like the EFF lists.
"""
import glob, itertools, re, collections

N = 7776
DIAC = re.compile("[ąćęłńóśźż]")
STRIP = str.maketrans("ąćęłńóśźż", "acelnoszz")

freq = {}
for line in open("data/candidates.tsv", encoding="utf-8"):
    w, n = line.rstrip("\n").split("\t")
    freq[w] = int(n)

rating = {}
for path in sorted(glob.glob("data/batches2/[bcd]*.txt")):
    for line in open(path, encoding="utf-8"):
        rating[line.strip()] = 1
rejected = collections.Counter()
for path in sorted(glob.glob("data/batches2/[bcd]*.reject.tsv") + glob.glob("data/safety/*.reject.tsv")):
    for line in open(path, encoding="utf-8"):
        if not line.strip():
            continue
        w, reason = (line.rstrip("\n").split("\t") + [""])[:2]
        if w in rating:
            rating[w] = 0
            rejected[reason] += 1
print("rejected:", sum(rejected.values()), dict(rejected))

blocklist = set()
try:
    for line in open("data/blocklist.txt", encoding="utf-8"):
        line = line.split("#")[0].strip()
        if line:
            blocklist.add(line)
except FileNotFoundError:
    pass

ALPHABET = "aąbcćdeęfghijklłmnńoópqrsśtuvwxyzźż"

def polish_key(w):
    return [ALPHABET.index(c) for c in w]

def ranked(words):
    return sorted(words, key=lambda w: (-rating[w], -freq[w], w))

def pick(words):
    chosen, seen_ascii = [], set()
    for w in ranked(words):
        key = w.translate(STRIP)
        if key in seen_ascii:  # e.g. "laska" vs "łaska": keep only one
            continue
        seen_ascii.add(key)
        chosen.append(w)
        if len(chosen) == N:
            break
    if len(chosen) < N:
        raise SystemExit(f"only {len(chosen)} words available, need {N}")
    return sorted(chosen, key=polish_key)

ok = [w for w, s in rating.items() if s >= 1 and w not in blocklist]
plain = pick([w for w in ok if not DIAC.search(w)])
full = pick(ok)

dice = ["".join(p) for p in itertools.product("123456", repeat=5)]
for name, words in (("lists/diceware-pl.txt", plain), ("lists/diceware-pl-ogonki.txt", full)):
    assert len(set(words)) == N
    with open(name, "w", encoding="utf-8", newline="\n") as f:
        for d, w in zip(dice, words):
            f.write(f"{d}\t{w}\n")
    lens = [len(w) for w in words]
    print(f"{name}: {N} words, "
          f"avg len {sum(lens)/N:.1f}, with diacritics {sum(bool(DIAC.search(w)) for w in words)}")
