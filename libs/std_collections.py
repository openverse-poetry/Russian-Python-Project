"""
Библиотека для работы с коллекциями (списки, словари, множества)
Предоставляет расширенные функции для манипуляции, фильтрации, преобразования и анализа коллекций.
"""

import random
import itertools
import operator
from typing import List, Dict, Tuple, Set, Any, Optional, Union, Callable, Iterator, Iterable
from collections import defaultdict, Counter, OrderedDict, deque
from functools import reduce, cmp_to_key


# === Создание коллекций ===

def list_create(size: int, value: Any = None) -> List[Any]:
    """Создать список заданного размера"""
    return [value] * size


def list_range(start: int, stop: int = None, step: int = 1) -> List[int]:
    """Создать список чисел в диапазоне"""
    if stop is None:
        stop = start
        start = 0
    return list(range(start, stop, step))


def dict_create(keys: List[Any], values: List[Any] = None, default: Any = None) -> Dict[Any, Any]:
    """Создать словарь из ключей и значений"""
    if values is None:
        return {k: default for k in keys}
    return dict(zip(keys, values))


def set_create(iterable: Iterable = None) -> Set[Any]:
    """Создать множество"""
    if iterable is None:
        return set()
    return set(iterable)


def tuple_create(*args) -> Tuple:
    """Создать кортеж"""
    return tuple(args)


# === Базовые операции со списками ===

def append(lst: List, item: Any) -> List:
    """Добавить элемент в конец списка"""
    lst.append(item)
    return lst


def prepend(lst: List, item: Any) -> List:
    """Добавить элемент в начало списка"""
    lst.insert(0, item)
    return lst


def insert(lst: List, index: int, item: Any) -> List:
    """Вставить элемент по индексу"""
    lst.insert(index, item)
    return lst


def remove(lst: List, item: Any) -> List:
    """Удалить первое вхождение элемента"""
    lst.remove(item)
    return lst


def pop(lst: List, index: int = -1) -> Any:
    """Удалить и вернуть элемент по индексу"""
    return lst.pop(index)


def clear(lst: List) -> List:
    """Очистить список"""
    lst.clear()
    return lst


def extend(lst: List, items: Iterable) -> List:
    """Расширить список элементами из итерируемого объекта"""
    lst.extend(items)
    return lst


def copy_list(lst: List) -> List:
    """Создать копию списка"""
    return lst[:]


def reverse_list(lst: List) -> List:
    """Перевернуть список (in-place)"""
    lst.reverse()
    return lst


def reversed_copy(lst: List) -> List:
    """Вернуть перевернутую копию списка"""
    return lst[::-1]


def rotate_left(lst: List, n: int = 1) -> List:
    """Повернуть список влево на n позиций"""
    if not lst:
        return lst
    n = n % len(lst)
    return lst[n:] + lst[:n]


def rotate_right(lst: List, n: int = 1) -> List:
    """Повернуть список вправо на n позиций"""
    if not lst:
        return lst
    n = n % len(lst)
    return lst[-n:] + lst[:-n]


def swap(lst: List, i: int, j: int) -> List:
    """Поменять местами элементы по индексам"""
    lst[i], lst[j] = lst[j], lst[i]
    return lst


def shuffle(lst: List) -> List:
    """Перемешать список (in-place)"""
    random.shuffle(lst)
    return lst


def shuffled_copy(lst: List) -> List:
    """Вернуть перемешанную копию списка"""
    result = lst[:]
    random.shuffle(result)
    return result


# === Доступ к элементам ===

def first(lst: List, default: Any = None) -> Any:
    """Получить первый элемент"""
    return lst[0] if lst else default


def last(lst: List, default: Any = None) -> Any:
    """Получить последний элемент"""
    return lst[-1] if lst else default


def nth(lst: List, n: int, default: Any = None) -> Any:
    """Получить n-й элемент (с поддержкой отрицательных индексов)"""
    if -len(lst) <= n < len(lst):
        return lst[n]
    return default


def get_slice(lst: List, start: int, end: int = None, step: int = 1) -> List:
    """Получить срез списка"""
    return lst[start:end:step]


def take(lst: List, n: int) -> List:
    """Взять первые n элементов"""
    return lst[:n]


def take_last(lst: List, n: int) -> List:
    """Взять последние n элементов"""
    return lst[-n:] if n > 0 else []


def drop(lst: List, n: int) -> List:
    """Отбросить первые n элементов"""
    return lst[n:]


def drop_last(lst: List, n: int) -> List:
    """Отбросить последние n элементов"""
    return lst[:-n] if n > 0 else lst[:]


def head(lst: List) -> Any:
    """Получить первый элемент (head)"""
    return lst[0] if lst else None


def tail(lst: List) -> List:
    """Получить все элементы кроме первого (tail)"""
    return lst[1:] if lst else []


def init(lst: List) -> List:
    """Получить все элементы кроме последнего"""
    return lst[:-1] if lst else []


# === Поиск и фильтрация ===

def find(lst: List, predicate: Callable[[Any], bool], default: Any = None) -> Any:
    """Найти первый элемент, удовлетворяющий условию"""
    for item in lst:
        if predicate(item):
            return item
    return default


def find_index(lst: List, predicate: Callable[[Any], bool], default: int = -1) -> int:
    """Найти индекс первого элемента, удовлетворяющего условию"""
    for i, item in enumerate(lst):
        if predicate(item):
            return i
    return default


def find_all(lst: List, predicate: Callable[[Any], bool]) -> List[Any]:
    """Найти все элементы, удовлетворяющие условию"""
    return [item for item in lst if predicate(item)]


def find_indices(lst: List, predicate: Callable[[Any], bool]) -> List[int]:
    """Найти индексы всех элементов, удовлетворяющих условию"""
    return [i for i, item in enumerate(lst) if predicate(item)]


def contains(lst: List, item: Any) -> bool:
    """Проверить наличие элемента"""
    return item in lst


def contains_any(lst: List, items: List) -> bool:
    """Проверить наличие любого из элементов"""
    return any(item in lst for item in items)


def contains_all(lst: List, items: List) -> bool:
    """Проверить наличие всех элементов"""
    return all(item in lst for item in items)


def index_of(lst: List, item: Any, start: int = 0) -> int:
    """Найти индекс элемента (-1 если не найден)"""
    try:
        return lst.index(item, start)
    except ValueError:
        return -1


def rindex_of(lst: List, item: Any) -> int:
    """Найти последний индекс элемента (-1 если не найден)"""
    try:
        return len(lst) - 1 - lst[::-1].index(item)
    except ValueError:
        return -1


def count(lst: List, item: Any) -> int:
    """Подсчитать количество вхождений элемента"""
    return lst.count(item)


def count_if(lst: List, predicate: Callable[[Any], bool]) -> int:
    """Подсчитать количество элементов, удовлетворяющих условию"""
    return sum(1 for item in lst if predicate(item))


# === Фильтрация ===

def filter_list(lst: List, predicate: Callable[[Any], bool]) -> List[Any]:
    """Отфильтровать элементы по условию"""
    return [item for item in lst if predicate(item)]


def reject(lst: List, predicate: Callable[[Any], bool]) -> List[Any]:
    """Отбросить элементы, удовлетворяющие условию"""
    return [item for item in lst if not predicate(item)]


def filter_none(lst: List) -> List[Any]:
    """Удалить None значения"""
    return [item for item in lst if item is not None]


def filter_false(lst: List) -> List[Any]:
    """Удалить ложные значения (None, False, 0, '', [], {})"""
    return [item for item in lst if item]


def unique(lst: List) -> List[Any]:
    """Удалить дубликаты (сохраняя порядок)"""
    seen = set()
    result = []
    for item in lst:
        if item not in seen:
            seen.add(item)
            result.append(item)
    return result


def unique_by(lst: List, key: Callable[[Any], Any]) -> List[Any]:
    """Удалить дубликаты по ключу"""
    seen = set()
    result = []
    for item in lst:
        k = key(item)
        if k not in seen:
            seen.add(k)
            result.append(item)
    return result


def distinct(lst: List) -> List[Any]:
    """Получить уникальные элементы (через множество)"""
    return list(set(lst))


# === Преобразование ===

def map_list(lst: List, func: Callable[[Any], Any]) -> List[Any]:
    """Преобразовать каждый элемент"""
    return [func(item) for item in lst]


def map_with_index(lst: List, func: Callable[[Any, int], Any]) -> List[Any]:
    """Преобразовать каждый элемент с индексом"""
    return [func(item, i) for i, item in enumerate(lst)]


def flat_map(lst: List, func: Callable[[Any], List]) -> List[Any]:
    """Преобразовать и сплющить результат"""
    result = []
    for item in lst:
        result.extend(func(item))
    return result


def flatten(lst: List) -> List[Any]:
    """Сплющить одноуровневый список"""
    result = []
    for item in lst:
        if isinstance(item, list):
            result.extend(item)
        else:
            result.append(item)
    return result


def flatten_deep(lst: List, depth: int = -1) -> List[Any]:
    """Рекурсивно сплющить список"""
    result = []
    for item in lst:
        if isinstance(item, list) and (depth == -1 or depth > 0):
            new_depth = depth - 1 if depth > 0 else -1
            result.extend(flatten_deep(item, new_depth))
        else:
            result.append(item)
    return result


def zip_lists(*lists: List) -> List[Tuple]:
    """Объединить несколько списков в кортежи"""
    return list(zip(*lists))


def unzip(pairs: List[Tuple]) -> Tuple[List, ...]:
    """Разделить список кортежей на отдельные списки"""
    if not pairs:
        return ()
    return tuple(list(x) for x in zip(*pairs))


def chunk(lst: List, size: int) -> List[List[Any]]:
    """Разбить список на чанки фиксированного размера"""
    return [lst[i:i+size] for i in range(0, len(lst), size)]


def partition(lst: List, predicate: Callable[[Any], bool]) -> Tuple[List[Any], List[Any]]:
    """Разделить список на две части по условию"""
    true_items = []
    false_items = []
    for item in lst:
        if predicate(item):
            true_items.append(item)
        else:
            false_items.append(item)
    return true_items, false_items


def group_by(lst: List, key: Callable[[Any], Any]) -> Dict[Any, List[Any]]:
    """Сгруппировать элементы по ключу"""
    result = defaultdict(list)
    for item in lst:
        result[key(item)].append(item)
    return dict(result)


def index_by(lst: List, key: Callable[[Any], Any]) -> Dict[Any, Any]:
    """Создать словарь с ключами по функции"""
    result = {}
    for item in lst:
        result[key(item)] = item
    return result


def nest(lst: List, parent_key: Callable[[Any], Any], child_key: Callable[[Any], Any]) -> Dict:
    """Построить вложенную структуру из плоского списка"""
    result = {}
    children = defaultdict(list)
    
    for item in lst:
        pk = parent_key(item)
        ck = child_key(item)
        if pk is None:
            result[ck] = {'item': item, 'children': []}
        else:
            children[pk].append({'item': item, 'children': []})
    
    # Связываем детей с родителями
    def attach_children(node, key):
        if key in children:
            node['children'] = children[key]
            for child in node['children']:
                attach_children(child, child_key(child['item']))
    
    for key, node in result.items():
        attach_children(node, key)
    
    return result


# === Сортировка ===

def sort_list(lst: List, reverse: bool = False) -> List:
    """Отсортировать список"""
    return sorted(lst, reverse=reverse)


def sort_by(lst: List, key: Callable[[Any], Any], reverse: bool = False) -> List:
    """Отсортировать по ключу"""
    return sorted(lst, key=key, reverse=reverse)


def sort_with(lst: List, comparator: Callable[[Any, Any], int]) -> List:
    """Отсортировать с функцией сравнения"""
    return sorted(lst, key=cmp_to_key(comparator))


def sort_by_key(lst: List, key_name: str, reverse: bool = False) -> List:
    """Отсортировать список словарей по ключу"""
    return sorted(lst, key=lambda x: x.get(key_name), reverse=reverse)


def order_by(lst: List, keys: List[str], orders: List[bool] = None) -> List:
    """Сортировка по нескольким ключам"""
    if orders is None:
        orders = [False] * len(keys)
    
    def multi_key(item):
        result = []
        for key, reverse in zip(keys, orders):
            val = item.get(key)
            if reverse:
                if isinstance(val, (int, float)):
                    val = -val
                elif isinstance(val, str):
                    val = ''.join(chr(255 - ord(c)) for c in val)
            result.append(val)
        return tuple(result)
    
    return sorted(lst, key=multi_key)


def bubble_sort(lst: List) -> List:
    """Сортировка пузырьком"""
    result = lst[:]
    n = len(result)
    for i in range(n):
        for j in range(0, n - i - 1):
            if result[j] > result[j + 1]:
                result[j], result[j + 1] = result[j + 1], result[j]
    return result


def quick_sort(lst: List) -> List:
    """Быстрая сортировка"""
    if len(lst) <= 1:
        return lst
    pivot = lst[len(lst) // 2]
    left = [x for x in lst if x < pivot]
    middle = [x for x in lst if x == pivot]
    right = [x for x in lst if x > pivot]
    return quick_sort(left) + middle + quick_sort(right)


def merge_sort(lst: List) -> List:
    """Сортировка слиянием"""
    if len(lst) <= 1:
        return lst
    
    mid = len(lst) // 2
    left = merge_sort(lst[:mid])
    right = merge_sort(lst[mid:])
    
    return merge(left, right)


def merge(left: List, right: List) -> List:
    """Слияние двух отсортированных списков"""
    result = []
    i = j = 0
    
    while i < len(left) and j < len(right):
        if left[i] <= right[j]:
            result.append(left[i])
            i += 1
        else:
            result.append(right[j])
            j += 1
    
    result.extend(left[i:])
    result.extend(right[j:])
    return result


# === Агрегация ===

def sum_list(lst: List) -> Union[int, float]:
    """Сумма элементов"""
    return sum(lst)


def product(lst: List) -> Union[int, float]:
    """Произведение элементов"""
    result = 1
    for item in lst:
        result *= item
    return result


def min_list(lst: List, default: Any = None) -> Any:
    """Минимальный элемент"""
    return min(lst) if lst else default


def max_list(lst: List, default: Any = None) -> Any:
    """Максимальный элемент"""
    return max(lst) if lst else default


def min_by(lst: List, key: Callable[[Any], Any], default: Any = None) -> Any:
    """Минимальный элемент по ключу"""
    if not lst:
        return default
    return min(lst, key=key)


def max_by(lst: List, key: Callable[[Any], Any], default: Any = None) -> Any:
    """Максимальный элемент по ключу"""
    if not lst:
        return default
    return max(lst, key=key)


def average(lst: List) -> float:
    """Среднее значение"""
    if not lst:
        return 0
    return sum(lst) / len(lst)


def median(lst: List) -> float:
    """Медиана"""
    if not lst:
        return 0
    sorted_lst = sorted(lst)
    n = len(sorted_lst)
    mid = n // 2
    if n % 2 == 0:
        return (sorted_lst[mid - 1] + sorted_lst[mid]) / 2
    return sorted_lst[mid]


def mode(lst: List) -> List[Any]:
    """Мода (наиболее частые элементы)"""
    if not lst:
        return []
    counts = Counter(lst)
    max_count = max(counts.values())
    return [item for item, count in counts.items() if count == max_count]


def variance(lst: List, population: bool = False) -> float:
    """Дисперсия"""
    if not lst:
        return 0
    mean = sum(lst) / len(lst)
    squared_diffs = [(x - mean) ** 2 for x in lst]
    if population:
        return sum(squared_diffs) / len(lst)
    return sum(squared_diffs) / (len(lst) - 1) if len(lst) > 1 else 0


def std_dev(lst: List, population: bool = False) -> float:
    """Стандартное отклонение"""
    import math
    return math.sqrt(variance(lst, population))


def accumulate(lst: List, func: Callable[[Any, Any], Any] = None) -> List:
    """Накопительное применение функции"""
    if func is None:
        func = operator.add
    return list(itertools.accumulate(lst, func))


def reduce_list(lst: List, func: Callable[[Any, Any], Any], initial: Any = None) -> Any:
    """Свернуть список к одному значению"""
    if initial is not None:
        return reduce(func, lst, initial)
    return reduce(func, lst)


def fold_left(lst: List, initial: Any, func: Callable[[Any, Any], Any]) -> Any:
    """Свертка слева"""
    result = initial
    for item in lst:
        result = func(result, item)
    return result


def fold_right(lst: List, initial: Any, func: Callable[[Any, Any], Any]) -> Any:
    """Свертка справа"""
    result = initial
    for item in reversed(lst):
        result = func(item, result)
    return result


# === Комбинации и перестановки ===

def permutations_list(lst: List, r: int = None) -> List[Tuple]:
    """Все перестановки"""
    return list(itertools.permutations(lst, r))


def combinations_list(lst: List, r: int) -> List[Tuple]:
    """Все сочетания"""
    return list(itertools.combinations(lst, r))


def combinations_with_replacement(lst: List, r: int) -> List[Tuple]:
    """Сочетания с повторениями"""
    return list(itertools.combinations_with_replacement(lst, r))


def powerset(lst: List) -> List[Tuple]:
    """Все подмножества (булеан)"""
    s = list(lst)
    return list(t for r in range(len(s) + 1) for t in itertools.combinations(s, r))


def cartesian_product(*lists: List) -> List[Tuple]:
    """Декартово произведение"""
    return list(itertools.product(*lists))


# === Операции с множествами ===

def union(*sets: Set) -> Set:
    """Объединение множеств"""
    if not sets:
        return set()
    return set.union(*sets)


def intersection(*sets: Set) -> Set:
    """Пересечение множеств"""
    if not sets:
        return set()
    return set.intersection(*sets)


def difference(set1: Set, set2: Set) -> Set:
    """Разность множеств"""
    return set1 - set2


def symmetric_difference(set1: Set, set2: Set) -> Set:
    """Симметрическая разность"""
    return set1 ^ set2


def is_subset(set1: Set, set2: Set) -> bool:
    """Является ли set1 подмножеством set2"""
    return set1 <= set2


def is_superset(set1: Set, set2: Set) -> bool:
    """Является ли set1 надмножеством set2"""
    return set1 >= set2


def is_disjoint(set1: Set, set2: Set) -> bool:
    """Не имеют ли множества общих элементов"""
    return set1.isdisjoint(set2)


# === Работа со словарями ===

def dict_get(d: Dict, key: Any, default: Any = None) -> Any:
    """Получить значение по ключу"""
    return d.get(key, default)


def dict_set(d: Dict, key: Any, value: Any) -> Dict:
    """Установить значение по ключу"""
    d[key] = value
    return d


def dict_delete(d: Dict, key: Any) -> Dict:
    """Удалить ключ из словаря"""
    if key in d:
        del d[key]
    return d


def dict_keys(d: Dict) -> List:
    """Получить список ключей"""
    return list(d.keys())


def dict_values(d: Dict) -> List:
    """Получить список значений"""
    return list(d.values())


def dict_items(d: Dict) -> List[Tuple]:
    """Получить список пар (ключ, значение)"""
    return list(d.items())


def dict_merge(*dicts: Dict) -> Dict:
    """Объединить словари"""
    result = {}
    for d in dicts:
        result.update(d)
    return result


def dict_deep_merge(*dicts: Dict) -> Dict:
    """Глубокое объединение словарей"""
    result = {}
    for d in dicts:
        for key, value in d.items():
            if key in result and isinstance(result[key], dict) and isinstance(value, dict):
                result[key] = dict_deep_merge(result[key], value)
            else:
                result[key] = value
    return result


def dict_filter(d: Dict, predicate: Callable[[Any, Any], bool]) -> Dict:
    """Отфильтровать словарь по условию"""
    return {k: v for k, v in d.items() if predicate(k, v)}


def dict_map(d: Dict, func: Callable[[Any, Any], Any]) -> Dict:
    """Преобразовать значения словаря"""
    return {k: func(k, v) for k, v in d.items()}


def dict_map_keys(d: Dict, func: Callable[[Any], Any]) -> Dict:
    """Преобразовать ключи словаря"""
    return {func(k): v for k, v in d.items()}


def dict_map_values(d: Dict, func: Callable[[Any], Any]) -> Dict:
    """Преобразовать значения словаря"""
    return {k: func(v) for k, v in d.items()}


def dict_invert(d: Dict) -> Dict:
    """Инвертировать словарь (ключи <-> значения)"""
    return {v: k for k, v in d.items()}


def dict_group_by(d: Dict, key_func: Callable[[Any, Any], Any]) -> Dict:
    """Сгруппировать элементы словаря"""
    result = defaultdict(dict)
    for k, v in d.items():
        result[key_func(k, v)][k] = v
    return dict(result)


def dict_pick(d: Dict, keys: List) -> Dict:
    """Извлечь только указанные ключи"""
    return {k: d[k] for k in keys if k in d}


def dict_omit(d: Dict, keys: List) -> Dict:
    """Исключить указанные ключи"""
    return {k: v for k, v in d.items() if k not in keys}


def dict_has(d: Dict, key: Any) -> bool:
    """Проверить наличие ключа"""
    return key in d


def dict_size(d: Dict) -> int:
    """Количество элементов в словаре"""
    return len(d)


def dict_empty(d: Dict) -> bool:
    """Проверить пустоту словаря"""
    return len(d) == 0


def dict_default(d: Dict, key: Any, default: Any) -> Any:
    """Получить значение или установить default если ключ отсутствует"""
    if key not in d:
        d[key] = default
    return d[key]


def dict_flatten(d: Dict, parent_key: str = '', sep: str = '.') -> Dict:
    """Сплющить вложенный словарь"""
    items = []
    for k, v in d.items():
        new_key = f"{parent_key}{sep}{k}" if parent_key else k
        if isinstance(v, dict):
            items.extend(dict_flatten(v, new_key, sep).items())
        else:
            items.append((new_key, v))
    return dict(items)


def dict_unflatten(d: Dict, sep: str = '.') -> Dict:
    """Восстановить вложенный словарь из сплющенного"""
    result = {}
    for key, value in d.items():
        parts = key.split(sep)
        current = result
        for part in parts[:-1]:
            if part not in current:
                current[part] = {}
            current = current[part]
        current[parts[-1]] = value
    return result


# === Утилиты ===

def range_list(start: int, stop: int = None, step: int = 1) -> List[int]:
    """Создать список чисел в диапазоне"""
    if stop is None:
        stop = start
        start = 0
    return list(range(start, stop, step))


def linspace(start: float, stop: float, num: int = 50) -> List[float]:
    """Равномерно распределенные числа от start до stop"""
    if num < 2:
        return [stop]
    step = (stop - start) / (num - 1)
    return [start + step * i for i in range(num)]


def logspace(start: float, stop: float, num: int = 50, base: float = 10) -> List[float]:
    """Числа в логарифмической шкале"""
    import math
    return [base ** (start + (stop - start) * i / (num - 1)) for i in range(num)]


def repeat(value: Any, n: int) -> List[Any]:
    """Создать список из n повторений значения"""
    return [value] * n


def replicate(value: Any, n: int) -> List[Any]:
    """То же что и repeat"""
    return repeat(value, n)


def cycle(lst: List, n: int) -> List[Any]:
    """Повторить список n раз"""
    return (lst * n) if n > 0 else []


def interleave(*lists: List) -> List[Any]:
    """Перемежать элементы нескольких списков"""
    result = []
    for items in zip(*lists):
        result.extend(items)
    return result


def interleave_shortest(*lists: List) -> List[Any]:
    """Перемежать до конца кратчайшего списка"""
    result = []
    for items in zip(*lists):
        result.extend(items)
    return result


def intersperse(lst: List, separator: Any) -> List[Any]:
    """Вставить разделитель между элементами"""
    if not lst:
        return []
    result = [lst[0]]
    for item in lst[1:]:
        result.append(separator)
        result.append(item)
    return result


def compact(lst: List) -> List[Any]:
    """Удалить ложные значения"""
    return [item for item in lst if item]


def without(lst: List, *values: Any) -> List[Any]:
    """Удалить указанные значения"""
    return [item for item in lst if item not in values]


def difference_list(lst1: List, lst2: List) -> List[Any]:
    """Разность списков"""
    return [item for item in lst1 if item not in lst2]


def intersection_list(*lists: List) -> List[Any]:
    """Пересечение списков"""
    if not lists:
        return []
    result = lists[0]
    for lst in lists[1:]:
        result = [item for item in result if item in lst]
    return result


def union_list(*lists: List) -> List[Any]:
    """Объединение списков без дубликатов"""
    result = []
    seen = set()
    for lst in lists:
        for item in lst:
            if item not in seen:
                seen.add(item if isinstance(item, (int, float, str, bool)) else id(item))
                result.append(item)
    return result


def sample(lst: List, k: int) -> List[Any]:
    """Случайная выборка k элементов"""
    return random.sample(lst, k)


def choice(lst: List) -> Any:
    """Случайный элемент"""
    return random.choice(lst)


def choices(lst: List, weights: List[float] = None, k: int = 1) -> List[Any]:
    """Случайные элементы с весами"""
    return random.choices(lst, weights=weights, k=k)


def generate(n: int, func: Callable[[int], Any]) -> List[Any]:
    """Сгенерировать список из n элементов функцией"""
    return [func(i) for i in range(n)]


def iterate(func: Callable[[Any], Any], initial: Any, n: int) -> List[Any]:
    """Применить функцию n раз последовательно"""
    result = [initial]
    current = initial
    for _ in range(n):
        current = func(current)
        result.append(current)
    return result


def unfold(func: Callable[[Any], Optional[Tuple[Any, Any]]], initial: Any) -> List[Any]:
    """Развернуть значение в список"""
    result = []
    current = initial
    while True:
        res = func(current)
        if res is None:
            break
        value, next_val = res
        result.append(value)
        current = next_val
    return result


# === Экспорт ===

__all__ = [
    # Создание
    'list_create', 'list_range', 'dict_create', 'set_create', 'tuple_create',
    
    # Базовые операции
    'append', 'prepend', 'insert', 'remove', 'pop', 'clear', 'extend',
    'copy_list', 'reverse_list', 'reversed_copy', 'rotate_left', 'rotate_right',
    'swap', 'shuffle', 'shuffled_copy',
    
    # Доступ
    'first', 'last', 'nth', 'get_slice', 'take', 'take_last', 'drop', 'drop_last',
    'head', 'tail', 'init',
    
    # Поиск
    'find', 'find_index', 'find_all', 'find_indices', 'contains', 'contains_any',
    'contains_all', 'index_of', 'rindex_of', 'count', 'count_if',
    
    # Фильтрация
    'filter_list', 'reject', 'filter_none', 'filter_false', 'unique', 'unique_by',
    'distinct',
    
    # Преобразование
    'map_list', 'map_with_index', 'flat_map', 'flatten', 'flatten_deep',
    'zip_lists', 'unzip', 'chunk', 'partition', 'group_by', 'index_by', 'nest',
    
    # Сортировка
    'sort_list', 'sort_by', 'sort_with', 'sort_by_key', 'order_by',
    'bubble_sort', 'quick_sort', 'merge_sort', 'merge',
    
    # Агрегация
    'sum_list', 'product', 'min_list', 'max_list', 'min_by', 'max_by',
    'average', 'median', 'mode', 'variance', 'std_dev', 'accumulate',
    'reduce_list', 'fold_left', 'fold_right',
    
    # Комбинаторика
    'permutations_list', 'combinations_list', 'combinations_with_replacement',
    'powerset', 'cartesian_product',
    
    # Множества
    'union', 'intersection', 'difference', 'symmetric_difference',
    'is_subset', 'is_superset', 'is_disjoint',
    
    # Словари
    'dict_get', 'dict_set', 'dict_delete', 'dict_keys', 'dict_values',
    'dict_items', 'dict_merge', 'dict_deep_merge', 'dict_filter', 'dict_map',
    'dict_map_keys', 'dict_map_values', 'dict_invert', 'dict_group_by',
    'dict_pick', 'dict_omit', 'dict_has', 'dict_size', 'dict_empty',
    'dict_default', 'dict_flatten', 'dict_unflatten',
    
    # Утилиты
    'range_list', 'linspace', 'logspace', 'repeat', 'replicate', 'cycle',
    'interleave', 'interleave_shortest', 'intersperse', 'compact', 'without',
    'difference_list', 'intersection_list', 'union_list', 'sample', 'choice',
    'choices', 'generate', 'iterate', 'unfold',
]
