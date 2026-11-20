# frozen_string_literal: true

require "minitest/autorun"
require_relative "../lib/diceware_polski"

class DicewarePolskiTest < Minitest::Test
  DIACRITICS = /[ąćęłńóśźż]/.freeze

  def test_lists_have_unique_words_and_full_dice_range
    [false, true].each do |diacritics|
      table = DicewarePolski.dice_table(diacritics: diacritics)
      assert_equal 7776, table.size
      assert_equal 7776, table.values.uniq.size
      assert_equal "11111", table.keys.first
      assert_equal "66666", table.keys.last
      table.each_value { |w| assert_match(/\A[a-ząćęłńóśźż]{3,9}\z/, w) }
    end
  end

  def test_plain_list_has_no_diacritics
    refute DicewarePolski.words_list.any? { |w| w.match?(DIACRITICS) }
  end

  def test_generate
    phrase = DicewarePolski.generate(words: 5, separator: "-")
    words = phrase.split("-")
    assert_equal 5, words.size
    words.each { |w| assert_includes DicewarePolski.words_list, w }
  end

  def test_lookup
    assert_equal DicewarePolski.words_list.first, DicewarePolski.lookup(11111)
    assert_raises(ArgumentError) { DicewarePolski.lookup("12347") }
  end

  def test_rejects_bad_word_count
    assert_raises(ArgumentError) { DicewarePolski.generate(words: 0) }
  end
end
