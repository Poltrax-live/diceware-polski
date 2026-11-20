// Polish Diceware word lists (7776 words each) and a passphrase generator.
// Works in browsers and Node.js >= 19 (uses globalThis.crypto.getRandomValues).
import { PLAIN, OGONKI } from "./lists.js";

export const LIST_SIZE = 7776;
export const DEFAULT_WORDS = 7;

const DIGITS = "123456";

/** Word list as an array (no Polish diacritics by default). */
export function words({ diacritics = false } = {}) {
  return diacritics ? OGONKI : PLAIN;
}

/** Uniform random index in [0, n) using rejection sampling. */
function randomIndex(n) {
  const limit = Math.floor(0x100000000 / n) * n;
  const buf = new Uint32Array(1);
  do {
    globalThis.crypto.getRandomValues(buf);
  } while (buf[0] >= limit);
  return buf[0] % n;
}

/** Passphrase of `words` words chosen with a cryptographically secure RNG. */
export function generate({ words: count = DEFAULT_WORDS, diacritics = false, separator = " " } = {}) {
  if (!Number.isInteger(count) || count < 1) throw new RangeError("words must be a positive integer");
  const list = words({ diacritics });
  return Array.from({ length: count }, () => list[randomIndex(list.length)]).join(separator);
}

/** Word for a five-dice roll such as "43136". */
export function lookup(roll, { diacritics = false } = {}) {
  const s = String(roll);
  if (!/^[1-6]{5}$/.test(s)) throw new RangeError("roll must be five digits from 1 to 6");
  let index = 0;
  for (const c of s) index = index * 6 + DIGITS.indexOf(c);
  return words({ diacritics })[index];
}

/** Approximate passphrase strength in bits. */
export function entropyBits(count = DEFAULT_WORDS) {
  return count * Math.log2(LIST_SIZE);
}
