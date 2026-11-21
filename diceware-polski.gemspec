# frozen_string_literal: true

require_relative "lib/diceware_polski/version"

Gem::Specification.new do |spec|
  spec.name = "diceware-polski"
  spec.version = DicewarePolski::VERSION
  spec.authors = ["Poltrax", "Michał Piórkowski", "Claude.ai"]
  spec.summary = "Polish Diceware word lists (7776 words) and a secure passphrase generator"
  spec.description = "Two full Polish Diceware lists (with and without Polish diacritics) " \
                     "and a tiny SecureRandom-based passphrase generator with a CLI."
  spec.homepage = "https://github.com/Poltrax-live/diceware-polski"
  spec.licenses = ["MIT", "CC-BY-SA-4.0"]
  spec.required_ruby_version = ">= 2.7"
  spec.metadata = {
    "homepage_uri" => "https://poltrax-live.github.io/diceware-polski/",
    "source_code_uri" => spec.homepage,
    "bug_tracker_uri" => "#{spec.homepage}/issues",
    "changelog_uri" => "#{spec.homepage}/releases",
    "rubygems_mfa_required" => "true"
  }
  spec.files = Dir["lib/**/*.rb", "lists/*.txt", "exe/*", "README.md", "LICENSE*"]
  spec.bindir = "exe"
  spec.executables = ["diceware-polski"]
end
