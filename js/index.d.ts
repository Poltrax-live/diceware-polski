export declare const LIST_SIZE: 7776;
export declare const DEFAULT_WORDS: 7;
export interface ListOptions { diacritics?: boolean }
export interface GenerateOptions extends ListOptions { words?: number; separator?: string }
export declare function words(options?: ListOptions): readonly string[];
export declare function generate(options?: GenerateOptions): string;
export declare function lookup(roll: string | number, options?: ListOptions): string;
export declare function entropyBits(count?: number): number;
