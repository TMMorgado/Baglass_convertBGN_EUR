
from decimal import Decimal, ROUND_HALF_UP
import variables as v



#Convert the decimal numbers and use the space width to keep the columns the same as original
def _convert_number_fit_width(num_str: str, width: int) -> str:
    
    dec = len(num_str.split(".", 1)[1]) #count the decimal place
    eur = (Decimal(num_str) / v.BGN_TO_EUR)

    for d in range(dec, -1, -1):
        quant = Decimal(1).scaleb(-d) if d > 0 else Decimal(1)
        rounded = eur.quantize(quant, rounding=ROUND_HALF_UP)
        out = f"{rounded:.{d}f}" if d > 0 else f"{rounded:.0f}"
        if len(out) <= width:
            return out.rjust(width)  
    
    return out.rjust(width)

# assumes FIELD_RE and _convert_number_fit_width already exist
def convert_text_preserving_layout(text: str) -> str:
    out = []
    last = 0
    for m in v.FIELD_RE.finditer(text):
        # copy everything before the match
        out.append(text[last:m.start()])

        left, num, right = m.group(1), m.group(2), m.group(3)
        new_num = _convert_number_fit_width(num, len(num))

        # add the replaced 
        out.append(f"{left}{new_num}{right}")

        last = m.end()

    # tail after the last match
    out.append(text[last:])
    return "".join(out)



#Decode the files
def _looks_like_utf16(raw: bytes) -> str | None:
    # Heuristic: lots of NULs => UTF-16, guess endianness by where NULs appear
    sample = raw[:4096]
    if not sample:
        return None
    le_nulls = sample[1::2].count(0)
    be_nulls = sample[0::2].count(0)
    if le_nulls + be_nulls > 0:  # at least some NULs
        return "utf-16le" if le_nulls >= be_nulls else "utf-16be"
    return None

def _detect_encoding(raw: bytes) -> str:
    # BOMs
    if raw.startswith(b"\xff\xfe"):
        return "utf-16le"
    if raw.startswith(b"\xfe\xff"):
        return "utf-16be"
    if raw.startswith(b"\xef\xbb\xbf"):
        return "utf-8-sig"
    # Heuristic UTF-16 without BOM
    maybe16 = _looks_like_utf16(raw)
    if maybe16:
        return maybe16
    # Try common candidates
    for enc in ("utf-8", "cp1251", "cp1252"):
        try:
            raw.decode(enc, errors="strict")
            return enc
        except UnicodeDecodeError:
            continue
    # Fallback
    return "utf-8"

def try_decode_bytes(raw_bytes: bytes):
    enc = _detect_encoding(raw_bytes)
    text = raw_bytes.decode(enc, errors="strict")
    return enc, text

