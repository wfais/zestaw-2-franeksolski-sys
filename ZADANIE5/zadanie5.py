import numpy as np
import matplotlib.pyplot as plt
from sympy import symbols, sympify, lambdify


def _parsuj_wejscie(wejscie: str):
    expr_part, rest = wejscie.split(",", 1)
    expr = expr_part.strip()
    rest = rest.strip()
    a_str, b_str = rest.split()
    a = float(a_str)
    b = float(b_str)
    return expr, a, b


def rysuj_wielomian(wejscie):
    expr, a, b = _parsuj_wejscie(wejscie)

    x = np.linspace(a, b, 400)

    env = {"x": x, "np": np}
    for name in ["sin", "cos", "tan", "exp", "log", "sqrt"]:
        env[name] = getattr(np, name)

    y = eval(expr, {"__builtins__": {}}, env)

    plt.plot(x, y)
    plt.grid(True)
    plt.xlabel("x")
    plt.ylabel("f(x)")
    plt.title(expr)

    return float(y[0]), float(y[-1])


def rysuj_wielomian_sympy(wejscie):
    expr_str, a, b = _parsuj_wejscie(wejscie)

    x = symbols("x")
    wyrazenie = sympify(expr_str)
    f = lambdify(x, wyrazenie, "numpy")

    xs = np.linspace(a, b, 400)
    ys = f(xs)

    plt.plot(xs, ys)
    plt.grid(True)
    plt.xlabel("x")
    plt.ylabel("f(x)")
    plt.title(str(wyrazenie))

    return float(ys[0]), float(ys[-1])


if __name__ == "__main__":
    wejscie1 = "x**3 + 3*x + 1, -10 10"
    wynik_eval = rysuj_wielomian(wejscie1)
    print("Wynik (eval):", wynik_eval)

    wejscie2 = "x**4 - 5*x**2 + 3*sin(x), -10 10"
    wynik_sympy = rysuj_wielomian_sympy(wejscie2)
    print("Wynik (SymPy):", wynik_sympy)

    plt.show()
