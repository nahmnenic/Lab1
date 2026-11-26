"""Лабораторная работа № 2, вариант 27: числа с плавающей запятой.

Регулярное выражение распознаёт числа с плавающей запятой в десятичной записи:
необязательный знак, целая и дробная части через точку или запятую
(допускаются записи 5. и .5), необязательная экспонента (e/E, знак, цифры),
а также целые мантиссы с экспонентой вида 3e8. Целые числа без точки и
экспоненты не считаются числами с плавающей запятой.
"""

import re
import sys

FLOAT_PATTERN = (
    r"(?<![\w.,])[+-]?(?:\d+[.,]\d*|[.,]\d+)(?:[eE][+-]?\d+)?(?![\w]|[.,]\d)"
    r"|(?<![\w.,])[+-]?\d+[eE][+-]?\d+(?![\w]|[.,]\d)"
)

# Шаблон проверки всей строки целиком
FLOAT_FULL_PATTERN = (
    r"[+-]?(?:\d+[.,]\d*|[.,]\d+)(?:[eE][+-]?\d+)?"
    r"|[+-]?\d+[eE][+-]?\d+"
)

FLOAT_RE = re.compile(FLOAT_PATTERN)
FLOAT_FULL_RE = re.compile(FLOAT_FULL_PATTERN)


def is_float(text):
    """Возвращает True, если вся строка является числом с плавающей запятой."""
    return FLOAT_FULL_RE.fullmatch(text.strip()) is not None


def find_floats(text):
    """Возвращает список чисел с плавающей запятой, найденных в тексте."""
    return [match.group(0) for match in FLOAT_RE.finditer(text)]


def find_floats_in_file(path, encoding="utf-8"):
    """Ищет числа с плавающей запятой в текстовом файле."""
    with open(path, "r", encoding=encoding) as file:
        return find_floats(file.read())


def find_floats_in_url(url, timeout=10):
    """Загружает веб-страницу по URL и ищет в её тексте числа с плавающей запятой."""
    response = requests.get(url, timeout=timeout)
    response.raise_for_status()
    return find_floats(response.text)


def main():
    """Интерактивный режим: ввод текста, файл или URL."""
    print("Поиск чисел с плавающей запятой")
    print("1 - ввод текста вручную")
    print("2 - поиск в файле")
    print("3 - поиск на веб-странице по URL")
    choice = input("Выберите режим: ").strip()
    if choice == "1":
        numbers = find_floats(input("Введите текст: "))
    elif choice == "2":
        numbers = find_floats_in_file(input("Путь к файлу: ").strip())
    elif choice == "3":
        numbers = find_floats_in_url(input("URL: ").strip())
    else:
        print("Неизвестный режим", file=sys.stderr)
        return 1
    print("Найдено:", len(numbers))
    for number in numbers:
        print(number)
    return 0


if __name__ == "__main__":
    sys.exit(main())
