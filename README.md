# BGN → EUR TXT Converter

Internal tool built for BA Glass Bulgaria to support the transition from BGN (Bulgarian Lev) to EUR.  
It converts financial `.txt` files while keeping the original layout and alignment.

The app is built with **Python** and **Dash**, and runs in GCP.

---

## Overview

This project was developed for the factory in Bulgaria, which will adopt the Euro in January.

The goal is to automate the conversion of existing `.txt` files containing financial data in **BGN** into **EUR**.  
The system reads the original text files, identifies the numeric values representing amounts in BGN, and converts them accurately to EUR while **preserving the original file’s structure and alignment**.

This ensures a seamless transition of all financial records to the new currency standard, without manual editing or format loss.

---

## Key Features

- ✅ Fixed conversion rate: **1 EUR = 1.95583 BGN**
- ✅ Uses Python `Decimal` for precise arithmetic
- ✅ **Decimal-only** replacement (only the numeric amounts are changed)
- ✅ Keeps **all spacing, columns, and layout identical** to the original files
- ✅ Created specifically for:
  - `Prodagbi` `.txt` files  
  - `Pokupki` `.txt` files  
  - `Deklar` `.txt` files
- ✅ Output filename is the same as the original, with `_EUR` appended  
  (e.g. `prodagbi.txt` → `prodagbi_EUR.txt`)

---

## Tech Stack

- **Python**
- **Dash** (web UI)
- **Dash Bootstrap Components**
- **Pandas**
- Standard libraries: `decimal`, `re`, `base64`, `os`

---

## Project Structure

```text
.
├─ app.py          # Dash web application (uploads, UI, downloads)
├─ convert.py      # Conversion logic and text processing
├─ variables.py    # Global constants (BGN→EUR rate, regex pattern)
├─ prodagbi.txt    # Example input file (Prodagbi)
├─ pokupki.txt     # Example input file (Pokupki)
├─ deklar.txt      # Example input file (Deklar)
└─ *_test*.txt     # Extra test files
