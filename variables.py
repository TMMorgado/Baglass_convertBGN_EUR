import re
from decimal import Decimal, getcontext

getcontext().prec = 28  # set the global precision for python decimal math
BGN_TO_EUR = Decimal("1.95583")
FIELD_RE = re.compile(r"(\s*)(-?\d+\.\d+)(\s*)") # Capture (left spaces)(number)(right spaces)