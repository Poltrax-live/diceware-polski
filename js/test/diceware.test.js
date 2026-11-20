import { test } from "node:test";
import assert from "node:assert/strict";
import { readFileSync } from "node:fs";
import { generate, lookup, words, entropyBits } from "../index.js";

const repoList = (name) =>
  readFileSync(new URL(`../../lists/${name}`, import.meta.url), "utf8").split("\n").filter(Boolean).map((l) => l.split("\t"));

test("lists match repo lists and dice numbering", () => {
  for (const [diacritics, name] of [[false, "diceware-pl.txt"], [true, "diceware-pl-ogonki.txt"]]) {
    const rows = repoList(name);
    const list = words({ diacritics });
    assert.equal(list.length, 7776);
    assert.equal(new Set(list).size, 7776);
    rows.forEach(([roll, word], i) => {
      assert.equal(list[i], word);
      assert.equal(lookup(roll, { diacritics }), word);
    });
  }
});

test("plain list has no diacritics", () => {
  assert.ok(!words().some((w) => /[ąćęłńóśźż]/.test(w)));
});

test("generate", () => {
  const parts = generate({ words: 5, separator: "-" }).split("-");
  assert.equal(parts.length, 5);
  parts.forEach((p) => assert.ok(words().includes(p)));
  assert.throws(() => generate({ words: 0 }), RangeError);
  assert.throws(() => lookup("12347"), RangeError);
  assert.equal(Math.round(entropyBits(7)), 90);
});
