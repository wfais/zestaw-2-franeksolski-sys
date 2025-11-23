import os
import time
import threading
import sys

LICZBA_KROKOW = 80_000_000
LICZBA_WATKOW = sorted({1, 2, 4, os.cpu_count() or 4})


def policz_fragment_pi(pocz: int, kon: int, krok: float, wyniki: list[float], indeks: int) -> None:
    s = 0.0
    for i in range(pocz, kon):
        x = (i + 0.5) * krok
        s += 4.0 / (1.0 + x * x)
    wyniki[indeks] = s * krok


def main():
    print(f"Python: {sys.version.split()[0]}  (tryb bez GIL? {getattr(sys, '_is_gil_enabled', lambda: None)() is False})")
    print(f"Liczba rdzeni logicznych CPU: {os.cpu_count()}")
    print(f"LICZBA_KROKOW: {LICZBA_KROKOW}\n")

    krok = 1.0 / LICZBA_KROKOW
    wyniki = [0.0]
    w = threading.Thread(target=policz_fragment_pi, args=(0, LICZBA_KROKOW, krok, wyniki, 0))
    w.start()
    w.join()

    print("Pomiary czasu dla różnych liczby wątków:")
    t_jeden = None

    for n_watkow in LICZBA_WATKOW:
        rozmiar_podstawowy = LICZBA_KROKOW // n_watkow
        reszta = LICZBA_KROKOW % n_watkow

        wyniki = [0.0] * n_watkow
        watki: list[threading.Thread] = []

        start = time.perf_counter()

        pocz = 0
        for i in range(n_watkow):
            dl = rozmiar_podstawowy + (1 if i < reszta else 0)
            kon = pocz + dl
            t = threading.Thread(
                target=policz_fragment_pi,
                args=(pocz, kon, krok, wyniki, i),
            )
            watki.append(t)
            t.start()
            pocz = kon

        for t in watki:
            t.join()

        pi_approx = sum(wyniki)
        elapsed = time.perf_counter() - start

        if t_jeden is None and n_watkow == 1:
            t_jeden = elapsed

        if t_jeden is not None:
            speedup = t_jeden / elapsed if elapsed > 0 else float("inf")
        else:
            speedup = 1.0

        print(f"{n_watkow:2d} wątków: pi ≈ {pi_approx:.9f}, czas: {elapsed:.3f} s, przyspieszenie: {speedup:.2f}x")


if __name__ == "__main__":
    main()
