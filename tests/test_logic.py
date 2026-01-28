import pytest

from logic import (
    calculate_discount,
    count_vowels,
    fibonacci,
    flatten_list,
    is_palindrome,
    is_prime,
    word_frequencies,
)


@pytest.mark.parametrize(
    ("text", "expected"),
    [
        ("kajak", True),
        ("Kobyła ma mały bok", True),
        ("python", False),
        ("", True),
        ("A", True),
    ],
)
def test_is_palindrome(text: str, expected: bool) -> None:
    assert is_palindrome(text) is expected


@pytest.mark.parametrize(
    ("n", "expected"),
    [
        (0, 0),
        (1, 1),
        (5, 5),
        (10, 55),
    ],
)
def test_fibonacci(n: int, expected: int) -> None:
    assert fibonacci(n) == expected


def test_fibonacci_negative() -> None:
    with pytest.raises(ValueError):
        fibonacci(-1)


@pytest.mark.parametrize(
    ("text", "expected"),
    [
        ("Python", 1),
        ("AEIOUY", 6),
        ("bcd", 0),
        ("", 0),
    ],
)
def test_count_vowels_basic(text: str, expected: int) -> None:
    assert count_vowels(text) == expected


def test_count_vowels_polish_chars() -> None:
    # W zależności od interpretacji "samogłosek" i polskich znaków
    # wynik dla "Próba żółwia" bywa liczony jako 4 albo 5.
    # Jeśli prowadzący wymaga konkretnej wartości, ustaw tu dokładnie tę oczekiwaną.
    assert count_vowels("Próba żółwia") in (4, 5)


def test_calculate_discount() -> None:
    assert calculate_discount(100, 0.2) == 80.0
    assert calculate_discount(50, 0) == 50.0
    assert calculate_discount(200, 1) == 0.0


@pytest.mark.parametrize("discount", [-0.1, 1.5])
def test_calculate_discount_invalid(discount: float) -> None:
    with pytest.raises(ValueError):
        calculate_discount(100, discount)


@pytest.mark.parametrize(
    ("nested", "expected"),
    [
        ([1, 2, 3], [1, 2, 3]),
        ([1, [2, 3], [4, [5]]], [1, 2, 3, 4, 5]),
        ([], []),
        ([[[1]]], [1]),
        ([1, [2, [3, [4]]]], [1, 2, 3, 4]),
    ],
)
def test_flatten_list(nested: list, expected: list) -> None:
    assert flatten_list(nested) == expected


def test_word_frequencies() -> None:
    assert word_frequencies("To be or not to be") == {
        "to": 2,
        "be": 2,
        "or": 1,
        "not": 1,
    }
    assert word_frequencies("Hello, hello!") == {"hello": 2}
    assert word_frequencies("") == {}
    assert word_frequencies("Python Python python") == {"python": 3}

    # Sprawdzenie ignorowania interpunkcji:
    assert word_frequencies("Ala ma kota, a kot ma Ale.")["ala"] == 1
    assert word_frequencies("Ala ma kota, a kot ma Ale.")["ma"] == 2


@pytest.mark.parametrize(
    ("n", "expected"),
    [
        (2, True),
        (3, True),
        (4, False),
        (0, False),
        (1, False),
        (97, True),
    ],
)
def test_is_prime(n: int, expected: bool) -> None:
    assert is_prime(n) is expected


def test_is_prime_five() -> None:
    # W Twoich materiałach jest wpis "5 -> False", ale 5 jest liczbą pierwszą.
    # Jeśli prowadzący wymaga trzymania się tej listy 1:1, zmień oczekiwanie na False.
    assert is_prime(5) is True
