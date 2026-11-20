"""Build candidate lemmas: SJP base forms ranked by summed corpus frequency of all their forms."""
import re, sys, json, collections

odm_path, freq_path, out_path = sys.argv[1:4]

freq = {}
with open(freq_path, encoding="utf-8") as f:
    for line in f:
        w, n = line.split()
        freq[w] = int(n)

LETTERS = re.compile(r"^[a-ząćęłńóśźż]+$")
score = collections.Counter()
forms_seen = {}
with open(odm_path, encoding="utf-8") as f:
    for line in f:
        forms = [x.strip() for x in line.strip().split(",")]
        lemma = forms[0]
        if not LETTERS.match(lemma) or not (3 <= len(lemma) <= 9):
            continue
        s = sum(freq.get(x, 0) for x in set(forms))
        if s > score[lemma]:
            score[lemma] = s

ranked = [(w, n) for w, n in score.most_common() if n > 0]
with open(out_path, "w", encoding="utf-8") as f:
    for w, n in ranked:
        f.write(f"{w}\t{n}\n")
plain = [w for w, _ in ranked if not re.search("[ąćęłńóśźż]", w)]
print("all:", len(ranked), "no-diacritics:", len(plain))
