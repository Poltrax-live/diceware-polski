# Losuje hasło z polskiej listy Diceware (Windows PowerShell 5.1 i PowerShell 7+).
# Użycie:  .\haslo.ps1            -> 7 słów bez polskich znaków
#          .\haslo.ps1 -Slowa 8   -> 8 słów
#          .\haslo.ps1 -Ogonki    -> lista z polskimi znakami
param(
    [int]$Slowa = 7,
    [switch]$Ogonki,
    [string]$Separator = " "
)
$name = if ($Ogonki) { "diceware-pl-ogonki.txt" } else { "diceware-pl.txt" }
$path = Join-Path $PSScriptRoot (Join-Path "lists" $name)
$words = Get-Content -LiteralPath $path -Encoding UTF8 | Where-Object { $_.Trim() } | ForEach-Object { ($_ -split "\s+")[-1] }

# Kryptograficzny generator (nie Get-Random) + odrzucanie, żeby każde słowo miało równe szanse.
$rng = [System.Security.Cryptography.RandomNumberGenerator]::Create()
$bytes = New-Object byte[] 4
$n = [uint64]$words.Count
$limit = [uint64]4294967296 - ([uint64]4294967296 % $n)
$picked = for ($i = 0; $i -lt $Slowa; $i++) {
    do { $rng.GetBytes($bytes); $r = [BitConverter]::ToUInt32($bytes, 0) } while ($r -ge $limit)
    $words[$r % $n]
}
$picked -join $Separator
