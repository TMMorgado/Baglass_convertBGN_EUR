import re
import sys
from typing import List, Tuple

SEP_RE = re.compile(r"( {2,})")  # separadores = sequências de 2+ espaços

def split_fields_and_separators(line: str) -> Tuple[List[str], List[str]]:
    """
    Divide a linha em campos e separadores (2+ espaços).
    - Campos preservam espaços simples internos (ex: 'DS Smith Bulgaria SA').
    - Separadores são apenas os blocos de 2+ espaços entre campos.
    """
    line = line.rstrip("\n")
    parts = SEP_RE.split(line)
    fields = parts[::2]         # índices 0,2,4,... -> campos
    separators = parts[1::2]    # índices 1,3,5,... -> separadores (espaços)
    return fields, separators

def compare_lines(orig_line: str, conv_line: str, line_no: int) -> List[str]:
    errors = []

    # 1) Comprimento total da linha (opcional mas útil)
    if len(orig_line.rstrip("\n")) != len(conv_line.rstrip("\n")):
        errors.append(
            f"[Line {line_no}] total length differs "
            f"(orig={len(orig_line.rstrip())}, conv={len(conv_line.rstrip())})"
        )

    o_fields, o_seps = split_fields_and_separators(orig_line)
    c_fields, c_seps = split_fields_and_separators(conv_line)

    # 2) Mesma contagem de campos e separadores
    if len(o_fields) != len(c_fields):
        errors.append(
            f"[Line {line_no}] field count differs (orig={len(o_fields)}, conv={len(c_fields)})"
        )
        # mesmo que difira, tenta comparar até ao mínimo para dar mais contexto
    if len(o_seps) != len(c_seps):
        errors.append(
            f"[Line {line_no}] separator count differs (orig={len(o_seps)}, conv={len(c_seps)})"
        )

    # 3) Comparar comprimento de cada campo (total de caracteres por campo)
    for i in range(min(len(o_fields), len(c_fields))):
        of, cf = o_fields[i], c_fields[i]
        if len(of) != len(cf):
            # mostra amostras seguras (encurta strings muito longas)
            of_show = of if len(of) <= 60 else of[:57] + "..."
            cf_show = cf if len(cf) <= 60 else cf[:57] + "..."
            errors.append(
                f"[Line {line_no}] field {i+1} width differs "
                f"(orig={len(of)}, conv={len(cf)}) | orig='{of_show}' | conv='{cf_show}'"
            )

    # 4) Comparar nº de espaços entre campos (separadores)
    for i in range(min(len(o_seps), len(c_seps))):
        os_, cs_ = o_seps[i], c_seps[i]
        if len(os_) != len(cs_):
            errors.append(
                f"[Line {line_no}] separator {i+1} spaces differ "
                f"(orig={len(os_)}, conv={len(cs_)})"
            )

    return errors

def compare_files(original_path: str, transformed_path: str) -> int:
    with open(original_path, "r", encoding="utf-8", errors="replace") as fo:
        orig_lines = fo.readlines()
    with open(transformed_path, "r", encoding="utf-8", errors="replace") as fc:
        conv_lines = fc.readlines()

    exit_code = 0
    if len(orig_lines) != len(conv_lines):
        print(f"[File] line count differs (orig={len(orig_lines)}, conv={len(conv_lines)})")
        # continua a comparar até ao mínimo, e marca erro
        exit_code = 1

    for idx in range(min(len(orig_lines), len(conv_lines))):
        errs = compare_lines(orig_lines[idx], conv_lines[idx], idx + 1)
        if errs:
            exit_code = 1
            for e in errs:
                print(e)

    # linhas extra (se existirem)
    if len(orig_lines) > len(conv_lines):
        for i in range(len(conv_lines) + 1, len(orig_lines) + 1):
            print(f"[Line {i}] missing in transformed file")
        exit_code = 1
    elif len(conv_lines) > len(orig_lines):
        for i in range(len(orig_lines) + 1, len(conv_lines) + 1):
            print(f"[Line {i}] extra in transformed file")
        exit_code = 1

    if exit_code == 0:
        print("OK: All lines match in field widths and inter-field spaces.")
    return exit_code

if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Usage: python compare_layout.py <original.txt> <transformed.txt>")
        sys.exit(2)
    sys.exit(compare_files(sys.argv[1], sys.argv[2]))
