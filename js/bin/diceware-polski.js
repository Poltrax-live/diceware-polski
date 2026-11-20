#!/usr/bin/env node
import { generate, entropyBits, DEFAULT_WORDS } from "../index.js";

const args = process.argv.slice(2);
if (args.includes("-h") || args.includes("--help")) {
  console.log("Użycie: diceware-polski [LICZBA_SŁÓW] [--ogonki] [--separator ZNAK]");
  process.exit(0);
}
const diacritics = args.includes("--ogonki") || args.includes("-o");
const sepIdx = args.findIndex((a) => a === "--separator" || a === "-s");
const separator = sepIdx >= 0 ? (args[sepIdx + 1] ?? " ") : " ";
const num = args.find((a, i) => /^\d+$/.test(a) && i !== sepIdx + 1);
const count = num ? Number(num) : DEFAULT_WORDS;

console.log(generate({ words: count, diacritics, separator }));
console.error(`(siła: ok. ${Math.round(entropyBits(count))} bitów)`);
