"""
Библиотеки для расширения функционала языка.
Этот модуль содержит реализации стандартных библиотек:
- std.io: Ввод/вывод, файлы
- std.math: Математические функции
- std.str: Обработка строк
- std.collections: Утилиты коллекций
- std.random: Случайные числа
- std.time: Время и даты
- std.sys: Системные функции
- std.json: Парсинг JSON
- std.color: Цветной вывод
- std.assert: Проверки и тесты
- std.crypto: Криптография и кодирование
- std.http: HTTP запросы
- std.csv: Работа с CSV файлами
- std.path: Утилиты путей
- std.validate: Валидация данных
- std.func: Функциональные утилиты
- std.data: Структуры данных (стек, очередь, дек)
"""

import os
import sys
import math
import random
import time
import json
import re
import hashlib
import base64
import hmac
import urllib.request
import urllib.parse
import urllib.error
import csv
import io as python_io
from datetime import datetime, timedelta
from typing import Any, List, Dict, Union, Optional, Callable, Tuple
from pathlib import Path
from collections import deque
from functools import reduce, partial, wraps

# ==============================================================================
# ВСПОМОГАТЕЛЬНЫЕ ТИПЫ И ОШИБКИ
# ==============================================================================

class LibraryError(Exception):
    """Базовое исключение для ошибок библиотек."""
    pass

class FileError(LibraryError):
    pass

class JsonError(LibraryError):
    pass

class CryptoError(LibraryError):
    pass

class HttpError(LibraryError):
    pass

class ValidationError(LibraryError):
    pass

# ==============================================================================
# STD.IO - ВВОД/ВЫВОД И РАБОТА С ФАЙЛАМИ
# ==============================================================================

class StdIo:
    @staticmethod
    def print(*args, sep=' ', end='\n'):
        """Вывод аргументов в консоль."""
        output = sep.join(str(arg) for arg in args)
        sys.stdout.write(output + end)
        sys.stdout.flush()
        return None

    @staticmethod
    def println(*args, sep=' '):
        """Вывод с автоматическим переносом строки."""
        return StdIo.print(*args, sep=sep, end='\n')

    @staticmethod
    def input(prompt=""):
        """Чтение строки ввода от пользователя."""
        try:
            if prompt:
                sys.stdout.write(str(prompt))
                sys.stdout.flush()
            return input()
        except EOFError:
            return ""

    @staticmethod
    def read_file(path: str, encoding: str = "utf-8") -> str:
        """Чтение всего файла в строку."""
        try:
            with open(path, 'r', encoding=encoding) as f:
                return f.read()
        except Exception as e:
            raise FileError(f"Не удалось прочитать файл '{path}': {e}")

    @staticmethod
    def write_file(path: str, content: str, encoding: str = "utf-8", append: bool = False) -> bool:
        """Запись строки в файл."""
        try:
            mode = 'a' if append else 'w'
            with open(path, mode, encoding=encoding) as f:
                f.write(content)
            return True
        except Exception as e:
            raise FileError(f"Не удалось записать в файл '{path}': {e}")

    @staticmethod
    def read_lines(path: str, encoding: str = "utf-8") -> list:
        """Чтение файла в список строк."""
        try:
            with open(path, 'r', encoding=encoding) as f:
                return [line.rstrip('\n') for line in f.readlines()]
        except Exception as e:
            raise FileError(f"Не удалось прочитать строки файла '{path}': {e}")

    @staticmethod
    def write_lines(path: str, lines: list, encoding: str = "utf-8", append: bool = False) -> bool:
        """Запись списка строк в файл."""
        try:
            mode = 'a' if append else 'w'
            with open(path, mode, encoding=encoding) as f:
                for line in lines:
                    f.write(str(line) + '\n')
            return True
        except Exception as e:
            raise FileError(f"Не удалось записать строки в файл '{path}': {e}")

    @staticmethod
    def file_exists(path: str) -> bool:
        """Проверка существования файла."""
        return os.path.isfile(path)

    @staticmethod
    def dir_exists(path: str) -> bool:
        """Проверка существования директории."""
        return os.path.isdir(path)

    @staticmethod
    def make_dir(path: str, parents: bool = False) -> bool:
        """Создание директории."""
        try:
            if parents:
                os.makedirs(path, exist_ok=True)
            else:
                os.mkdir(path)
            return True
        except Exception as e:
            raise FileError(f"Не удалось создать директорию '{path}': {e}")

    @staticmethod
    def remove_file(path: str) -> bool:
        """Удаление файла."""
        try:
            os.remove(path)
            return True
        except Exception as e:
            raise FileError(f"Не удалось удалить файл '{path}': {e}")

    @staticmethod
    def list_dir(path: str = ".") -> list:
        """Список файлов и папок в директории."""
        try:
            return os.listdir(path)
        except Exception as e:
            raise FileError(f"Не удалось прочитать директорию '{path}': {e}")

    @staticmethod
    def get_cwd() -> str:
        """Текущая рабочая директория."""
        return os.getcwd()

    @staticmethod
    def set_cwd(path: str) -> bool:
        """Смена рабочей директории."""
        try:
            os.chdir(path)
            return True
        except Exception as e:
            raise FileError(f"Не удалось сменить директорию на '{path}': {e}")

    @staticmethod
    def get_size(path: str) -> int:
        """Размер файла в байтах."""
        try:
            return os.path.getsize(path)
        except Exception as e:
            raise FileError(f"Не удалось получить размер файла '{path}': {e}")

# ==============================================================================
# STD.MATH - МАТЕМАТИКА
# ==============================================================================

class StdMath:
    PI = math.pi
    E = math.e
    TAU = math.tau
    INF = math.inf
    NAN = math.nan

    @staticmethod
    def abs(x): return abs(x)
    @staticmethod
    def ceil(x): return math.ceil(x)
    @staticmethod
    def floor(x): return math.floor(x)
    @staticmethod
    def round(x, n=0): return round(x, n)
    @staticmethod
    def sqrt(x): return math.sqrt(x)
    @staticmethod
    def cbrt(x): return x ** (1/3)
    @staticmethod
    def pow(x, y): return x ** y
    @staticmethod
    def log(x, base=None): return math.log(x, base) if base else math.log(x)
    @staticmethod
    def log10(x): return math.log10(x)
    @staticmethod
    def log2(x): return math.log2(x)
    @staticmethod
    def exp(x): return math.exp(x)
    
    # Тригонометрия (в радианах)
    @staticmethod
    def sin(x): return math.sin(x)
    @staticmethod
    def cos(x): return math.cos(x)
    @staticmethod
    def tan(x): return math.tan(x)
    @staticmethod
    def asin(x): return math.asin(x)
    @staticmethod
    def acos(x): return math.acos(x)
    @staticmethod
    def atan(x): return math.atan(x)
    @staticmethod
    def atan2(y, x): return math.atan2(y, x)
    
    # Градусы <-> Радианы
    @staticmethod
    def deg(x): return math.degrees(x)
    @staticmethod
    def rad(x): return math.radians(x)

    @staticmethod
    def factorial(n): return math.factorial(int(n))
    @staticmethod
    def gcd(a, b): return math.gcd(int(a), int(b))
    @staticmethod
    def lcm(a, b): return math.lcm(int(a), int(b)) if hasattr(math, 'lcm') else abs(a*b)//math.gcd(int(a), int(b))
    
    @staticmethod
    def is_inf(x): return math.isinf(x)
    @staticmethod
    def is_nan(x): return math.isnan(x)
    @staticmethod
    def clamp(val, min_val, max_val): return max(min_val, min(val, max_val))
    
    @staticmethod
    def sum_list(lst): return sum(lst)
    @staticmethod
    def avg_list(lst): return sum(lst) / len(lst) if lst else 0
    @staticmethod
    def min_list(lst): return min(lst) if lst else None
    @staticmethod
    def max_list(lst): return max(lst) if lst else None
    
    @staticmethod
    def distance_2d(x1, y1, x2, y2):
        return math.sqrt((x2-x1)**2 + (y2-y1)**2)
    
    @staticmethod
    def distance_3d(x1, y1, z1, x2, y2, z2):
        return math.sqrt((x2-x1)**2 + (y2-y1)**2 + (z2-z1)**2)

# ==============================================================================
# STD.STR - ОБРАБОТКА СТРОК
# ==============================================================================

class StdStr:
    @staticmethod
    def len(s): return len(s)
    @staticmethod
    def upper(s): return s.upper()
    @staticmethod
    def lower(s): return s.lower()
    @staticmethod
    def title(s): return s.title()
    @staticmethod
    def capitalize(s): return s.capitalize()
    @staticmethod
    def swapcase(s): return s.swapcase()
    
    @staticmethod
    def strip(s, chars=None): return s.strip(chars)
    @staticmethod
    def lstrip(s, chars=None): return s.lstrip(chars)
    @staticmethod
    def rstrip(s, chars=None): return s.rstrip(chars)
    
    @staticmethod
    def replace(s, old, new, count=-1): return s.replace(old, new, count)
    
    @staticmethod
    def split(s, sep=None, maxsplit=-1): return s.split(sep, maxsplit)
    @staticmethod
    def rsplit(s, sep=None, maxsplit=-1): return s.rsplit(sep, maxsplit)
    @staticmethod
    def join(iterable, sep=""): return sep.join(str(x) for x in iterable)
    
    @staticmethod
    def starts_with(s, prefix): return s.startswith(prefix)
    @staticmethod
    def ends_with(s, suffix): return s.endswith(suffix)
    
    @staticmethod
    def find(s, sub, start=0, end=None): 
        return s.find(sub, start, end)
    
    @staticmethod
    def rfind(s, sub, start=0, end=None): 
        return s.rfind(sub, start, end)
    
    @staticmethod
    def count(s, sub, start=0, end=None): 
        return s.count(sub, start, end)
    
    @staticmethod
    def index_of(s, sub): 
        try: return s.index(sub)
        except ValueError: return -1
    
    @staticmethod
    def contains(s, sub): return sub in s
    
    @staticmethod
    def repeat(s, n): return s * int(n)
    
    @staticmethod
    def reverse(s): return s[::-1]
    
    @staticmethod
    def slice(s, start, end=None): return s[start:end]
    
    @staticmethod
    def pad_left(s, width, char=' '): return s.rjust(width, char)
    @staticmethod
    def pad_right(s, width, char=' '): return s.ljust(width, char)
    @staticmethod
    def pad_center(s, width, char=' '): return s.center(width, char)
    
    @staticmethod
    def is_digit(s): return s.isdigit()
    @staticmethod
    def is_alpha(s): return s.isalpha()
    @staticmethod
    def is_alnum(s): return s.isalnum()
    @staticmethod
    def is_space(s): return s.isspace()
    @staticmethod
    def is_lower(s): return s.islower()
    @staticmethod
    def is_upper(s): return s.isupper()
    
    @staticmethod
    def format(template, *args, **kwargs):
        try:
            # Поддержка позиционных и именованных аргументов
            if kwargs:
                return template.format(**kwargs)
            return template.format(*args)
        except Exception as e:
            raise LibraryError(f"Ошибка форматирования строки: {e}")

    @staticmethod
    def to_int(s, default=0):
        try: return int(s)
        except: return default
    
    @staticmethod
    def to_float(s, default=0.0):
        try: return float(s)
        except: return default

    @staticmethod
    def regex_match(pattern, text):
        match = re.match(pattern, text)
        return match.group(0) if match else None

    @staticmethod
    def regex_find_all(pattern, text):
        return re.findall(pattern, text)

    @staticmethod
    def regex_replace(pattern, text, replacement):
        return re.sub(pattern, replacement, text)

# ==============================================================================
# STD.COLLECTIONS - УТИЛИТЫ КОЛЛЕКЦИЙ
# ==============================================================================

class StdCollections:
    @staticmethod
    def len(arr): return len(arr)
    
    @staticmethod
    def append(arr, item):
        arr.append(item)
        return arr
    
    @staticmethod
    def push(arr, item): return StdCollections.append(arr, item)
    
    @staticmethod
    def pop(arr):
        if arr: return arr.pop()
        return None
    
    @staticmethod
    def shift(arr):
        if arr: return arr.pop(0)
        return None
    
    @staticmethod
    def unshift(arr, item):
        arr.insert(0, item)
        return arr
    
    @staticmethod
    def insert(arr, index, item):
        arr.insert(index, item)
        return arr
    
    @staticmethod
    def remove(arr, item):
        try:
            arr.remove(item)
            return True
        except ValueError:
            return False
    
    @staticmethod
    def clear(arr):
        arr.clear()
        return arr
    
    @staticmethod
    def index_of(arr, item):
        try: return arr.index(item)
        except ValueError: return -1
    
    @staticmethod
    def contains(arr, item): return item in arr
    
    @staticmethod
    def count(arr, item): return arr.count(item)
    
    @staticmethod
    def reverse(arr):
        arr.reverse()
        return arr
    
    @staticmethod
    def sort(arr, reverse=False):
        arr.sort(reverse=reverse)
        return arr
    
    @staticmethod
    def sorted_copy(arr, reverse=False):
        return sorted(arr, reverse=reverse)
    
    @staticmethod
    def sum_list(lst): return sum(lst) if lst else 0
    
    @staticmethod
    def filter_list(arr, func):
        return [x for x in arr if func(x)]
    
    @staticmethod
    def map_list(arr, func):
        return [func(x) for x in arr]
    
    @staticmethod
    def reduce_list(arr, func, initial=None):
        from functools import reduce
        if initial is not None:
            return reduce(func, arr, initial)
        return reduce(func, arr) if arr else None
    
    @staticmethod
    def unique(arr):
        seen = set()
        result = []
        for item in arr:
            if item not in seen:
                seen.add(item)
                result.append(item)
        return result
    
    @staticmethod
    def flatten(arr):
        result = []
        for item in arr:
            if isinstance(item, list):
                result.extend(StdCollections.flatten(item))
            else:
                result.append(item)
        return result
    
    @staticmethod
    def chunk(arr, size):
        return [arr[i:i+size] for i in range(0, len(arr), size)]
    
    @staticmethod
    def zip_lists(*lists):
        return [list(x) for x in zip(*lists)]
    
    # Словари
    @staticmethod
    def dict_keys(d): return list(d.keys())
    @staticmethod
    def dict_values(d): return list(d.values())
    @staticmethod
    def dict_items(d): return list(d.items())
    
    @staticmethod
    def dict_get(d, key, default=None):
        return d.get(key, default)
    
    @staticmethod
    def dict_set(d, key, value):
        d[key] = value
        return d
    
    @staticmethod
    def dict_remove(d, key):
        if key in d:
            del d[key]
            return True
        return False
    
    @staticmethod
    def dict_merge(d1, d2):
        res = d1.copy()
        res.update(d2)
        return res
    
    @staticmethod
    def dict_has(d, key): return key in d
    
    @staticmethod
    def dict_clear(d):
        d.clear()
        return d

# ==============================================================================
# STD.RANDOM - СЛУЧАЙНЫЕ ЧИСЛА
# ==============================================================================

class StdRandom:
    @staticmethod
    def seed(val=None):
        random.seed(val)
    
    @staticmethod
    def int(min_val, max_val):
        return random.randint(int(min_val), int(max_val))
    
    @staticmethod
    def float(min_val=0.0, max_val=1.0):
        return random.uniform(float(min_val), float(max_val))
    
    @staticmethod
    def choice(lst):
        if not lst: return None
        return random.choice(lst)
    
    @staticmethod
    def choices(lst, k=1):
        return random.choices(lst, k=int(k))
    
    @staticmethod
    def shuffle(lst):
        random.shuffle(lst)
        return lst
    
    @staticmethod
    def sample(lst, k):
        return random.sample(lst, min(k, len(lst)))
    
    @staticmethod
    def gauss(mu=0, sigma=1):
        return random.gauss(float(mu), float(sigma))
    
    @staticmethod
    def bool(probability=0.5):
        return random.random() < float(probability)

# ==============================================================================
# STD.TIME - ВРЕМЯ И ДАТЫ
# ==============================================================================

class StdTime:
    @staticmethod
    def now():
        return time.time()
    
    @staticmethod
    def sleep(seconds):
        time.sleep(float(seconds))
    
    @staticmethod
    def timestamp():
        return int(time.time())
    
    @staticmethod
    def date(format_str="%Y-%m-%d"):
        return datetime.now().strftime(format_str)
    
    @staticmethod
    def time(format_str="%H:%M:%S"):
        return datetime.now().strftime(format_str)
    
    @staticmethod
    def datetime(format_str="%Y-%m-%d %H:%M:%S"):
        return datetime.now().strftime(format_str)
    
    @staticmethod
    def parse_date(date_str, format_str="%Y-%m-%d"):
        try:
            dt = datetime.strptime(date_str, format_str)
            return dt.timestamp()
        except Exception:
            return None
    
    @staticmethod
    def format_timestamp(ts, format_str="%Y-%m-%d %H:%M:%S"):
        try:
            return datetime.fromtimestamp(ts).strftime(format_str)
        except Exception:
            return None
    
    @staticmethod
    def year(): return datetime.now().year
    @staticmethod
    def month(): return datetime.now().month
    @staticmethod
    def day(): return datetime.now().day
    @staticmethod
    def hour(): return datetime.now().hour
    @staticmethod
    def minute(): return datetime.now().minute
    @staticmethod
    def second(): return datetime.now().second
    @staticmethod
    def weekday(): return datetime.now().weekday()  # 0 = понедельник

# ==============================================================================
# STD.SYS - СИСТЕМНЫЕ ФУНКЦИИ
# ==============================================================================

class StdSys:
    @staticmethod
    def exit(code=0):
        sys.exit(int(code))
    
    @staticmethod
    def get_args():
        return sys.argv[1:]  # Без имени скрипта
    
    @staticmethod
    def get_env(name, default=None):
        return os.environ.get(name, default)
    
    @staticmethod
    def set_env(name, value):
        os.environ[name] = str(value)
    
    @staticmethod
    def platform():
        return sys.platform
    
    @staticmethod
    def python_version():
        return sys.version
    
    @staticmethod
    def exec_cmd(command):
        import subprocess
        try:
            result = subprocess.run(command, shell=True, capture_output=True, text=True)
            return {
                "code": result.returncode,
                "stdout": result.stdout,
                "stderr": result.stderr
            }
        except Exception as e:
            return {"code": -1, "stdout": "", "stderr": str(e)}
    
    @staticmethod
    def get_pid():
        return os.getpid()

# ==============================================================================
# STD.JSON - РАБОТА С JSON
# ==============================================================================

class StdJson:
    @staticmethod
    def stringify(obj, indent=None) -> str:
        try:
            return json.dumps(obj, ensure_ascii=False, indent=indent)
        except Exception as e:
            raise JsonError(f"Ошибка сериализации JSON: {e}")
    
    @staticmethod
    def parse(json_str) -> Any:
        try:
            return json.loads(json_str)
        except Exception as e:
            raise JsonError(f"Ошибка парсинга JSON: {e}")
    
    @staticmethod
    def read_file(path: str) -> Any:
        content = StdIo.read_file(path)
        return StdJson.parse(content)
    
    @staticmethod
    def write_file(path: str, obj, indent=2) -> bool:
        content = StdJson.stringify(obj, indent=indent)
        return StdIo.write_file(path, content)

# ==============================================================================
# STD.COLOR - ЦВЕТНОЙ ВЫВОД (ANSI)
# ==============================================================================

class StdColor:
    RESET = "\033[0m"
    BOLD = "\033[1m"
    DIM = "\033[2m"
    UNDERLINE = "\033[4m"
    BLINK = "\033[5m"
    REVERSE = "\033[7m"
    HIDDEN = "\033[8m"
    
    # Цвета текста
    BLACK = "\033[30m"
    RED = "\033[31m"
    GREEN = "\033[32m"
    YELLOW = "\033[33m"
    BLUE = "\033[34m"
    MAGENTA = "\033[35m"
    CYAN = "\033[36m"
    WHITE = "\033[37m"
    
    # Яркие цвета
    BRIGHT_RED = "\033[91m"
    BRIGHT_GREEN = "\033[92m"
    BRIGHT_YELLOW = "\033[93m"
    BRIGHT_BLUE = "\033[94m"
    BRIGHT_MAGENTA = "\033[95m"
    BRIGHT_CYAN = "\033[96m"
    BRIGHT_WHITE = "\033[97m"
    
    # Фоны
    BG_BLACK = "\033[40m"
    BG_RED = "\033[41m"
    BG_GREEN = "\033[42m"
    BG_YELLOW = "\033[43m"
    BG_BLUE = "\033[44m"
    BG_MAGENTA = "\033[45m"
    BG_CYAN = "\033[46m"
    BG_WHITE = "\033[47m"

    @staticmethod
    def colorize(text, color_code):
        return f"{color_code}{text}{StdColor.RESET}"
    
    @staticmethod
    def red(text): return StdColor.colorize(text, StdColor.RED)
    @staticmethod
    def green(text): return StdColor.colorize(text, StdColor.GREEN)
    @staticmethod
    def yellow(text): return StdColor.colorize(text, StdColor.YELLOW)
    @staticmethod
    def blue(text): return StdColor.colorize(text, StdColor.BLUE)
    @staticmethod
    def magenta(text): return StdColor.colorize(text, StdColor.MAGENTA)
    @staticmethod
    def cyan(text): return StdColor.colorize(text, StdColor.CYAN)
    @staticmethod
    def white(text): return StdColor.colorize(text, StdColor.WHITE)
    
    @staticmethod
    def bold(text): return StdColor.colorize(text, StdColor.BOLD)
    @staticmethod
    def underline(text): return StdColor.colorize(text, StdColor.UNDERLINE)

# ==============================================================================
# STD.ASSERT - ПРОВЕРКИ И ТЕСТЫ
# ==============================================================================

class StdAssert:
    @staticmethod
    def true(condition, message="Ожидалось True"):
        if not condition:
            raise AssertionError(message)
    
    @staticmethod
    def false(condition, message="Ожидалось False"):
        if condition:
            raise AssertionError(message)
    
    @staticmethod
    def equal(a, b, message=None):
        if a != b:
            msg = message or f"Ожидалось {a} == {b}"
            raise AssertionError(msg)
    
    @staticmethod
    def not_equal(a, b, message=None):
        if a == b:
            msg = message or f"Ожидалось {a} != {b}"
            raise AssertionError(msg)
    
    @staticmethod
    def null(val, message="Ожидалось None"):
        if val is not None:
            raise AssertionError(message)
    
    @staticmethod
    def not_null(val, message="Ожидалось не None"):
        if val is None:
            raise AssertionError(message)
    
    @staticmethod
    def type_is(val, expected_type, message=None):
        if not isinstance(val, expected_type):
            msg = message or f"Ожидался тип {expected_type}, получен {type(val)}"
            raise AssertionError(msg)
    
    @staticmethod
    def raises(func, exception_type=Exception):
        try:
            func()
            raise AssertionError("Ожидалось исключение, но его не было")
        except exception_type:
            pass  # Успех
        except Exception as e:
            raise AssertionError(f"Ожидалось {exception_type}, получено {type(e)}: {e}")

# ==============================================================================
# STD.CRYPTO - КРИПТОГРАФИЯ И КОДИРОВАНИЕ
# ==============================================================================

class StdCrypto:
    @staticmethod
    def md5(text: str) -> str:
        """Вычисляет MD5 хеш строки."""
        return hashlib.md5(text.encode('utf-8')).hexdigest()
    
    @staticmethod
    def sha1(text: str) -> str:
        """Вычисляет SHA1 хеш строки."""
        return hashlib.sha1(text.encode('utf-8')).hexdigest()
    
    @staticmethod
    def sha256(text: str) -> str:
        """Вычисляет SHA256 хеш строки."""
        return hashlib.sha256(text.encode('utf-8')).hexdigest()
    
    @staticmethod
    def sha512(text: str) -> str:
        """Вычисляет SHA512 хеш строки."""
        return hashlib.sha512(text.encode('utf-8')).hexdigest()
    
    @staticmethod
    def hmac_sha256(message: str, key: str) -> str:
        """Вычисляет HMAC-SHA256."""
        return hmac.new(key.encode('utf-8'), message.encode('utf-8'), hashlib.sha256).hexdigest()
    
    @staticmethod
    def base64_encode(data: Union[str, bytes]) -> str:
        """Кодирует в Base64."""
        if isinstance(data, str):
            data = data.encode('utf-8')
        return base64.b64encode(data).decode('utf-8')
    
    @staticmethod
    def base64_decode(data: str) -> str:
        """Декодирует из Base64."""
        return base64.b64decode(data.encode('utf-8')).decode('utf-8')
    
    @staticmethod
    def base64_url_encode(data: Union[str, bytes]) -> str:
        """Кодирует в URL-safe Base64."""
        if isinstance(data, str):
            data = data.encode('utf-8')
        return base64.urlsafe_b64encode(data).decode('utf-8')
    
    @staticmethod
    def base64_url_decode(data: str) -> str:
        """Декодирует из URL-safe Base64."""
        return base64.urlsafe_b64decode(data.encode('utf-8')).decode('utf-8')
    
    @staticmethod
    def hex_encode(data: Union[str, bytes]) -> str:
        """Кодирует в HEX."""
        if isinstance(data, str):
            data = data.encode('utf-8')
        return data.hex()
    
    @staticmethod
    def hex_decode(hex_str: str) -> str:
        """Декодирует из HEX."""
        return bytes.fromhex(hex_str).decode('utf-8')
    
    @staticmethod
    def generate_token(length: int = 32) -> str:
        """Генерирует случайный токен."""
        import secrets
        return secrets.token_hex(length)
    
    @staticmethod
    def secure_compare(a: str, b: str) -> bool:
        """Безопасное сравнение строк (защита от timing attack)."""
        return hmac.compare_digest(a, b)

# ==============================================================================
# STD.HTTP - HTTP ЗАПРОСЫ
# ==============================================================================

class StdHttp:
    @staticmethod
    def get(url: str, headers: Dict[str, str] = None, timeout: int = 30) -> Dict[str, Any]:
        """Выполняет GET запрос."""
        try:
            req = urllib.request.Request(url)
            if headers:
                for key, value in headers.items():
                    req.add_header(key, value)
            with urllib.request.urlopen(req, timeout=timeout) as response:
                return {
                    "status": response.status,
                    "headers": dict(response.headers),
                    "body": response.read().decode('utf-8')
                }
        except urllib.error.HTTPError as e:
            raise HttpError(f"HTTP ошибка: {e.code} - {e.reason}")
        except urllib.error.URLError as e:
            raise HttpError(f"Ошибка соединения: {e.reason}")
    
    @staticmethod
    def post(url: str, data: Union[Dict[str, Any], str] = None, 
             headers: Dict[str, str] = None, timeout: int = 30) -> Dict[str, Any]:
        """Выполняет POST запрос."""
        try:
            if isinstance(data, dict):
                data = urllib.parse.urlencode(data).encode('utf-8')
            elif isinstance(data, str):
                data = data.encode('utf-8')
            
            req = urllib.request.Request(url, data=data, method='POST')
            if headers:
                for key, value in headers.items():
                    req.add_header(key, value)
            else:
                req.add_header('Content-Type', 'application/x-www-form-urlencoded')
            
            with urllib.request.urlopen(req, timeout=timeout) as response:
                return {
                    "status": response.status,
                    "headers": dict(response.headers),
                    "body": response.read().decode('utf-8')
                }
        except urllib.error.HTTPError as e:
            raise HttpError(f"HTTP ошибка: {e.code} - {e.reason}")
        except urllib.error.URLError as e:
            raise HttpError(f"Ошибка соединения: {e.reason}")
    
    @staticmethod
    def download(url: str, save_path: str, timeout: int = 30) -> bool:
        """Скачивает файл по URL."""
        try:
            urllib.request.urlretrieve(url, save_path)
            return True
        except Exception as e:
            raise HttpError(f"Ошибка загрузки: {e}")
    
    @staticmethod
    def url_encode(data: Union[str, Dict]) -> str:
        """Кодирует данные для URL."""
        if isinstance(data, dict):
            return urllib.parse.urlencode(data)
        return urllib.parse.quote(data)
    
    @staticmethod
    def url_decode(url_str: str) -> Dict[str, str]:
        """Декодирует параметры из URL."""
        parsed = urllib.parse.urlparse(url_str)
        return dict(urllib.parse.parse_qsl(parsed.query))
    
    @staticmethod
    def parse_url(url: str) -> Dict[str, Any]:
        """Парсит URL на компоненты."""
        parsed = urllib.parse.urlparse(url)
        return {
            "scheme": parsed.scheme,
            "netloc": parsed.netloc,
            "path": parsed.path,
            "params": parsed.params,
            "query": parsed.query,
            "fragment": parsed.fragment
        }

# ==============================================================================
# STD.CSV - РАБОТА С CSV ФАЙЛАМИ
# ==============================================================================

class StdCsv:
    @staticmethod
    def read_file(path: str, delimiter: str = ',', has_header: bool = True) -> List[Dict[str, Any]]:
        """Читает CSV файл в список словарей."""
        result = []
        with open(path, 'r', encoding='utf-8', newline='') as f:
            reader = csv.DictReader(f, delimiter=delimiter) if has_header else csv.reader(f, delimiter=delimiter)
            if has_header:
                for row in reader:
                    result.append(dict(row))
            else:
                for row in reader:
                    result.append(row)
        return result
    
    @staticmethod
    def write_file(path: str, data: List[Dict[str, Any]], delimiter: str = ',', 
                   include_header: bool = True) -> bool:
        """Записывает список словарей в CSV файл."""
        if not data:
            return False
        fieldnames = list(data[0].keys())
        with open(path, 'w', encoding='utf-8', newline='') as f:
            writer = csv.DictWriter(f, fieldnames=fieldnames, delimiter=delimiter)
            if include_header:
                writer.writeheader()
            writer.writerows(data)
        return True
    
    @staticmethod
    def from_string(csv_str: str, delimiter: str = ',') -> List[List[str]]:
        """Парсит CSV строку в список списков."""
        reader = csv.reader(python_io.StringIO(csv_str), delimiter=delimiter)
        return [row for row in reader]
    
    @staticmethod
    def to_string(data: List[List[str]], delimiter: str = ',') -> str:
        """Конвертирует список списков в CSV строку."""
        output = python_io.StringIO()
        writer = csv.writer(output, delimiter=delimiter)
        writer.writerows(data)
        return output.getvalue()

# ==============================================================================
# STD.PATH - УТИЛИТЫ ПУТЕЙ
# ==============================================================================

class StdPath:
    @staticmethod
    def join(*parts) -> str:
        """Объединяет части пути."""
        return os.path.join(*parts)
    
    @staticmethod
    def normalize(path: str) -> str:
        """Нормализует путь."""
        return os.path.normpath(path)
    
    @staticmethod
    def absolute(path: str) -> str:
        """Возвращает абсолютный путь."""
        return os.path.abspath(path)
    
    @staticmethod
    def relative(path: str, start: str = None) -> str:
        """Возвращает относительный путь."""
        return os.path.relpath(path, start)
    
    @staticmethod
    def dirname(path: str) -> str:
        """Возвращает директорию пути."""
        return os.path.dirname(path)
    
    @staticmethod
    def basename(path: str) -> str:
        """Возвращает имя файла/папки."""
        return os.path.basename(path)
    
    @staticmethod
    def extension(path: str) -> str:
        """Возвращает расширение файла."""
        return os.path.splitext(path)[1]
    
    @staticmethod
    def filename_without_ext(path: str) -> str:
        """Возвращает имя файла без расширения."""
        return os.path.splitext(os.path.basename(path))[0]
    
    @staticmethod
    def exists(path: str) -> bool:
        """Проверяет существование пути."""
        return os.path.exists(path)
    
    @staticmethod
    def is_file(path: str) -> bool:
        """Проверяет, является ли путь файлом."""
        return os.path.isfile(path)
    
    @staticmethod
    def is_dir(path: str) -> bool:
        """Проверяет, является ли путь директорией."""
        return os.path.isdir(path)
    
    @staticmethod
    def is_absolute(path: str) -> bool:
        """Проверяет, является ли путь абсолютным."""
        return os.path.isabs(path)
    
    @staticmethod
    def split(path: str) -> Tuple[str, str]:
        """Разделяет путь на директорию и имя."""
        return os.path.split(path)
    
    @staticmethod
    def split_ext(path: str) -> Tuple[str, str]:
        """Разделяет путь на имя и расширение."""
        return os.path.splitext(path)
    
    @staticmethod
    def walk(directory: str) -> List[Tuple[str, List[str], List[str]]]:
        """Обходит дерево директорий."""
        result = []
        for root, dirs, files in os.walk(directory):
            result.append((root, dirs, files))
        return result
    
    @staticmethod
    def glob(pattern: str) -> List[str]:
        """Находит файлы по шаблону."""
        import glob as glob_module
        return glob_module.glob(pattern)

# ==============================================================================
# STD.VALIDATE - ВАЛИДАЦИЯ ДАННЫХ
# ==============================================================================

class StdValidate:
    @staticmethod
    def is_email(value: str) -> bool:
        """Проверяет, является ли строка email."""
        pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
        return bool(re.match(pattern, value))
    
    @staticmethod
    def is_url(value: str) -> bool:
        """Проверяет, является ли строка URL."""
        pattern = r'^https?://[^\s]+$'
        return bool(re.match(pattern, value))
    
    @staticmethod
    def is_ip(value: str) -> bool:
        """Проверяет, является ли строка IP адресом."""
        pattern = r'^(\d{1,3}\.){3}\d{1,3}$'
        if not re.match(pattern, value):
            return False
        parts = value.split('.')
        return all(0 <= int(p) <= 255 for p in parts)
    
    @staticmethod
    def is_phone(value: str) -> bool:
        """Проверяет, является ли строка телефоном."""
        pattern = r'^\+?[\d\s\-()]{7,20}$'
        return bool(re.match(pattern, value))
    
    @staticmethod
    def is_date(value: str, format_str: str = "%Y-%m-%d") -> bool:
        """Проверяет, является ли строка датой."""
        try:
            datetime.strptime(value, format_str)
            return True
        except ValueError:
            return False
    
    @staticmethod
    def is_numeric(value: Any) -> bool:
        """Проверяет, является ли значение числом."""
        return isinstance(value, (int, float)) and not isinstance(value, bool)
    
    @staticmethod
    def is_integer(value: Any) -> bool:
        """Проверяет, является ли значение целым числом."""
        return isinstance(value, int) and not isinstance(value, bool)
    
    @staticmethod
    def is_float(value: Any) -> bool:
        """Проверяет, является ли значение числом с плавающей точкой."""
        return isinstance(value, float)
    
    @staticmethod
    def is_string(value: Any) -> bool:
        """Проверяет, является ли значение строкой."""
        return isinstance(value, str)
    
    @staticmethod
    def is_boolean(value: Any) -> bool:
        """Проверяет, является ли значение булевым."""
        return isinstance(value, bool)
    
    @staticmethod
    def is_list(value: Any) -> bool:
        """Проверяет, является ли значение списком."""
        return isinstance(value, list)
    
    @staticmethod
    def is_dict(value: Any) -> bool:
        """Проверяет, является ли значение словарем."""
        return isinstance(value, dict)
    
    @staticmethod
    def is_empty(value: Any) -> bool:
        """Проверяет, является ли значение пустым."""
        if value is None:
            return True
        if isinstance(value, (str, list, dict, tuple, set)):
            return len(value) == 0
        return False
    
    @staticmethod
    def in_range(value: Union[int, float], min_val: Union[int, float], 
                 max_val: Union[int, float], inclusive: bool = True) -> bool:
        """Проверяет, находится ли значение в диапазоне."""
        if inclusive:
            return min_val <= value <= max_val
        return min_val < value < max_val
    
    @staticmethod
    def one_of(value: Any, allowed: List[Any]) -> bool:
        """Проверяет, содержится ли значение в списке разрешенных."""
        return value in allowed
    
    @staticmethod
    def length(value: Union[str, list], min_len: int = None, max_len: int = None) -> bool:
        """Проверяет длину строки или списка."""
        l = len(value)
        if min_len is not None and l < min_len:
            return False
        if max_len is not None and l > max_len:
            return False
        return True

# ==============================================================================
# STD.FUNC - ФУНКЦИОНАЛЬНЫЕ УТИЛИТЫ
# ==============================================================================

class StdFunc:
    @staticmethod
    def compose(*functions):
        """Композиция функций (справа налево)."""
        def composed(arg):
            for func in reversed(functions):
                arg = func(arg)
            return arg
        return composed
    
    @staticmethod
    def pipe(*functions):
        """Конвейер функций (слева направо)."""
        def piped(arg):
            for func in functions:
                arg = func(arg)
            return arg
        return piped
    
    @staticmethod
    def curry(func):
        """Каррирование функции."""
        def curried(*args, **kwargs):
            if len(args) + len(kwargs) >= func.__code__.co_argcount:
                return func(*args, **kwargs)
            return lambda *a, **kw: curried(*(args + a), **{**kwargs, **kw})
        return curried
    
    @staticmethod
    def partial(func, *args, **kwargs):
        """Частичное применение функции."""
        return partial(func, *args, **kwargs)
    
    @staticmethod
    def identity(x):
        """Функция тождественности."""
        return x
    
    @staticmethod
    def constant(x):
        """Функция константы."""
        return lambda: x
    
    @staticmethod
    def negate(predicate):
        """Отрицание предиката."""
        return lambda x: not predicate(x)
    
    @staticmethod
    def memoize(func):
        """Мемоизация функции."""
        cache = {}
        def memoized(*args):
            if args not in cache:
                cache[args] = func(*args)
            return cache[args]
        return memoized
    
    @staticmethod
    def debounce(func, wait_seconds: float):
        """Декоратор debouncing для функции."""
        last_call = [0]
        def debounced(*args, **kwargs):
            now = time.time()
            if now - last_call[0] >= wait_seconds:
                last_call[0] = now
                return func(*args, **kwargs)
            return None
        return debounced
    
    @staticmethod
    def throttle(func, interval_seconds: float):
        """Декоратор throttling для функции."""
        last_call = [0]
        def throttled(*args, **kwargs):
            now = time.time()
            if now - last_call[0] >= interval_seconds:
                last_call[0] = now
                return func(*args, **kwargs)
            return None
        return throttled
    
    @staticmethod
    def retry(func, max_attempts: int = 3, delay: float = 1.0):
        """Повторное выполнение функции при ошибке."""
        def retried(*args, **kwargs):
            last_error = None
            for attempt in range(max_attempts):
                try:
                    return func(*args, **kwargs)
                except Exception as e:
                    last_error = e
                    if attempt < max_attempts - 1:
                        time.sleep(delay)
            raise last_error
        return retried

# ==============================================================================
# STD.DATA - СТРУКТУРЫ ДАННЫХ
# ==============================================================================

class Stack:
    """Реализация стека (LIFO)."""
    def __init__(self):
        self._items = []
    
    def push(self, item):
        self._items.append(item)
        return self
    
    def pop(self):
        return self._items.pop() if self._items else None
    
    def peek(self):
        return self._items[-1] if self._items else None
    
    def is_empty(self) -> bool:
        return len(self._items) == 0
    
    def size(self) -> int:
        return len(self._items)
    
    def clear(self):
        self._items.clear()
        return self
    
    def to_list(self) -> list:
        return self._items.copy()

class Queue:
    """Реализация очереди (FIFO)."""
    def __init__(self):
        self._items = deque()
    
    def enqueue(self, item):
        self._items.append(item)
        return self
    
    def dequeue(self):
        return self._items.popleft() if self._items else None
    
    def front(self):
        return self._items[0] if self._items else None
    
    def is_empty(self) -> bool:
        return len(self._items) == 0
    
    def size(self) -> int:
        return len(self._items)
    
    def clear(self):
        self._items.clear()
        return self
    
    def to_list(self) -> list:
        return list(self._items)

class Deque:
    """Реализация двусторонней очереди."""
    def __init__(self):
        self._items = deque()
    
    def push_front(self, item):
        self._items.appendleft(item)
        return self
    
    def push_back(self, item):
        self._items.append(item)
        return self
    
    def pop_front(self):
        return self._items.popleft() if self._items else None
    
    def pop_back(self):
        return self._items.pop() if self._items else None
    
    def front(self):
        return self._items[0] if self._items else None
    
    def back(self):
        return self._items[-1] if self._items else None
    
    def is_empty(self) -> bool:
        return len(self._items) == 0
    
    def size(self) -> int:
        return len(self._items)
    
    def clear(self):
        self._items.clear()
        return self
    
    def to_list(self) -> list:
        return list(self._items)

class StdData:
    """Фабрика структур данных."""
    @staticmethod
    def create_stack() -> Stack:
        return Stack()
    
    @staticmethod
    def create_queue() -> Queue:
        return Queue()
    
    @staticmethod
    def create_deque() -> Deque:
        return Deque()
    
    @staticmethod
    def create_linked_list():
        class Node:
            def __init__(self, value):
                self.value = value
                self.next = None
        
        class LinkedList:
            def __init__(self):
                self.head = None
                self.size = 0
            
            def append(self, value):
                new_node = Node(value)
                if not self.head:
                    self.head = new_node
                else:
                    current = self.head
                    while current.next:
                        current = current.next
                    current.next = new_node
                self.size += 1
                return self
            
            def prepend(self, value):
                new_node = Node(value)
                new_node.next = self.head
                self.head = new_node
                self.size += 1
                return self
            
            def remove(self, value):
                if not self.head:
                    return False
                if self.head.value == value:
                    self.head = self.head.next
                    self.size -= 1
                    return True
                current = self.head
                while current.next:
                    if current.next.value == value:
                        current.next = current.next.next
                        self.size -= 1
                        return True
                    current = current.next
                return False
            
            def contains(self, value) -> bool:
                current = self.head
                while current:
                    if current.value == value:
                        return True
                    current = current.next
                return False
            
            def to_list(self) -> list:
                result = []
                current = self.head
                while current:
                    result.append(current.value)
                    current = current.next
                return result
        
        return LinkedList()

# ==============================================================================
# РЕГИСТРАЦИЯ БИБЛИОТЕК
# ==============================================================================

def get_all_libraries():
    """Возвращает словарь всех доступных библиотек."""
    return {
        "io": StdIo,
        "math": StdMath,
        "str": StdStr,
        "collections": StdCollections,
        "random": StdRandom,
        "time": StdTime,
        "sys": StdSys,
        "json": StdJson,
        "color": StdColor,
        "assert": StdAssert,
        "crypto": StdCrypto,
        "http": StdHttp,
        "csv": StdCsv,
        "path": StdPath,
        "validate": StdValidate,
        "func": StdFunc,
        "data": StdData
    }

def get_library_functions():
    """
    Возвращает плоский словарь всех функций библиотек.
    Ключи имеют вид: "io.print", "math.sqrt", etc.
    Это удобно для прямой регистрации в интерпретаторе.
    """
    libs = get_all_libraries()
    functions = {}
    
    for lib_name, lib_class in libs.items():
        for attr_name in dir(lib_class):
            if not attr_name.startswith('_'):
                attr = getattr(lib_class, attr_name)
                if callable(attr):
                    functions[f"{lib_name}.{attr_name}"] = attr
                else:
                    # Константы (как math.PI)
                    functions[f"{lib_name}.{attr_name}"] = attr
                    
    return functions

# Для быстрой проверки при запуске напрямую
if __name__ == "__main__":
    print("=== Тест библиотек ===")
    
    # Тест IO
    StdIo.print("Привет, ", "мир!", sep="", end="!\n")
    
    # Тест Math
    print(f"PI = {StdMath.PI}, Sqrt(16) = {StdMath.sqrt(16)}")
    
    # Тест Str
    s = "  Hello World  "
    print(f"Upper: '{StdStr.upper(s)}', Trimmed: '{StdStr.strip(s)}'")
    
    # Тест Collections
    arr = [1, 2, 3, 4, 5]
    StdCollections.append(arr, 6)
    print(f"Array: {arr}, Sum: {StdCollections.sum_list(arr)}")
    
    # Тест Random
    StdRandom.seed(42)
    print(f"Random Int: {StdRandom.int(1, 100)}, Choice: {StdRandom.choice(['a', 'b', 'c'])}")
    
    # Тест Time
    print(f"Current DateTime: {StdTime.datetime()}")
    
    # Тест Color
    print(f"{StdColor.red('Red')} {StdColor.green('Green')} {StdColor.blue('Blue')}")
    
    # Тест JSON
    data = {"name": "Test", "value": 123}
    json_str = StdJson.stringify(data)
    print(f"JSON: {json_str}")
    parsed = StdJson.parse(json_str)
    print(f"Parsed: {parsed}")
    
    # Тест Assert
    try:
        StdAssert.equal(2+2, 4)
        print("Assert OK: 2+2 == 4")
        StdAssert.true(True)
        print("Assert OK: True is True")
    except AssertionError as e:
        print(f"Assert Failed: {e}")
    
    # Тест Crypto
    print(f"\nCrypto SHA256: {StdCrypto.sha256('test')}")
    print(f"Crypto Base64: {StdCrypto.base64_encode('hello')}")
    
    # Тест Validate
    print(f"\nValidate Email: {StdValidate.is_email('test@example.com')}")
    print(f"Validate URL: {StdValidate.is_url('https://example.com')}")
    
    # Тест Func
    double = lambda x: x * 2
    add_one = lambda x: x + 1
    composed = StdFunc.compose(double, add_one)
    print(f"\nFunc Compose (3): {composed(3)}")
    
    # Тест Data
    stack = StdData.create_stack()
    stack.push(1).push(2).push(3)
    print(f"\nData Stack pop: {stack.pop()}")
    
    queue = StdData.create_queue()
    queue.enqueue("a").enqueue("b")
    print(f"Data Queue dequeue: {queue.dequeue()}")

    print("\n=== Все библиотеки загружены успешно! ===")
    funcs = get_library_functions()
    print(f"Всего доступно функций: {len(funcs)}")
    print("Примеры ключей:", list(funcs.keys())[:15])
