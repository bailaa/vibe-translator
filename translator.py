# translator.py
import re
import sys
from lexicons import CORP_RULES, ESO_RULES, CORP_PREFIX, CORP_SUFFIX, ESO_PREFIX, ESO_SUFFIX


def apply_rules(text: str, rules) -> str:
    for pattern, repl, case_sensitive in rules:
        flags = 0 if case_sensitive else re.IGNORECASE
        text = re.sub(pattern, repl, text, flags=flags)
    return text


def to_corporate(text: str) -> str:
    body = apply_rules(text, CORP_RULES)
    return CORP_PREFIX + body + CORP_SUFFIX


def to_esoteric(text: str) -> str:
    body = apply_rules(text, ESO_RULES)
    # аккуратно убираем двойные пробелы после удаления «не»
    body = re.sub(r"\s{2,}", " ", body).strip()
    return ESO_PREFIX + body + ESO_SUFFIX


def translate(text: str) -> dict:
    return {
        "corporate": to_corporate(text),
        "esoteric": to_esoteric(text),
    }


if __name__ == "__main__":
    if len(sys.argv) > 1:
        phrase = " ".join(sys.argv[1:])
    else:
        phrase = input("Фраза: ")
    result = translate(phrase)
    print("\n=== Корпоративно-ебланский ===")
    print(result["corporate"])
    print("\n=== Эзотерико-осознанный ===")
    print(result["esoteric"])
  
