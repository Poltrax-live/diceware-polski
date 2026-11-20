# frozen_string_literal: true

require "securerandom"
require_relative "diceware_polski/version"

# Polish Diceware word lists (7776 words each) and a passphrase generator.
#
#   DicewarePolski.generate                    # => "kot szyba mleko ..." (7 words, no diacritics)
#   DicewarePolski.generate(words: 8, diacritics: true, separator: "-")
#   DicewarePolski.lookup("43136")             # => word for a five-dice roll
module DicewarePolski
  Error = Class.new(StandardError)

  LIST_SIZE = 7776
  DEFAULT_WORDS = 7
  LISTS_DIR = File.expand_path("../lists", __dir__)
  LIST_FILES = {
    plain: File.join(LISTS_DIR, "diceware-pl.txt"),
    diacritics: File.join(LISTS_DIR, "diceware-pl-ogonki.txt")
  }.freeze

  module_function

  # Returns a passphrase built from words chosen with SecureRandom.
  def generate(words: DEFAULT_WORDS, diacritics: false, separator: " ")
    raise ArgumentError, "words must be a positive integer" unless words.is_a?(Integer) && words.positive?

    list = words_list(diacritics: diacritics)
    Array.new(words) { list[SecureRandom.random_number(list.size)] }.join(separator)
  end

  # Returns the word for a five-dice roll such as "43136".
  def lookup(roll, diacritics: false)
    roll = roll.to_s
    raise ArgumentError, "roll must be five digits from 1 to 6" unless roll.match?(/\A[1-6]{5}\z/)

    dice_table(diacritics: diacritics).fetch(roll)
  end

  # Approximate passphrase strength in bits.
  def entropy_bits(words: DEFAULT_WORDS)
    words * Math.log2(LIST_SIZE)
  end

  def words_list(diacritics: false)
    dice_table(diacritics: diacritics).values
  end

  def dice_table(diacritics: false)
    key = diacritics ? :diacritics : :plain
    @dice_tables ||= {}
    @dice_tables[key] ||= load_table(LIST_FILES.fetch(key))
  end

  def load_table(path)
    table = File.foreach(path, encoding: "UTF-8").each_with_object({}) do |line, acc|
      roll, word = line.split("\t", 2)
      acc[roll] = word.strip.freeze
    end
    raise Error, "#{path}: expected #{LIST_SIZE} words, got #{table.size}" unless table.size == LIST_SIZE

    table.freeze
  end
  private_class_method :load_table
end
