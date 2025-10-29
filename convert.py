
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
def try_decode_bytes(raw_bytes, encodings=("cp1251", "cp1252", "utf-8")):
    errors = []
    for enc in encodings:
        try:
            return enc, raw_bytes.decode(enc, errors="strict")
        except UnicodeDecodeError as e:
            errors.append((enc, str(e)))
    
    return "utf-8", raw_bytes.decode("utf-8", errors="replace")

