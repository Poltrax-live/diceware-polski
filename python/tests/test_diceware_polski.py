import re
import unittest
from pathlib import Path

import diceware_polski as dp

ROOT = Path(__file__).resolve().parents[2]


class DicewarePolskiTest(unittest.TestCase):
    def test_lists_match_repo_lists(self):
        for diacritics, name in ((False, "diceware-pl.txt"), (True, "diceware-pl-ogonki.txt")):
            repo = (ROOT / "lists" / name).read_text(encoding="utf-8").split("\n")
            table = dp.dice_table(diacritics)
            self.assertEqual(len(table), 7776)
            self.assertEqual(len(set(table.values())), 7776)
            self.assertEqual([f"{r}\t{w}" for r, w in table.items()], [l for l in repo if l])

    def test_plain_has_no_diacritics(self):
        self.assertFalse(any(re.search("[ąćęłńóśźż]", w) for w in dp.words()))

    def test_generate(self):
        parts = dp.generate(words=5, separator="-").split("-")
        self.assertEqual(len(parts), 5)
        self.assertTrue(set(parts) <= set(dp.words()))

    def test_lookup_and_errors(self):
        self.assertEqual(dp.lookup(11111), dp.words()[0])
        self.assertEqual(dp.lookup("66666", diacritics=True), dp.words(True)[-1])
        with self.assertRaises(ValueError):
            dp.lookup("12347")
        with self.assertRaises(ValueError):
            dp.generate(words=0)

    def test_entropy(self):
        self.assertAlmostEqual(dp.entropy_bits(7), 90.47, places=2)


if __name__ == "__main__":
    unittest.main()
