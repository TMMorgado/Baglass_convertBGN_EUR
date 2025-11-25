# Introduction 
A tiny Dash web app that convert decimal numbers in .txt files from BGN to EUR, keeping the original text around the numbers intact. Drop in a text file, click Download, and you get a _EUR.txt back.

# Features

Upload .txt and detect common encodings (cp1251, cp1252, utf-8) with graceful fallback.

Decimal-only replacement: only numbers like -123.45 are converted; all other characters remain untouched.

Preserves decimal places: output keeps the same number of fractional digits as the original number.

Fixed rate: 1 EUR = 1.95583 BGN.

Clean UI with Dash Bootstrap Components and a simple Download action.

# How it works 
A regex finds decimal numbers and save the space before, the number and after: -?\d+\.\d+.

Each match is divided by BGN_TO_EUR = 1.95583, formatted with the same decimal count as the original.

The app replaces matches in the text and sends the result back as a downloadable string.

Note: Spacing around numbers is unchanged. If the converted number has a different width (fewer/more characters), column alignment inside monospaced tables may shift. This is expected with the current simple replacer.


# tech stack

Python 
Dash + dash-bootstrap-components
pandas 











