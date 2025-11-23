import requests, re, time, sys
from collections import Counter

URL = "https://pl.wikipedia.org/api/rest_v1/page/random/summary"
N = 100
HEADERS = {
    "User-Agent": "wp-edu-wiki-stats/0.1 (kontakt: twoj-email@domena)",
    "Accept": "application/json",
}

WORD_RE = re.compile(r"[^\W\d_]+", re.UNICODE)


def selekcja(text: str):
    text = text.lower()
    words = WORD_RE.findall(text)
    return [w for w in words if len(w) > 3]


def ramka(text: str, width: int = 80) -> str:
    inner = width - 2
    if len(text) > inner:
        text = text[:inner - 1] + "\u2026"
    return f"[{text.center(inner)}]"


def main():
    cnt = Counter()
    licznik_slow = 0
    pobrane = 0

    print(ramka("Start"), end="", flush=True)

    while pobrane < N:
        try:
            data = requests.get(URL, headers=HEADERS, timeout=10).json()
        except Exception:
            time.sleep(0.1)
            continue

        title = data.get("title") or ""
        print("\r" + ramka(title, 80), end="", flush=True)

        extract = data.get("extract") or ""
        lista = selekcja(extract)
        cnt.update(lista)
        licznik_slow += len(lista)
        pobrane += 1

    print()
    print(f"Pobrano: {pobrane}")
    print(f"#Słowa:   {licznik_slow}")
    print(f"Unikalne: {len(cnt)}\n")

    print("Najczęstsze 15 słów:")
    for s, ile in cnt.most_common(15):
        print(f"{s}: {ile}")


if __name__ == "__main__":
    main()
