"""
Расширенная библиотека для работы со строками
Предоставляет функции для манипуляции, анализа, форматирования и обработки строк.
Включает поддержку регулярных выражений, кодировок, шаблонизации и многого другого.
"""

import re
import string
import unicodedata
import html
import json
import base64
import hashlib
from typing import List, Dict, Tuple, Optional, Union, Callable, Iterator, Pattern, Any
from functools import lru_cache


# === Константы ===

ASCII_LETTERS = string.ascii_letters
ASCII_LOWERCASE = string.ascii_lowercase
ASCII_UPPERCASE = string.ascii_uppercase
ASCII_DIGITS = string.digits
ASCII_HEX = string.hexdigits
ASCII_OCTAL = string.octdigits
ASCII_PUNCTUATION = string.punctuation
ASCII_WHITESPACE = string.whitespace
ASCII_PRINTABLE = string.printable

# Часто используемые наборы символов
CYRILLIC = 'абвгдеёжзийклмнопрстуфхцчшщъыьэюяАБВГДЕЁЖЗИЙКЛМНОПРСТУФХЦЧШЩЪЫЬЭЮЯ'
CYRILLIC_LOWER = 'абвгдеёжзийклмнопрстуфхцчшщъыьэюя'
CYRILLIC_UPPER = 'АБВГДЕЁЖЗИЙКЛМНОПРСТУФХЦЧШЩЪЫЬЭЮЯ'

# Шаблоны регулярных выражений
EMAIL_PATTERN = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
PHONE_PATTERN = r'^\+?[\d\s\-\(\)]{10,}$'
URL_PATTERN = r'^https?://[^\s]+$'
IPV4_PATTERN = r'^(\d{1,3}\.){3}\d{1,3}$'
IPV6_PATTERN = r'^([0-9a-fA-F]{0,4}:){2,7}[0-9a-fA-F]{0,4}$'
DATE_PATTERN = r'^\d{4}-\d{2}-\d{2}$'
TIME_PATTERN = r'^\d{2}:\d{2}:\d{2}$'
DATETIME_PATTERN = r'^\d{4}-\d{2}-\d{2}[T ]\d{2}:\d{2}:\d{2}'
UUID_PATTERN = r'^[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}$'
HASH_MD5_PATTERN = r'^[0-9a-f]{32}$'
HASH_SHA1_PATTERN = r'^[0-9a-f]{40}$'
HASH_SHA256_PATTERN = r'^[0-9a-f]{64}$'


# === Базовые операции ===

def length(s: str) -> int:
    """Длина строки"""
    return len(s)


def concat(*args: str) -> str:
    """Конкатенация строк"""
    return ''.join(args)


def repeat(s: str, n: int) -> str:
    """Повторить строку n раз"""
    return s * n


def substring(s: str, start: int, end: int = None) -> str:
    """Подстрока от start до end"""
    if end is None:
        return s[start:]
    return s[start:end]


def char_at(s: str, index: int) -> str:
    """Символ по индексу"""
    return s[index]


def slice_string(s: str, indices: List[int]) -> str:
    """Извлечь символы по индексам"""
    return ''.join(s[i] for i in indices if 0 <= i < len(s))


def insert(s: str, index: int, substr: str) -> str:
    """Вставить подстроку в позицию"""
    return s[:index] + substr + s[index:]


def remove(s: str, start: int, end: int = None) -> str:
    """Удалить часть строки"""
    if end is None:
        end = start + 1
    return s[:start] + s[end:]


def reverse(s: str) -> str:
    """Перевернуть строку"""
    return s[::-1]


# === Регистр символов ===

def upper(s: str) -> str:
    """Преобразовать к верхнему регистру"""
    return s.upper()


def lower(s: str) -> str:
    """Преобразовать к нижнему регистру"""
    return s.lower()


def capitalize(s: str) -> str:
    """Первый символ заглавный, остальные строчные"""
    return s.capitalize()


def title(s: str) -> str:
    """Каждое слово с заглавной буквы"""
    return s.title()


def swapcase(s: str) -> str:
    """Поменять регистр на противоположный"""
    return s.swapcase()


def casefold(s: str) -> str:
    """Агрессивное преобразование к нижнему регистру (для сравнения)"""
    return s.casefold()


def is_upper(s: str) -> bool:
    """Все символы в верхнем регистре"""
    return s.isupper()


def is_lower(s: str) -> bool:
    """Все символы в нижнем регистре"""
    return s.islower()


def is_title(s: str) -> bool:
    """Строка в заголовочном регистре"""
    return s.istitle()


def to_camel_case(s: str) -> str:
    """Преобразовать в camelCase"""
    words = re.split(r'[_\-\s]+', s)
    return words[0].lower() + ''.join(word.capitalize() for word in words[1:])


def to_pascal_case(s: str) -> str:
    """Преобразовать в PascalCase"""
    words = re.split(r'[_\-\s]+', s)
    return ''.join(word.capitalize() for word in words)


def to_snake_case(s: str) -> str:
    """Преобразовать в snake_case"""
    s = re.sub(r'([A-Z]+)([A-Z][a-z])', r'\1_\2', s)
    s = re.sub(r'([a-z\d])([A-Z])', r'\1_\2', s)
    s = re.sub(r'[\-\s]+', '_', s)
    return s.lower()


def to_kebab_case(s: str) -> str:
    """Преобразовать в kebab-case"""
    s = re.sub(r'([A-Z]+)([A-Z][a-z])', r'\1-\2', s)
    s = re.sub(r'([a-z\d])([A-Z])', r'\1-\2', s)
    s = re.sub(r'[_\s]+', '-', s)
    return s.lower()


def to_constant_case(s: str) -> str:
    """Преобразовать в CONSTANT_CASE"""
    s = re.sub(r'([A-Z]+)([A-Z][a-z])', r'\1_\2', s)
    s = re.sub(r'([a-z\d])([A-Z])', r'\1_\2', s)
    s = re.sub(r'[\-\s]+', '_', s)
    return s.upper()


# === Поиск и замена ===

def find(s: str, substr: str, start: int = 0, end: int = None) -> int:
    """Найти первую позицию подстроки (-1 если не найдено)"""
    if end is None:
        end = len(s)
    return s.find(substr, start, end)


def rfind(s: str, substr: str, start: int = 0, end: int = None) -> int:
    """Найти последнюю позицию подстроки (-1 если не найдено)"""
    if end is None:
        end = len(s)
    return s.rfind(substr, start, end)


def contains(s: str, substr: str) -> bool:
    """Проверить наличие подстроки"""
    return substr in s


def starts_with(s: str, prefix: str) -> bool:
    """Начинается ли строка с префикса"""
    return s.startswith(prefix)


def ends_with(s: str, suffix: str) -> bool:
    """Заканчивается ли строка суффиксом"""
    return s.endswith(suffix)


def count(s: str, substr: str, start: int = 0, end: int = None) -> int:
    """Количество вхождений подстроки"""
    if end is None:
        end = len(s)
    return s.count(substr, start, end)


def replace(s: str, old: str, new: str, count: int = -1) -> str:
    """Заменить подстроку"""
    if count == -1:
        return s.replace(old, new)
    return s.replace(old, new, count)


def replace_all(s: str, replacements: Dict[str, str]) -> str:
    """Выполнить множественную замену"""
    result = s
    for old, new in replacements.items():
        result = result.replace(old, new)
    return result


def replace_regex(s: str, pattern: str, replacement: str, count: int = 0) -> str:
    """Заменить по регулярному выражению"""
    if count == 0:
        return re.sub(pattern, replacement, s)
    return re.sub(pattern, replacement, s, count=count)


def translate(s: str, table: Dict[str, str]) -> str:
    """Транслитерация по таблице"""
    trans_table = str.maketrans(table)
    return s.translate(trans_table)


# === Разбиение и соединение ===

def split(s: str, sep: str = None, maxsplit: int = -1) -> List[str]:
    """Разбить строку на части"""
    if maxsplit == -1:
        return s.split(sep)
    return s.split(sep, maxsplit)


def rsplit(s: str, sep: str = None, maxsplit: int = -1) -> List[str]:
    """Разбить строку справа"""
    if maxsplit == -1:
        return s.rsplit(sep)
    return s.rsplit(sep, maxsplit)


def splitlines(s: str, keepends: bool = False) -> List[str]:
    """Разбить на строки"""
    return s.splitlines(keepends)


def partition(s: str, sep: str) -> Tuple[str, str, str]:
    """Разбить на три части: до разделителя, разделитель, после"""
    return s.partition(sep)


def rpartition(s: str, sep: str) -> Tuple[str, str, str]:
    """Разбить справа на три части"""
    return s.rpartition(sep)


def join(iterable: List[str], sep: str = '') -> str:
    """Соединить строки разделителем"""
    return sep.join(iterable)


def chunk(s: str, size: int) -> List[str]:
    """Разбить строку на чанки фиксированного размера"""
    return [s[i:i+size] for i in range(0, len(s), size)]


def wrap(s: str, width: int = 70, break_long_words: bool = True) -> List[str]:
    """Обернуть текст в строки указанной ширины"""
    import textwrap
    wrapper = textwrap.TextWrapper(width=width, break_long_words=break_long_words)
    return wrapper.wrap(s)


def fill(s: str, width: int = 70) -> str:
    """Обернуть текст и соединить переносами строк"""
    import textwrap
    return textwrap.fill(s, width=width)


# === Очистка и обрезка ===

def strip(s: str, chars: str = None) -> str:
    """Удалить пробельные символы с обоих концов"""
    return s.strip(chars)


def lstrip(s: str, chars: str = None) -> str:
    """Удалить пробельные символы слева"""
    return s.lstrip(chars)


def rstrip(s: str, chars: str = None) -> str:
    """Удалить пробельные символы справа"""
    return s.rstrip(chars)


def strip_tags(s: str) -> str:
    """Удалить HTML/XML теги"""
    return re.sub(r'<[^>]+>', '', s)


def strip_non_ascii(s: str) -> str:
    """Удалить не ASCII символы"""
    return ''.join(c for c in s if ord(c) < 128)


def strip_non_alpha(s: str) -> str:
    """Оставить только буквы"""
    return ''.join(c for c in s if c.isalpha())


def strip_non_digit(s: str) -> str:
    """Оставить только цифры"""
    return ''.join(c for c in s if c.isdigit())


def strip_non_alnum(s: str) -> str:
    """Оставить только буквы и цифры"""
    return ''.join(c for c in s if c.isalnum())


def remove_whitespace(s: str) -> str:
    """Удалить все пробельные символы"""
    return ''.join(s.split())


def normalize_whitespace(s: str) -> str:
    """Нормализовать пробелы (заменить множественные на одиночные)"""
    return ' '.join(s.split())


def truncate(s: str, length: int, suffix: str = '...') -> str:
    """Обрезать строку до указанной длины с суффиксом"""
    if len(s) <= length:
        return s
    return s[:length - len(suffix)] + suffix


def pad_left(s: str, width: int, fillchar: str = ' ') -> str:
    """Добавить заполнение слева"""
    return s.rjust(width, fillchar)


def pad_right(s: str, width: int, fillchar: str = ' ') -> str:
    """Добавить заполнение справа"""
    return s.ljust(width, fillchar)


def pad_center(s: str, width: int, fillchar: str = ' ') -> str:
    """Центрировать строку с заполнением"""
    return s.center(width, fillchar)


def zero_fill(s: str, width: int) -> str:
    """Заполнить нулями слева (для чисел)"""
    return s.zfill(width)


# === Проверки ===

def is_empty(s: str) -> bool:
    """Строка пустая"""
    return len(s) == 0


def is_not_empty(s: str) -> bool:
    """Строка не пустая"""
    return len(s) > 0


def is_blank(s: str) -> bool:
    """Строка пустая или содержит только пробелы"""
    return len(s.strip()) == 0


def is_alpha(s: str) -> bool:
    """Все символы - буквы"""
    return s.isalpha()


def is_digit(s: str) -> bool:
    """Все символы - цифры"""
    return s.isdigit()


def is_alnum(s: str) -> bool:
    """Все символы - буквы или цифры"""
    return s.isalnum()


def is_space(s: str) -> bool:
    """Все символы - пробельные"""
    return s.isspace()


def is_printable(s: str) -> bool:
    """Все символы печатаемые"""
    return s.isprintable()


def is_decimal(s: str) -> bool:
    """Все символы - десятичные цифры"""
    return s.isdecimal()


def is_numeric(s: str) -> bool:
    """Все символы - числовые"""
    return s.isnumeric()


def is_identifier(s: str) -> bool:
    """Строка является корректным идентификатором"""
    return s.isidentifier()


def is_email(s: str) -> bool:
    """Строка является email адресом"""
    return bool(re.match(EMAIL_PATTERN, s))


def is_phone(s: str) -> bool:
    """Строка является номером телефона"""
    return bool(re.match(PHONE_PATTERN, s))


def is_url(s: str) -> bool:
    """Строка является URL"""
    return bool(re.match(URL_PATTERN, s))


def is_ipv4(s: str) -> bool:
    """Строка является IPv4 адресом"""
    if not re.match(IPV4_PATTERN, s):
        return False
    parts = s.split('.')
    return all(0 <= int(p) <= 255 for p in parts)


def is_ipv6(s: str) -> bool:
    """Строка является IPv6 адресом"""
    return bool(re.match(IPV6_PATTERN, s))


def is_date(s: str) -> bool:
    """Строка является датой в формате YYYY-MM-DD"""
    return bool(re.match(DATE_PATTERN, s))


def is_time(s: str) -> bool:
    """Строка является временем в формате HH:MM:SS"""
    return bool(re.match(TIME_PATTERN, s))


def is_datetime(s: str) -> bool:
    """Строка является датой и временем"""
    return bool(re.match(DATETIME_PATTERN, s))


def is_uuid(s: str) -> bool:
    """Строка является UUID"""
    return bool(re.match(UUID_PATTERN, s, re.IGNORECASE))


def is_hash(s: str, algorithm: str = 'sha256') -> bool:
    """Строка является хешем"""
    patterns = {
        'md5': HASH_MD5_PATTERN,
        'sha1': HASH_SHA1_PATTERN,
        'sha256': HASH_SHA256_PATTERN,
    }
    pattern = patterns.get(algorithm.lower())
    if not pattern:
        return False
    return bool(re.match(pattern, s.lower()))


def is_palindrome(s: str, ignore_case: bool = True, ignore_spaces: bool = True) -> bool:
    """Строка является палиндромом"""
    if ignore_case:
        s = s.lower()
    if ignore_spaces:
        s = s.replace(' ', '')
    return s == s[::-1]


def is_anagram(s1: str, s2: str) -> bool:
    """Строки являются анаграммами"""
    return sorted(s1.lower()) == sorted(s2.lower())


# === Форматирование ===

def format_string(template: str, *args, **kwargs) -> str:
    """Форматировать строку"""
    if args and kwargs:
        return template.format(*args, **kwargs)
    elif args:
        return template.format(*args)
    else:
        return template.format(**kwargs)


def format_number(n: Union[int, float], decimals: int = 2, 
                  thousands_sep: str = ',', decimal_sep: str = '.') -> str:
    """Форматировать число с разделителями"""
    if isinstance(n, int):
        return f"{n:,}".replace(',', thousands_sep)
    
    format_spec = f".{decimals}f"
    formatted = f"{n:{format_spec}}"
    
    if thousands_sep:
        parts = formatted.split('.')
        parts[0] = parts[0].replace(',', thousands_sep)
        formatted = decimal_sep.join(parts)
    elif decimal_sep != '.':
        formatted = formatted.replace('.', decimal_sep)
    
    return formatted


def format_currency(amount: float, currency: str = '$', 
                    decimals: int = 2, locale: str = 'en') -> str:
    """Форматировать сумму как валюту"""
    formatted = format_number(amount, decimals)
    
    if locale == 'ru':
        return f"{formatted} {currency}"
    elif locale == 'en':
        return f"{currency}{formatted}"
    elif locale == 'eu':
        return f"{formatted}{currency}"
    else:
        return f"{currency}{formatted}"


def format_bytes(size: int, precision: int = 2) -> str:
    """Форматировать размер в байтах в человекочитаемый вид"""
    for unit in ['B', 'KB', 'MB', 'GB', 'TB', 'PB']:
        if abs(size) < 1024.0:
            return f"{size:.{precision}f} {unit}"
        size /= 1024.0
    return f"{size:.{precision}f} PB"


def format_percent(value: float, decimals: int = 1, multiply: bool = True) -> str:
    """Форматировать как процент"""
    if multiply:
        value *= 100
    return f"{value:.{decimals}f}%"


def indent(s: str, spaces: int = 4, lines: int = -1) -> str:
    """Добавить отступ к строкам"""
    indent_str = ' ' * spaces
    if lines == -1:
        lines = float('inf')
    
    result_lines = []
    for i, line in enumerate(s.split('\n')):
        if i < lines:
            result_lines.append(indent_str + line)
        else:
            result_lines.append(line)
    
    return '\n'.join(result_lines)


def dedent(s: str) -> str:
    """Удалить общий отступ у всех строк"""
    import textwrap
    return textwrap.dedent(s)


# === Кодировки и хеширование ===

def encode_utf8(s: str) -> bytes:
    """Кодировать в UTF-8"""
    return s.encode('utf-8')


def decode_utf8(b: bytes) -> str:
    """Декодировать из UTF-8"""
    return b.decode('utf-8')


def encode_base64(s: str) -> str:
    """Кодировать в Base64"""
    return base64.b64encode(s.encode('utf-8')).decode('ascii')


def decode_base64(s: str) -> str:
    """Декодировать из Base64"""
    return base64.b64decode(s.encode('ascii')).decode('utf-8')


def url_encode(s: str) -> str:
    """URL-кодировать строку"""
    from urllib.parse import quote
    return quote(s)


def url_decode(s: str) -> str:
    """URL-декодировать строку"""
    from urllib.parse import unquote
    return unquote(s)


def html_encode(s: str) -> str:
    """HTML-экранировать строку"""
    return html.escape(s)


def html_decode(s: str) -> str:
    """HTML-декодировать строку"""
    return html.unescape(s)


def json_encode(obj: Any) -> str:
    """Сериализовать объект в JSON"""
    return json.dumps(obj, ensure_ascii=False)


def json_decode(s: str) -> Any:
    """Десериализовать JSON"""
    return json.loads(s)


def hash_string(s: str, algorithm: str = 'sha256') -> str:
    """Вычислить хеш строки"""
    algorithms = {
        'md5': hashlib.md5,
        'sha1': hashlib.sha1,
        'sha256': hashlib.sha256,
        'sha512': hashlib.sha512,
    }
    
    hasher = algorithms.get(algorithm.lower())
    if not hasher:
        raise ValueError(f"Неизвестный алгоритм: {algorithm}")
    
    return hasher(s.encode('utf-8')).hexdigest()


def hmac_string(s: str, key: str, algorithm: str = 'sha256') -> str:
    """Вычислить HMAC"""
    import hmac
    algorithms = {
        'md5': hashlib.md5,
        'sha1': hashlib.sha1,
        'sha256': hashlib.sha256,
        'sha512': hashlib.sha512,
    }
    
    hasher = algorithms.get(algorithm.lower())
    if not hasher:
        raise ValueError(f"Неизвестный алгоритм: {algorithm}")
    
    return hmac.new(key.encode('utf-8'), s.encode('utf-8'), hasher).hexdigest()


# === Unicode и нормализация ===

def normalize_unicode(s: str, form: str = 'NFC') -> str:
    """Нормализовать Unicode строку"""
    return unicodedata.normalize(form, s)


def is_normalized(s: str, form: str = 'NFC') -> bool:
    """Проверить нормализацию Unicode"""
    return unicodedata.is_normalized(form, s)


def get_char_name(char: str) -> str:
    """Получить название символа Unicode"""
    try:
        return unicodedata.name(char)
    except ValueError:
        return ''


def get_char_category(char: str) -> str:
    """Получить категорию символа Unicode"""
    return unicodedata.category(char)


def combining(char: str) -> int:
    """Получить комбинирующий класс символа"""
    return unicodedata.combining(char)


def digit(char: str, default: int = None) -> int:
    """Получить числовое значение символа"""
    try:
        return unicodedata.digit(char)
    except ValueError:
        return default


def numeric(char: str, default: float = None) -> float:
    """Получить числовое значение символа (float)"""
    try:
        return unicodedata.numeric(char)
    except ValueError:
        return default


def decompose(s: str) -> str:
    """Разложить символы на базовые и комбинирующие"""
    return unicodedata.normalize('NFD', s)


def compose(s: str) -> str:
    """Скомпоновать символы обратно"""
    return unicodedata.normalize('NFC', s)


def remove_accents(s: str) -> str:
    """Удалить диакритические знаки"""
    nfkd_form = unicodedata.normalize('NFKD', s)
    return ''.join(c for c in nfkd_form if not unicodedata.combining(c))


def transliterate_cyrillic(s: str) -> str:
    """Транслитерировать кириллицу в латиницу"""
    mapping = {
        'а': 'a', 'б': 'b', 'в': 'v', 'г': 'g', 'д': 'd', 'е': 'e', 'ё': 'yo',
        'ж': 'zh', 'з': 'z', 'и': 'i', 'й': 'y', 'к': 'k', 'л': 'l', 'м': 'm',
        'н': 'n', 'о': 'o', 'п': 'p', 'р': 'r', 'с': 's', 'т': 't', 'у': 'u',
        'ф': 'f', 'х': 'kh', 'ц': 'ts', 'ч': 'ch', 'ш': 'sh', 'щ': 'shch',
        'ъ': '', 'ы': 'y', 'ь': '', 'э': 'e', 'ю': 'yu', 'я': 'ya',
        'А': 'A', 'Б': 'B', 'В': 'V', 'Г': 'G', 'Д': 'D', 'Е': 'E', 'Ё': 'Yo',
        'Ж': 'Zh', 'З': 'Z', 'И': 'I', 'Й': 'Y', 'К': 'K', 'Л': 'L', 'М': 'M',
        'Н': 'N', 'О': 'O', 'П': 'P', 'Р': 'R', 'С': 'S', 'Т': 'T', 'У': 'U',
        'Ф': 'F', 'Х': 'Kh', 'Ц': 'Ts', 'Ч': 'Ch', 'Ш': 'Sh', 'Щ': 'Shch',
        'Ъ': '', 'Ы': 'Y', 'Ь': '', 'Э': 'E', 'Ю': 'Yu', 'Я': 'Ya',
    }
    return ''.join(mapping.get(c, c) for c in s)


# === Регулярные выражения ===

def match(s: str, pattern: str) -> Optional[re.Match]:
    """Проверить соответствие шаблону в начале строки"""
    return re.match(pattern, s)


def fullmatch(s: str, pattern: str) -> Optional[re.Match]:
    """Проверить полное соответствие шаблону"""
    return re.fullmatch(pattern, s)


def search(s: str, pattern: str) -> Optional[re.Match]:
    """Найти первое совпадение"""
    return re.search(pattern, s)


def findall(s: str, pattern: str) -> List[str]:
    """Найти все совпадения"""
    return re.findall(pattern, s)


def finditer(s: str, pattern: str) -> Iterator[re.Match]:
    """Найти все совпадения с итератором"""
    return re.finditer(pattern, s)


def regex_replace(s: str, pattern: str, replacement: str, count: int = 0) -> str:
    """Заменить по регулярному выражению"""
    return re.sub(pattern, replacement, s, count=count)


def regex_split(s: str, pattern: str, maxsplit: int = 0) -> List[str]:
    """Разбить по регулярному выражению"""
    return re.split(pattern, s, maxsplit)


def escape_regex(s: str) -> str:
    """Экранировать спецсимволы для regex"""
    return re.escape(s)


def compile_regex(pattern: str, flags: int = 0) -> Pattern:
    """Скомпилировать регулярное выражение"""
    return re.compile(pattern, flags)


# === Шаблонизация ===

def template_render(template: str, context: Dict[str, Any]) -> str:
    """Рендерить простой шаблон с {{variable}} синтаксисом"""
    def replace_var(match):
        var_name = match.group(1).strip()
        return str(context.get(var_name, match.group(0)))
    
    return re.sub(r'\{\{([^}]+)\}\}', replace_var, template)


def template_if(condition: bool, true_value: str, false_value: str = '') -> str:
    """Простой условный шаблон"""
    return true_value if condition else false_value


def template_for(items: List[Any], template: str, separator: str = '') -> str:
    """Шаблон для цикла"""
    results = []
    for item in items:
        rendered = template.replace('{{item}}', str(item))
        if isinstance(item, dict):
            for key, value in item.items():
                rendered = rendered.replace(f'{{{{{key}}}}}', str(value))
        results.append(rendered)
    return separator.join(results)


# === Утилиты ===

def levenshtein_distance(s1: str, s2: str) -> int:
    """Расстояние Левенштейна между строками"""
    if len(s1) < len(s2):
        return levenshtein_distance(s2, s1)
    
    if len(s2) == 0:
        return len(s1)
    
    previous_row = range(len(s2) + 1)
    for i, c1 in enumerate(s1):
        current_row = [i + 1]
        for j, c2 in enumerate(s2):
            insertions = previous_row[j + 1] + 1
            deletions = current_row[j] + 1
            substitutions = previous_row[j] + (c1 != c2)
            current_row.append(min(insertions, deletions, substitutions))
        previous_row = current_row
    
    return previous_row[-1]


def similarity(s1: str, s2: str) -> float:
    """Коэффициент схожести строк (0-1)"""
    if not s1 and not s2:
        return 1.0
    max_len = max(len(s1), len(s2))
    if max_len == 0:
        return 1.0
    distance = levenshtein_distance(s1, s2)
    return 1 - distance / max_len


def soundex(s: str) -> str:
    """Алгоритм Soundex для фонетического кодирования"""
    if not s:
        return ''
    
    s = s.upper()
    first_letter = s[0]
    
    # Заменяем буквы на цифры
    mapping = '01230120022455012623010202'
    codes = [first_letter]
    
    for char in s[1:]:
        if char.isalpha():
            code = mapping[ord(char) - ord('A')]
            if code != '0' and code != codes[-1]:
                codes.append(code)
    
    # Удаляем нули и дополняем до 4 символов
    result = ''.join(c for c in codes if c != '0')
    result = (result + '000')[:4]
    
    return first_letter + result[1:]


def generate_random_string(length: int, charset: str = ASCII_LETTERS + ASCII_DIGITS) -> str:
    """Сгенерировать случайную строку"""
    import random
    return ''.join(random.choice(charset) for _ in range(length))


def slugify(s: str, separator: str = '-', lowercase: bool = True) -> str:
    """Создать URL-friendly слаг"""
    s = remove_accents(s)
    if lowercase:
        s = s.lower()
    s = re.sub(r'[^\w\s-]', '', s)
    s = re.sub(r'[-\s]+', separator, s)
    s = s.strip(separator)
    return s


def extract_urls(s: str) -> List[str]:
    """Извлечь все URL из строки"""
    url_pattern = r'https?://[^\s<>"{}|\\^`\[\]]+'
    return re.findall(url_pattern, s)


def extract_emails(s: str) -> List[str]:
    """Извлечь все email адреса из строки"""
    email_pattern = r'[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}'
    return re.findall(email_pattern, s)


def extract_numbers(s: str, as_int: bool = False) -> List[Union[float, int]]:
    """Извлечь все числа из строки"""
    if as_int:
        pattern = r'-?\d+'
        return [int(x) for x in re.findall(pattern, s)]
    else:
        pattern = r'-?\d+(?:\.\d+)?'
        return [float(x) for x in re.findall(pattern, s)]


def extract_hashtags(s: str) -> List[str]:
    """Извлечь все хештеги из строки"""
    return re.findall(r'#\w+', s)


def extract_mentions(s: str) -> List[str]:
    """Извлечь все упоминания (@username) из строки"""
    return re.findall(r'@\w+', s)


# === Экспорт ===

__all__ = [
    # Константы
    'ASCII_LETTERS', 'ASCII_LOWERCASE', 'ASCII_UPPERCASE', 'ASCII_DIGITS',
    'ASCII_HEX', 'ASCII_OCTAL', 'ASCII_PUNCTUATION', 'ASCII_WHITESPACE',
    'ASCII_PRINTABLE', 'CYRILLIC', 'CYRILLIC_LOWER', 'CYRILLIC_UPPER',
    'EMAIL_PATTERN', 'PHONE_PATTERN', 'URL_PATTERN', 'IPV4_PATTERN',
    'IPV6_PATTERN', 'DATE_PATTERN', 'TIME_PATTERN', 'DATETIME_PATTERN',
    'UUID_PATTERN', 'HASH_MD5_PATTERN', 'HASH_SHA1_PATTERN', 'HASH_SHA256_PATTERN',
    
    # Базовые операции
    'length', 'concat', 'repeat', 'substring', 'char_at', 'slice_string',
    'insert', 'remove', 'reverse',
    
    # Регистр
    'upper', 'lower', 'capitalize', 'title', 'swapcase', 'casefold',
    'is_upper', 'is_lower', 'is_title',
    'to_camel_case', 'to_pascal_case', 'to_snake_case', 'to_kebab_case',
    'to_constant_case',
    
    # Поиск и замена
    'find', 'rfind', 'contains', 'starts_with', 'ends_with', 'count',
    'replace', 'replace_all', 'replace_regex', 'translate',
    
    # Разбиение и соединение
    'split', 'rsplit', 'splitlines', 'partition', 'rpartition',
    'join', 'chunk', 'wrap', 'fill',
    
    # Очистка и обрезка
    'strip', 'lstrip', 'rstrip', 'strip_tags', 'strip_non_ascii',
    'strip_non_alpha', 'strip_non_digit', 'strip_non_alnum',
    'remove_whitespace', 'normalize_whitespace', 'truncate',
    'pad_left', 'pad_right', 'pad_center', 'zero_fill',
    
    # Проверки
    'is_empty', 'is_not_empty', 'is_blank', 'is_alpha', 'is_digit',
    'is_alnum', 'is_space', 'is_printable', 'is_decimal', 'is_numeric',
    'is_identifier', 'is_email', 'is_phone', 'is_url', 'is_ipv4',
    'is_ipv6', 'is_date', 'is_time', 'is_datetime', 'is_uuid',
    'is_hash', 'is_palindrome', 'is_anagram',
    
    # Форматирование
    'format_string', 'format_number', 'format_currency', 'format_bytes',
    'format_percent', 'indent', 'dedent',
    
    # Кодировки и хеширование
    'encode_utf8', 'decode_utf8', 'encode_base64', 'decode_base64',
    'url_encode', 'url_decode', 'html_encode', 'html_decode',
    'json_encode', 'json_decode', 'hash_string', 'hmac_string',
    
    # Unicode
    'normalize_unicode', 'is_normalized', 'get_char_name', 'get_char_category',
    'combining', 'digit', 'numeric', 'decompose', 'compose',
    'remove_accents', 'transliterate_cyrillic',
    
    # Регулярные выражения
    'match', 'fullmatch', 'search', 'findall', 'finditer',
    'regex_replace', 'regex_split', 'escape_regex', 'compile_regex',
    
    # Шаблонизация
    'template_render', 'template_if', 'template_for',
    
    # Утилиты
    'levenshtein_distance', 'similarity', 'soundex', 'generate_random_string',
    'slugify', 'extract_urls', 'extract_emails', 'extract_numbers',
    'extract_hashtags', 'extract_mentions',
]
