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
"""

import os
import sys
import math
import random
import time
import json
import re
from datetime import datetime
from typing import Any, List, Dict, Union, Optional, Callable
from pathlib import Path

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
        "assert": StdAssert
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
    
    print("\n=== Все библиотеки загружены успешно! ===")
    funcs = get_library_functions()
    print(f"Всего доступно функций: {len(funcs)}")
    print("Примеры ключей:", list(funcs.keys())[:10])
