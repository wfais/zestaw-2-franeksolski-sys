def dodaj_element(wejscie):
    def max_depth(x):
        if isinstance(x, list) or isinstance(x, tuple):
            if not x:
                return 1
            return 1 + max(max_depth(e) for e in x)
        if isinstance(x, dict):
            if not x:
                return 1
            return 1 + max(max_depth(v) for v in x.values())
        return 1

    deepest = max_depth(wejscie)

    def add_at_depth(x, current_depth, next_value):
        if isinstance(x, list):
            if current_depth == deepest:
                x.append(next_value)
            else:
                for i in range(len(x)):
                    x[i] = add_at_depth(x[i], current_depth + 1, next_value)
        elif isinstance(x, tuple):
            if current_depth == deepest:
                x = list(x)
                x.append(next_value)
                return tuple(x)
            else:
                temp = []
                for e in x:
                    temp.append(add_at_depth(e, current_depth + 1, next_value))
                return tuple(temp)
        elif isinstance(x, dict):
            if current_depth == deepest:

                return x
            for k in x:
                x[k] = add_at_depth(x[k], current_depth + 1, next_value)
        return x

    def max_number(x):
        if isinstance(x, list) or isinstance(x, tuple):
            m = -10**18
            for e in x:
                m = max(m, max_number(e))
            return m
        if isinstance(x, dict):
            m = -10**18
            for v in x.values():
                m = max(m, max_number(v))
            return m
        if isinstance(x, int):
            return x
        return -10**18

    next_value = max_number(wejscie) + 1

    return add_at_depth(wejscie, 1, next_value)


if __name__ == "__main__":
    input_list = [
        1, 2, [3, 4, 5, {"klucz": [5, 6], "tekst": [1, 2]}], 5,
        "hello", 3, [4, 5], (5, (6, (1, [7, 8])))
    ]
    output_list = dodaj_element(input_list)
    print(output_list)
