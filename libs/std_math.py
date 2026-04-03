"""
Расширенная математическая библиотека
Предоставляет функции для научных вычислений, статистики, линейной алгебры, комбинаторики и работы с числами.
"""

import math
import random
import cmath
import fractions
import decimal
from typing import List, Tuple, Dict, Any, Optional, Union, Callable, Iterator
from functools import reduce
from collections import defaultdict

# Математические константы с высокой точностью
PI = math.pi
E = math.e
TAU = math.tau  # 2 * PI
PHI = (1 + math.sqrt(5)) / 2  # Золотое сечение
SQRT2 = math.sqrt(2)
SQRT3 = math.sqrt(3)
LN2 = math.log(2)
LN10 = math.log(10)
LOG2E = math.log2(math.e)
LOG10E = math.log10(math.e)

# Бесконечность и NaN
INF = float('inf')
NAN = float('nan')

# Точность вычислений по умолчанию
DEFAULT_PRECISION = 15


def set_precision(precision: int) -> None:
    """Установить точность вычислений для десятичных дробей"""
    decimal.getcontext().prec = precision


def get_precision() -> int:
    """Получить текущую точность вычислений"""
    return decimal.getcontext().prec


# === Тригонометрические функции ===

def sin(x: float, degrees: bool = False) -> float:
    """Синус угла"""
    if degrees:
        x = math.radians(x)
    return math.sin(x)


def cos(x: float, degrees: bool = False) -> float:
    """Косинус угла"""
    if degrees:
        x = math.radians(x)
    return math.cos(x)


def tan(x: float, degrees: bool = False) -> float:
    """Тангенс угла"""
    if degrees:
        x = math.radians(x)
    return math.tan(x)


def cot(x: float, degrees: bool = False) -> float:
    """Котангенс угла"""
    if degrees:
        x = math.radians(x)
    return 1 / math.tan(x)


def sec(x: float, degrees: bool = False) -> float:
    """Секанс угла"""
    if degrees:
        x = math.radians(x)
    return 1 / math.cos(x)


def csc(x: float, degrees: bool = False) -> float:
    """Косеканс угла"""
    if degrees:
        x = math.radians(x)
    return 1 / math.sin(x)


def arcsin(x: float, degrees: bool = False) -> float:
    """Арксинус"""
    result = math.asin(x)
    return math.degrees(result) if degrees else result


def arccos(x: float, degrees: bool = False) -> float:
    """Арккосинус"""
    result = math.acos(x)
    return math.degrees(result) if degrees else result


def arctan(x: float, degrees: bool = False) -> float:
    """Арктангенс"""
    result = math.atan(x)
    return math.degrees(result) if degrees else result


def arctan2(y: float, x: float, degrees: bool = False) -> float:
    """Арктангенс от отношения y/x с учетом квадранта"""
    result = math.atan2(y, x)
    return math.degrees(result) if degrees else result


def sinh(x: float) -> float:
    """Гиперболический синус"""
    return math.sinh(x)


def cosh(x: float) -> float:
    """Гиперболический косинус"""
    return math.cosh(x)


def tanh(x: float) -> float:
    """Гиперболический тангенс"""
    return math.tanh(x)


def coth(x: float) -> float:
    """Гиперболический котангенс"""
    return 1 / math.tanh(x)


def sech(x: float) -> float:
    """Гиперболический секанс"""
    return 1 / math.cosh(x)


def csch(x: float) -> float:
    """Гиперболический косеканс"""
    return 1 / math.sinh(x)


def arcsinh(x: float) -> float:
    """Обратный гиперболический синус"""
    return math.asinh(x)


def arccosh(x: float) -> float:
    """Обратный гиперболический косинус"""
    return math.acosh(x)


def arctanh(x: float) -> float:
    """Обратный гиперболический тангенс"""
    return math.atanh(x)


# === Степенные и логарифмические функции ===

def sqrt(x: float) -> float:
    """Квадратный корень"""
    return math.sqrt(x)


def cbrt(x: float) -> float:
    """Кубический корень"""
    if x < 0:
        return -abs(x) ** (1/3)
    return x ** (1/3)


def pow(base: float, exp: float) -> float:
    """Возведение в степень"""
    return math.pow(base, exp)


def exp(x: float) -> float:
    """Экспонента e^x"""
    return math.exp(x)


def expm1(x: float) -> float:
    """e^x - 1 с высокой точностью для малых x"""
    return math.expm1(x)


def log(x: float, base: float = None) -> float:
    """Логарифм по основанию base (по умолчанию натуральный)"""
    if base is None:
        return math.log(x)
    elif base == 10:
        return math.log10(x)
    elif base == 2:
        return math.log2(x)
    else:
        return math.log(x, base)


def log10(x: float) -> float:
    """Десятичный логарифм"""
    return math.log10(x)


def log2(x: float) -> float:
    """Двоичный логарифм"""
    return math.log2(x)


def log1p(x: float) -> float:
    """ln(1 + x) с высокой точностью для малых x"""
    return math.log1p(x)


def factorial(n: int) -> int:
    """Факториал числа"""
    if n < 0:
        raise ValueError("Факториал определен только для неотрицательных чисел")
    return math.factorial(n)


def double_factorial(n: int) -> int:
    """Двойной факториал n!! = n * (n-2) * (n-4) * ..."""
    if n < 0:
        raise ValueError("Двойной факториал определен только для неотрицательных чисел")
    if n <= 1:
        return 1
    result = 1
    for i in range(n, 0, -2):
        result *= i
    return result


def gamma(x: float) -> float:
    """Гамма-функция (обобщение факториала)"""
    return math.gamma(x)


def lgamma(x: float) -> float:
    """Натуральный логарифм гамма-функции"""
    return math.lgamma(x)


# === Функции округления ===

def floor(x: float) -> int:
    """Округление вниз"""
    return math.floor(x)


def ceil(x: float) -> int:
    """Округление вверх"""
    return math.ceil(x)


def trunc(x: float) -> int:
    """Отсечение дробной части"""
    return math.trunc(x)


def round_to(x: float, decimals: int = 0) -> float:
    """Округление до указанного количества знаков после запятой"""
    multiplier = 10 ** decimals
    return round(x * multiplier) / multiplier


def round_half_up(x: float, decimals: int = 0) -> float:
    """Округление по правилам арифметики (0.5 всегда вверх)"""
    multiplier = 10 ** decimals
    return math.floor(x * multiplier + 0.5) / multiplier


def round_half_even(x: float, decimals: int = 0) -> float:
    """Банковское округление (0.5 к ближайшему четному)"""
    return round(x, decimals)


def clamp(value: float, min_val: float, max_val: float) -> float:
    """Ограничить значение диапазоном [min_val, max_val]"""
    return max(min_val, min(max_val, value))


# === Функции для работы с числами ===

def abs(x: Union[int, float, complex]) -> Union[int, float, complex]:
    """Модуль числа"""
    return abs(x)


def sign(x: float) -> int:
    """Знак числа (-1, 0, или 1)"""
    if x > 0:
        return 1
    elif x < 0:
        return -1
    else:
        return 0


def gcd(a: int, b: int) -> int:
    """Наибольший общий делитель"""
    return math.gcd(abs(a), abs(b))


def lcm(a: int, b: int) -> int:
    """Наименьшее общее кратное"""
    return abs(a * b) // math.gcd(a, b)


def mod(a: float, b: float) -> float:
    """Остаток от деления (всегда неотрицательный)"""
    return a % b


def divmod_int(a: int, b: int) -> Tuple[int, int]:
    """Частное и остаток от целочисленного деления"""
    return divmod(a, b)


def frac(x: float) -> float:
    """Дробная часть числа"""
    return x - math.trunc(x)


def integer_part(x: float) -> int:
    """Целая часть числа"""
    return math.trunc(x)


def is_integer(x: float, tolerance: float = 1e-10) -> bool:
    """Проверить, является ли число целым (с учетом погрешности)"""
    return abs(x - round(x)) < tolerance


def is_rational(x: float, max_denominator: int = 1000000) -> bool:
    """Проверить, можно ли представить число как рациональную дробь"""
    try:
        fractions.Fraction(x).limit_denominator(max_denominator)
        return True
    except:
        return False


def to_rational(x: float, max_denominator: int = 1000000) -> Tuple[int, int]:
    """Преобразовать число в рациональную дробь (числитель, знаменатель)"""
    frac = fractions.Fraction(x).limit_denominator(max_denominator)
    return (frac.numerator, frac.denominator)


def to_decimal(x: Union[int, float, str], precision: int = None) -> decimal.Decimal:
    """Преобразовать число в десятичную дробь с указанной точностью"""
    if precision:
        ctx = decimal.Context(prec=precision)
        return ctx.create_decimal(str(x))
    return decimal.Decimal(str(x))


# === Статистические функции ===

def mean(data: List[float]) -> float:
    """Среднее арифметическое"""
    if not data:
        raise ValueError("Пустой набор данных")
    return sum(data) / len(data)


def geometric_mean(data: List[float]) -> float:
    """Среднее геометрическое"""
    if not data:
        raise ValueError("Пустой набор данных")
    if any(x <= 0 for x in data):
        raise ValueError("Все числа должны быть положительными")
    product = reduce(lambda x, y: x * y, data)
    return product ** (1 / len(data))


def harmonic_mean(data: List[float]) -> float:
    """Среднее гармоническое"""
    if not data:
        raise ValueError("Пустой набор данных")
    if any(x <= 0 for x in data):
        raise ValueError("Все числа должны быть положительными")
    return len(data) / sum(1 / x for x in data)


def median(data: List[float]) -> float:
    """Медиана"""
    if not data:
        raise ValueError("Пустой набор данных")
    sorted_data = sorted(data)
    n = len(sorted_data)
    mid = n // 2
    if n % 2 == 0:
        return (sorted_data[mid - 1] + sorted_data[mid]) / 2
    else:
        return sorted_data[mid]


def mode(data: List[float]) -> List[float]:
    """Мода (одно или несколько наиболее часто встречающихся значений)"""
    if not data:
        raise ValueError("Пустой набор данных")
    counts = defaultdict(int)
    for x in data:
        counts[x] += 1
    max_count = max(counts.values())
    return [x for x, count in counts.items() if count == max_count]


def variance(data: List[float], population: bool = False) -> float:
    """Дисперсия"""
    if not data:
        raise ValueError("Пустой набор данных")
    if len(data) < 2 and not population:
        raise ValueError("Для выборочной дисперсии нужно минимум 2 значения")
    m = mean(data)
    squared_diffs = [(x - m) ** 2 for x in data]
    if population:
        return sum(squared_diffs) / len(data)
    else:
        return sum(squared_diffs) / (len(data) - 1)


def std_dev(data: List[float], population: bool = False) -> float:
    """Стандартное отклонение"""
    return sqrt(variance(data, population))


def percentile(data: List[float], p: float) -> float:
    """Процентиль (p от 0 до 100)"""
    if not data:
        raise ValueError("Пустой набор данных")
    if not 0 <= p <= 100:
        raise ValueError("Процентиль должен быть от 0 до 100")
    sorted_data = sorted(data)
    k = (len(sorted_data) - 1) * p / 100
    f = math.floor(k)
    c = math.ceil(k)
    if f == c:
        return sorted_data[int(k)]
    return sorted_data[int(f)] * (c - k) + sorted_data[int(c)] * (k - f)


def quartile(data: List[float], q: int) -> float:
    """Квартиль (q = 1, 2, или 3)"""
    if q not in [1, 2, 3]:
        raise ValueError("Квартиль должен быть 1, 2, или 3")
    return percentile(data, q * 25)


def iqr(data: List[float]) -> float:
    """Межквартильный размах"""
    return quartile(data, 3) - quartile(data, 1)


def covariance(x: List[float], y: List[float]) -> float:
    """Ковариация двух выборок"""
    if len(x) != len(y):
        raise ValueError("Выборки должны иметь одинаковую длину")
    if len(x) < 2:
        raise ValueError("Нужно минимум 2 значения")
    mean_x = mean(x)
    mean_y = mean(y)
    return sum((xi - mean_x) * (yi - mean_y) for xi, yi in zip(x, y)) / (len(x) - 1)


def correlation(x: List[float], y: List[float]) -> float:
    """Коэффициент корреляции Пирсона"""
    cov = covariance(x, y)
    std_x = std_dev(x)
    std_y = std_dev(y)
    if std_x == 0 or std_y == 0:
        return 0
    return cov / (std_x * std_y)


def z_score(x: float, data: List[float]) -> float:
    """Z-оценка (сколько стандартных отклонений от среднего)"""
    m = mean(data)
    s = std_dev(data)
    if s == 0:
        return 0
    return (x - m) / s


def normalize(data: List[float]) -> List[float]:
    """Нормализация данных к диапазону [0, 1]"""
    if not data:
        raise ValueError("Пустой набор данных")
    min_val = min(data)
    max_val = max(data)
    if max_val == min_val:
        return [0.5] * len(data)
    return [(x - min_val) / (max_val - min_val) for x in data]


def standardize(data: List[float]) -> List[float]:
    """Стандартизация данных (среднее = 0, стд. откл. = 1)"""
    if not data:
        raise ValueError("Пустой набор данных")
    m = mean(data)
    s = std_dev(data)
    if s == 0:
        return [0] * len(data)
    return [(x - m) / s for x in data]


# === Комбинаторика ===

def permutations(n: int, k: int = None) -> int:
    """Количество перестановок из n по k"""
    if k is None:
        k = n
    if k > n or k < 0:
        return 0
    return math.perm(n, k)


def combinations(n: int, k: int) -> int:
    """Количество сочетаний из n по k"""
    if k > n or k < 0:
        return 0
    return math.comb(n, k)


def multinomial(n: int, groups: List[int]) -> int:
    """Мультиномиальный коэффициент"""
    if sum(groups) != n:
        raise ValueError("Сумма групп должна равняться n")
    result = factorial(n)
    for g in groups:
        result //= factorial(g)
    return result


def derangements(n: int) -> int:
    """Количество беспорядков (перестановок без неподвижных точек)"""
    if n < 0:
        return 0
    if n == 0:
        return 1
    if n == 1:
        return 0
    d = [0] * (n + 1)
    d[0] = 1
    d[1] = 0
    for i in range(2, n + 1):
        d[i] = (i - 1) * (d[i - 1] + d[i - 2])
    return d[n]


def catalan(n: int) -> int:
    """Число Каталана"""
    if n < 0:
        return 0
    return combinations(2 * n, n) // (n + 1)


def bell(n: int) -> int:
    """Число Белла (количество разбиений множества)"""
    if n < 0:
        return 0
    bell_triangle = [[0] * (n + 1) for _ in range(n + 1)]
    bell_triangle[0][0] = 1
    for i in range(1, n + 1):
        bell_triangle[i][0] = bell_triangle[i - 1][i - 1]
        for j in range(1, i + 1):
            bell_triangle[i][j] = bell_triangle[i - 1][j - 1] + bell_triangle[i][j - 1]
    return bell_triangle[n][0]


def stirling_second(n: int, k: int) -> int:
    """Число Стирлинга второго рода (разбиения n элементов на k непустых подмножеств)"""
    if k > n or k < 0:
        return 0
    if k == 0:
        return 1 if n == 0 else 0
    dp = [[0] * (k + 1) for _ in range(n + 1)]
    dp[0][0] = 1
    for i in range(1, n + 1):
        for j in range(1, min(i, k) + 1):
            dp[i][j] = j * dp[i - 1][j] + dp[i - 1][j - 1]
    return dp[n][k]


def partitions(n: int) -> int:
    """Количество разбиений числа n на положительные слагаемые"""
    if n < 0:
        return 0
    if n == 0:
        return 1
    p = [0] * (n + 1)
    p[0] = 1
    for i in range(1, n + 1):
        for j in range(i, n + 1):
            p[j] += p[j - i]
    return p[n]


# === Теория чисел ===

def is_prime(n: int) -> bool:
    """Проверка на простоту"""
    if n < 2:
        return False
    if n == 2:
        return True
    if n % 2 == 0:
        return False
    for i in range(3, int(math.sqrt(n)) + 1, 2):
        if n % i == 0:
            return False
    return True


def sieve_of_eratosthenes(limit: int) -> List[int]:
    """Решето Эратосфена - все простые числа до limit"""
    if limit < 2:
        return []
    sieve = [True] * (limit + 1)
    sieve[0] = sieve[1] = False
    for i in range(2, int(math.sqrt(limit)) + 1):
        if sieve[i]:
            for j in range(i * i, limit + 1, i):
                sieve[j] = False
    return [i for i, is_prime in enumerate(sieve) if is_prime]


def prime_factors(n: int) -> List[int]:
    """Простые множители числа"""
    if n < 2:
        return []
    factors = []
    d = 2
    while d * d <= n:
        while n % d == 0:
            factors.append(d)
            n //= d
        d += 1
    if n > 1:
        factors.append(n)
    return factors


def prime_factorization(n: int) -> Dict[int, int]:
    """Разложение на простые множители с показателями степени"""
    if n < 2:
        return {}
    factors = defaultdict(int)
    d = 2
    while d * d <= n:
        while n % d == 0:
            factors[d] += 1
            n //= d
        d += 1
    if n > 1:
        factors[n] += 1
    return dict(factors)


def euler_totient(n: int) -> int:
    """Функция Эйлера φ(n) - количество чисел от 1 до n, взаимно простых с n"""
    if n < 1:
        return 0
    result = n
    p = 2
    while p * p <= n:
        if n % p == 0:
            while n % p == 0:
                n //= p
            result -= result // p
        p += 1
    if n > 1:
        result -= result // n
    return result


def mobius(n: int) -> int:
    """Функция Мёбиуса μ(n)"""
    if n < 1:
        return 0
    if n == 1:
        return 1
    factors = prime_factorization(n)
    if any(exp > 1 for exp in factors.values()):
        return 0
    return (-1) ** len(factors)


def divisor_sum(n: int, power: int = 1) -> int:
    """Сумма делителей числа в степени power"""
    if n < 1:
        return 0
    total = 0
    for i in range(1, int(math.sqrt(n)) + 1):
        if n % i == 0:
            total += i ** power
            if i != n // i:
                total += (n // i) ** power
    return total


def divisor_count(n: int) -> int:
    """Количество делителей числа"""
    if n < 1:
        return 0
    factors = prime_factorization(n)
    count = 1
    for exp in factors.values():
        count *= (exp + 1)
    return count


def is_perfect(n: int) -> bool:
    """Проверка на совершенное число (равно сумме своих собственных делителей)"""
    if n < 2:
        return False
    return divisor_sum(n) - n == n


def is_abundant(n: int) -> bool:
    """Проверка на избыточное число"""
    if n < 2:
        return False
    return divisor_sum(n) - n > n


def is_deficient(n: int) -> bool:
    """Проверка на недостаточное число"""
    if n < 1:
        return False
    return divisor_sum(n) - n < n


def fibonacci(n: int) -> int:
    """N-е число Фибоначчи"""
    if n < 0:
        raise ValueError("n должно быть неотрицательным")
    if n <= 1:
        return n
    a, b = 0, 1
    for _ in range(2, n + 1):
        a, b = b, a + b
    return b


def fibonacci_generator() -> Iterator[int]:
    """Генератор чисел Фибоначчи"""
    a, b = 0, 1
    while True:
        yield a
        a, b = b, a + b


def lucas(n: int) -> int:
    """N-е число Люка"""
    if n < 0:
        raise ValueError("n должно быть неотрицательным")
    if n == 0:
        return 2
    if n == 1:
        return 1
    a, b = 2, 1
    for _ in range(2, n + 1):
        a, b = b, a + b
    return b


def tribonacci(n: int) -> int:
    """N-е число Трибоначчи"""
    if n < 0:
        raise ValueError("n должно быть неотрицательным")
    if n == 0:
        return 0
    if n == 1 or n == 2:
        return 1
    a, b, c = 0, 1, 1
    for _ in range(3, n + 1):
        a, b, c = b, c, a + b + c
    return c


# === Комплексные числа ===

def complex_from_polar(r: float, theta: float, degrees: bool = False) -> complex:
    """Создать комплексное число из полярных координат"""
    if degrees:
        theta = math.radians(theta)
    return r * (math.cos(theta) + 1j * math.sin(theta))


def complex_to_polar(z: complex, degrees: bool = False) -> Tuple[float, float]:
    """Преобразовать комплексное число в полярные координаты (r, theta)"""
    r = abs(z)
    theta = cmath.phase(z)
    if degrees:
        theta = math.degrees(theta)
    return (r, theta)


def complex_conjugate(z: complex) -> complex:
    """Комплексно сопряженное число"""
    return z.conjugate()


def complex_exp(z: complex) -> complex:
    """Экспонента комплексного числа"""
    return cmath.exp(z)


def complex_log(z: complex, base: float = None) -> complex:
    """Логарифм комплексного числа"""
    result = cmath.log(z)
    if base is not None:
        result = result / math.log(base)
    return result


def complex_sqrt(z: complex) -> complex:
    """Квадратный корень комплексного числа"""
    return cmath.sqrt(z)


def complex_sin(z: complex) -> complex:
    """Синус комплексного числа"""
    return cmath.sin(z)


def complex_cos(z: complex) -> complex:
    """Косинус комплексного числа"""
    return cmath.cos(z)


def complex_tan(z: complex) -> complex:
    """Тангенс комплексного числа"""
    return cmath.tan(z)


def complex_asin(z: complex) -> complex:
    """Арксинус комплексного числа"""
    return cmath.asin(z)


def complex_acos(z: complex) -> complex:
    """Арккосинус комплексного числа"""
    return cmath.acos(z)


def complex_atan(z: complex) -> complex:
    """Арктангенс комплексного числа"""
    return cmath.atan(z)


def complex_sinh(z: complex) -> complex:
    """Гиперболический синус комплексного числа"""
    return cmath.sinh(z)


def complex_cosh(z: complex) -> complex:
    """Гиперболический косинус комплексного числа"""
    return cmath.cosh(z)


def complex_tanh(z: complex) -> complex:
    """Гиперболический тангенс комплексного числа"""
    return cmath.tanh(z)


# === Линейная алгебра (базовые операции) ===

def dot_product(v1: List[float], v2: List[float]) -> float:
    """Скалярное произведение векторов"""
    if len(v1) != len(v2):
        raise ValueError("Векторы должны иметь одинаковую длину")
    return sum(a * b for a, b in zip(v1, v2))


def cross_product(v1: List[float], v2: List[float]) -> List[float]:
    """Векторное произведение (только для 3D)"""
    if len(v1) != 3 or len(v2) != 3:
        raise ValueError("Векторное произведение определено только для 3D векторов")
    return [
        v1[1] * v2[2] - v1[2] * v2[1],
        v1[2] * v2[0] - v1[0] * v2[2],
        v1[0] * v2[1] - v1[1] * v2[0]
    ]


def vector_norm(v: List[float], p: int = 2) -> float:
    """Норма вектора (Lp-норма)"""
    if p == float('inf'):
        return max(abs(x) for x in v)
    elif p == 1:
        return sum(abs(x) for x in v)
    else:
        return sum(abs(x) ** p for x in v) ** (1 / p)


def normalize_vector(v: List[float]) -> List[float]:
    """Нормализовать вектор к единичной длине"""
    norm = vector_norm(v)
    if norm == 0:
        return v[:]
    return [x / norm for x in v]


def matrix_multiply(a: List[List[float]], b: List[List[float]]) -> List[List[float]]:
    """Умножение матриц"""
    rows_a, cols_a = len(a), len(a[0])
    rows_b, cols_b = len(b), len(b[0])
    
    if cols_a != rows_b:
        raise ValueError("Несовместимые размеры матриц")
    
    result = [[0] * cols_b for _ in range(rows_a)]
    for i in range(rows_a):
        for j in range(cols_b):
            for k in range(cols_a):
                result[i][j] += a[i][k] * b[k][j]
    
    return result


def matrix_transpose(m: List[List[float]]) -> List[List[float]]:
    """Транспонирование матрицы"""
    if not m:
        return []
    rows, cols = len(m), len(m[0])
    return [[m[i][j] for i in range(rows)] for j in range(cols)]


def matrix_trace(m: List[List[float]]) -> float:
    """След матрицы (сумма диагональных элементов)"""
    if not m or len(m) != len(m[0]):
        raise ValueError("Матрица должна быть квадратной")
    return sum(m[i][i] for i in range(len(m)))


def determinant_2x2(m: List[List[float]]) -> float:
    """Определитель матрицы 2x2"""
    return m[0][0] * m[1][1] - m[0][1] * m[1][0]


def determinant_3x3(m: List[List[float]]) -> float:
    """Определитель матрицы 3x3"""
    return (m[0][0] * (m[1][1] * m[2][2] - m[1][2] * m[2][1])
            - m[0][1] * (m[1][0] * m[2][2] - m[1][2] * m[2][0])
            + m[0][2] * (m[1][0] * m[2][1] - m[1][1] * m[2][0]))


def determinant(m: List[List[float]]) -> float:
    """Определитель матрицы (рекурсивно)"""
    if not m or len(m) != len(m[0]):
        raise ValueError("Матрица должна быть квадратной")
    
    n = len(m)
    if n == 1:
        return m[0][0]
    elif n == 2:
        return determinant_2x2(m)
    elif n == 3:
        return determinant_3x3(m)
    else:
        det = 0
        for j in range(n):
            minor = [[m[i][k] for k in range(n) if k != j] for i in range(1, n)]
            det += ((-1) ** j) * m[0][j] * determinant(minor)
        return det


def identity_matrix(n: int) -> List[List[float]]:
    """Единичная матрица размера n x n"""
    return [[1 if i == j else 0 for j in range(n)] for i in range(n)]


def zero_matrix(rows: int, cols: int) -> List[List[float]]:
    """Нулевая матрица"""
    return [[0] * cols for _ in range(rows)]


def matrix_add(a: List[List[float]], b: List[List[float]]) -> List[List[float]]:
    """Сложение матриц"""
    if len(a) != len(b) or len(a[0]) != len(b[0]):
        raise ValueError("Матрицы должны иметь одинаковые размеры")
    return [[a[i][j] + b[i][j] for j in range(len(a[0]))] for i in range(len(a))]


def matrix_subtract(a: List[List[float]], b: List[List[float]]) -> List[List[float]]:
    """Вычитание матриц"""
    if len(a) != len(b) or len(a[0]) != len(b[0]):
        raise ValueError("Матрицы должны иметь одинаковые размеры")
    return [[a[i][j] - b[i][j] for j in range(len(a[0]))] for i in range(len(a))]


def scalar_multiply(matrix: List[List[float]], scalar: float) -> List[List[float]]:
    """Умножение матрицы на скаляр"""
    return [[scalar * cell for cell in row] for row in matrix]


# === Интерполяция и аппроксимация ===

def linear_interpolate(x0: float, y0: float, x1: float, y1: float, x: float) -> float:
    """Линейная интерполяция"""
    if x1 == x0:
        return y0
    return y0 + (y1 - y0) * (x - x0) / (x1 - x0)


def lerp(a: float, b: float, t: float) -> float:
    """Линейная интерполяция между a и b по параметру t (0 <= t <= 1)"""
    return a + (b - a) * t


def inverse_lerp(a: float, b: float, v: float) -> float:
    """Обратная линейная интерполяция"""
    if b == a:
        return 0
    return (v - a) / (b - a)


def smoothstep(edge0: float, edge1: float, x: float) -> float:
    """Плавная функция шага (интерполяция Hermite)"""
    t = clamp((x - edge0) / (edge1 - edge0), 0, 1)
    return t * t * (3 - 2 * t)


def smootherstep(edge0: float, edge1: float, x: float) -> float:
    """Более плавная функция шага"""
    t = clamp((x - edge0) / (edge1 - edge0), 0, 1)
    return t * t * t * (t * (t * 6 - 15) + 10)


def lagrange_interpolate(points: List[Tuple[float, float]], x: float) -> float:
    """Интерполяция Лагранжа"""
    if not points:
        raise ValueError("Нужно хотя бы одна точка")
    
    result = 0
    n = len(points)
    
    for i in range(n):
        xi, yi = points[i]
        term = yi
        for j in range(n):
            if i != j:
                xj, _ = points[j]
                term *= (x - xj) / (xi - xj)
        result += term
    
    return result


def newton_forward_difference(x_values: List[float], y_values: List[float]) -> List[float]:
    """Вычислить таблицу конечных разностей Ньютона"""
    n = len(x_values)
    diff_table = [y_values[:]]
    
    for level in range(1, n):
        prev = diff_table[-1]
        current = [prev[i + 1] - prev[i] for i in range(len(prev) - 1)]
        diff_table.append(current)
    
    return diff_table


# === Численные методы ===

def numerical_derivative(f: Callable[[float], float], x: float, h: float = 1e-7) -> float:
    """Численное вычисление производной"""
    return (f(x + h) - f(x - h)) / (2 * h)


def numerical_second_derivative(f: Callable[[float], float], x: float, h: float = 1e-5) -> float:
    """Численное вычисление второй производной"""
    return (f(x + h) - 2 * f(x) + f(x - h)) / (h * h)


def numerical_integral(f: Callable[[float], float], a: float, b: float, n: int = 1000) -> float:
    """Численное интегрирование методом трапеций"""
    h = (b - a) / n
    result = 0.5 * (f(a) + f(b))
    for i in range(1, n):
        result += f(a + i * h)
    return result * h


def simpson_integral(f: Callable[[float], float], a: float, b: float, n: int = 100) -> float:
    """Интегрирование методом Симпсона"""
    if n % 2 == 1:
        n += 1
    h = (b - a) / n
    result = f(a) + f(b)
    for i in range(1, n):
        x = a + i * h
        if i % 2 == 0:
            result += 2 * f(x)
        else:
            result += 4 * f(x)
    return result * h / 3


def bisection_method(f: Callable[[float], float], a: float, b: float, 
                     tolerance: float = 1e-10, max_iterations: int = 1000) -> Optional[float]:
    """Метод половинного деления для нахождения корня"""
    if f(a) * f(b) > 0:
        return None
    
    for _ in range(max_iterations):
        c = (a + b) / 2
        if abs(f(c)) < tolerance or (b - a) / 2 < tolerance:
            return c
        if f(a) * f(c) < 0:
            b = c
        else:
            a = c
    
    return (a + b) / 2


def newton_method(f: Callable[[float], float], df: Callable[[float], float], 
                  x0: float, tolerance: float = 1e-10, max_iterations: int = 100) -> Optional[float]:
    """Метод Ньютона для нахождения корня"""
    x = x0
    for _ in range(max_iterations):
        fx = f(x)
        if abs(fx) < tolerance:
            return x
        dfx = df(x)
        if dfx == 0:
            return None
        x = x - fx / dfx
    return None


def fixed_point_iteration(f: Callable[[float], float], x0: float, 
                          tolerance: float = 1e-10, max_iterations: int = 100) -> Optional[float]:
    """Метод простой итерации"""
    x = x0
    for _ in range(max_iterations):
        x_new = f(x)
        if abs(x_new - x) < tolerance:
            return x_new
        x = x_new
    return None


# === Экспорт всех функций ===

__all__ = [
    # Константы
    'PI', 'E', 'TAU', 'PHI', 'SQRT2', 'SQRT3', 'LN2', 'LN10', 'LOG2E', 'LOG10E',
    'INF', 'NAN', 'DEFAULT_PRECISION',
    
    # Управление точностью
    'set_precision', 'get_precision',
    
    # Тригонометрия
    'sin', 'cos', 'tan', 'cot', 'sec', 'csc',
    'arcsin', 'arccos', 'arctan', 'arctan2',
    'sinh', 'cosh', 'tanh', 'coth', 'sech', 'csch',
    'arcsinh', 'arccosh', 'arctanh',
    
    # Степени и логарифмы
    'sqrt', 'cbrt', 'pow', 'exp', 'expm1',
    'log', 'log10', 'log2', 'log1p',
    'factorial', 'double_factorial', 'gamma', 'lgamma',
    
    # Округление
    'floor', 'ceil', 'trunc', 'round_to', 'round_half_up', 
    'round_half_even', 'clamp',
    
    # Работа с числами
    'abs', 'sign', 'gcd', 'lcm', 'mod', 'divmod_int',
    'frac', 'integer_part', 'is_integer', 'is_rational',
    'to_rational', 'to_decimal',
    
    # Статистика
    'mean', 'geometric_mean', 'harmonic_mean', 'median', 'mode',
    'variance', 'std_dev', 'percentile', 'quartile', 'iqr',
    'covariance', 'correlation', 'z_score', 'normalize', 'standardize',
    
    # Комбинаторика
    'permutations', 'combinations', 'multinomial', 'derangements',
    'catalan', 'bell', 'stirling_second', 'partitions',
    
    # Теория чисел
    'is_prime', 'sieve_of_eratosthenes', 'prime_factors', 'prime_factorization',
    'euler_totient', 'mobius', 'divisor_sum', 'divisor_count',
    'is_perfect', 'is_abundant', 'is_deficient',
    'fibonacci', 'fibonacci_generator', 'lucas', 'tribonacci',
    
    # Комплексные числа
    'complex_from_polar', 'complex_to_polar', 'complex_conjugate',
    'complex_exp', 'complex_log', 'complex_sqrt',
    'complex_sin', 'complex_cos', 'complex_tan',
    'complex_asin', 'complex_acos', 'complex_atan',
    'complex_sinh', 'complex_cosh', 'complex_tanh',
    
    # Линейная алгебра
    'dot_product', 'cross_product', 'vector_norm', 'normalize_vector',
    'matrix_multiply', 'matrix_transpose', 'matrix_trace',
    'determinant', 'determinant_2x2', 'determinant_3x3',
    'identity_matrix', 'zero_matrix', 'matrix_add', 'matrix_subtract',
    'scalar_multiply',
    
    # Интерполяция
    'linear_interpolate', 'lerp', 'inverse_lerp',
    'smoothstep', 'smootherstep', 'lagrange_interpolate',
    'newton_forward_difference',
    
    # Численные методы
    'numerical_derivative', 'numerical_second_derivative',
    'numerical_integral', 'simpson_integral',
    'bisection_method', 'newton_method', 'fixed_point_iteration',
]
