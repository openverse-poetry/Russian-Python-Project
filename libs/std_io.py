"""
Библиотека стандартного ввода-вывода и работы с файлами
Предоставляет расширенные возможности для работы с консолью, файлами, буфером обмена и потоками.
"""

import sys
import os
import shutil
import tempfile
import mmap
import hashlib
import base64
import gzip
import bz2
import lzma
import io
import contextlib
from pathlib import Path
from typing import Any, List, Dict, Optional, Union, Callable, Iterator, Tuple

# Константы цветов для терминала (расширенные)
COLORS = {
    'reset': '\033[0m',
    'bold': '\033[1m',
    'dim': '\033[2m',
    'italic': '\033[3m',
    'underline': '\033[4m',
    'blink': '\033[5m',
    'reverse': '\033[7m',
    'hidden': '\033[8m',
    'black': '\033[30m',
    'red': '\033[31m',
    'green': '\033[32m',
    'yellow': '\033[33m',
    'blue': '\033[34m',
    'magenta': '\033[35m',
    'cyan': '\033[36m',
    'white': '\033[37m',
    'bg_black': '\033[40m',
    'bg_red': '\033[41m',
    'bg_green': '\033[42m',
    'bg_yellow': '\033[43m',
    'bg_blue': '\033[44m',
    'bg_magenta': '\033[45m',
    'bg_cyan': '\033[46m',
    'bg_white': '\033[47m',
    'bright_black': '\033[90m',
    'bright_red': '\033[91m',
    'bright_green': '\033[92m',
    'bright_yellow': '\033[93m',
    'bright_blue': '\033[94m',
    'bright_magenta': '\033[95m',
    'bright_cyan': '\033[96m',
    'bright_white': '\033[97m',
}

# Уровни логирования
LOG_LEVELS = {
    'DEBUG': 0,
    'INFO': 1,
    'WARNING': 2,
    'ERROR': 3,
    'CRITICAL': 4,
}

class IOBuffer:
    """Буфер для эффективной работы с вводом-выводом"""
    def __init__(self, initial_size: int = 4096):
        self.buffer = bytearray(initial_size)
        self.position = 0
        self.size = 0
    
    def write(self, data: bytes) -> int:
        """Записать данные в буфер"""
        if len(data) > len(self.buffer) - self.position:
            new_size = max(len(self.buffer) * 2, self.position + len(data))
            self.buffer.extend(b'\x00' * (new_size - len(self.buffer)))
        self.buffer[self.position:self.position + len(data)] = data
        self.position += len(data)
        self.size = max(self.size, self.position)
        return len(data)
    
    def read(self, size: int = -1) -> bytes:
        """Прочитать данные из буфера"""
        if size == -1:
            size = self.size - self.position
        result = bytes(self.buffer[self.position:self.position + size])
        self.position += min(size, self.size - self.position)
        return result
    
    def seek(self, pos: int, whence: int = 0) -> int:
        """Изменить позицию в буфере"""
        if whence == 0:
            self.position = pos
        elif whence == 1:
            self.position += pos
        elif whence == 2:
            self.position = self.size + pos
        self.position = max(0, min(self.position, self.size))
        return self.position
    
    def tell(self) -> int:
        """Вернуть текущую позицию"""
        return self.position
    
    def clear(self):
        """Очистить буфер"""
        self.position = 0
        self.size = 0
    
    def getvalue(self) -> bytes:
        """Получить содержимое буфера"""
        return bytes(self.buffer[:self.size])


class FileStream:
    """Потоковый интерфейс для работы с файлами"""
    def __init__(self, path: str, mode: str = 'r', buffering: int = -1, encoding: str = None):
        self.path = Path(path)
        self.mode = mode
        self.encoding = encoding or 'utf-8'
        self.buffering = buffering
        self.file = None
        self.is_open = False
    
    def open(self) -> 'FileStream':
        """Открыть файл"""
        if self.mode in ['r', 'rb']:
            if not self.path.exists():
                raise FileNotFoundError(f"Файл не найден: {self.path}")
        self.file = open(self.path, self.mode, buffering=self.buffering, encoding=self.encoding if 'b' not in self.mode else None)
        self.is_open = True
        return self
    
    def close(self):
        """Закрыть файл"""
        if self.file and self.is_open:
            self.file.close()
            self.is_open = False
    
    def __enter__(self):
        return self.open()
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        self.close()
        return False
    
    def read(self, size: int = -1) -> Union[str, bytes]:
        """Прочитать данные из файла"""
        if not self.is_open:
            raise IOError("Файл не открыт")
        return self.file.read(size)
    
    def readline(self, size: int = -1) -> Union[str, bytes]:
        """Прочитать строку из файла"""
        if not self.is_open:
            raise IOError("Файл не открыт")
        return self.file.readline(size)
    
    def readlines(self, hint: int = -1) -> List[Union[str, bytes]]:
        """Прочитать все строки из файла"""
        if not self.is_open:
            raise IOError("Файл не открыт")
        return self.file.readlines(hint)
    
    def write(self, data: Union[str, bytes]) -> int:
        """Записать данные в файл"""
        if not self.is_open:
            raise IOError("Файл не открыт")
        return self.file.write(data)
    
    def writelines(self, lines: List[Union[str, bytes]]) -> None:
        """Записать список строк в файл"""
        if not self.is_open:
            raise IOError("Файл не открыт")
        self.file.writelines(lines)
    
    def seek(self, pos: int, whence: int = 0) -> int:
        """Изменить позицию в файле"""
        if not self.is_open:
            raise IOError("Файл не открыт")
        return self.file.seek(pos, whence)
    
    def tell(self) -> int:
        """Вернуть текущую позицию в файле"""
        if not self.is_open:
            raise IOError("Файл не открыт")
        return self.file.tell()
    
    def flush(self) -> None:
        """Сбросить буфер файла"""
        if not self.is_open:
            raise IOError("Файл не открыт")
        self.file.flush()
    
    def truncate(self, size: int = None) -> int:
        """Обрезать файл до указанного размера"""
        if not self.is_open:
            raise IOError("Файл не открыт")
        return self.file.truncate(size)
    
    def is_eof(self) -> bool:
        """Проверить конец файла"""
        if not self.is_open:
            raise IOError("Файл не открыт")
        pos = self.file.tell()
        self.file.seek(0, 2)
        eof = pos == self.file.tell()
        self.file.seek(pos)
        return eof


class DirectoryWatcher:
    """Наблюдатель за изменениями в директории"""
    def __init__(self, path: str, recursive: bool = False):
        self.path = Path(path)
        self.recursive = recursive
        self.snapshot = {}
    
    def take_snapshot(self) -> Dict[str, float]:
        """Сделать снимок состояния директории"""
        snapshot = {}
        if not self.path.exists():
            return snapshot
        
        pattern = '**/*' if self.recursive else '*'
        for item in self.path.glob(pattern):
            if item.is_file():
                snapshot[str(item)] = item.stat().st_mtime
        self.snapshot = snapshot
        return snapshot
    
    def get_changes(self) -> Dict[str, List[str]]:
        """Получить изменения с момента последнего снимка"""
        current = {}
        pattern = '**/*' if self.recursive else '*'
        for item in self.path.glob(pattern):
            if item.is_file():
                current[str(item)] = item.stat().st_mtime
        
        changes = {'created': [], 'modified': [], 'deleted': []}
        
        for path, mtime in current.items():
            if path not in self.snapshot:
                changes['created'].append(path)
            elif self.snapshot[path] != mtime:
                changes['modified'].append(path)
        
        for path in self.snapshot:
            if path not in current:
                changes['deleted'].append(path)
        
        self.snapshot = current
        return changes


def print(*args, sep: str = ' ', end: str = '\n', file=None, flush: bool = False, 
          color: str = None, bg_color: str = None, style: str = None) -> None:
    """
    Расширенная функция печати с поддержкой цветов и стилей
    
    Аргументы:
        *args: Объекты для печати
        sep: Разделитель между объектами
        end: Строка в конце вывода
        file: Файловый объект для вывода
        flush: Сбросить буфер после печати
        color: Цвет текста (название или код)
        bg_color: Цвет фона
        style: Стиль текста (bold, italic, underline и т.д.)
    """
    output = sep.join(str(arg) for arg in args)
    
    if color or bg_color or style:
        codes = []
        if style and style in COLORS:
            codes.append(COLORS[style])
        if color and color in COLORS:
            codes.append(COLORS[color])
        if bg_color and bg_color in COLORS:
            codes.append(COLORS[bg_color])
        
        output = ''.join(codes) + output + COLORS['reset']
    
    target_file = file if file else sys.stdout
    target_file.write(output + end)
    
    if flush:
        target_file.flush()


def input(prompt: str = '', default: str = None, mask: bool = False, 
          timeout: float = None, validator: Callable[[str], bool] = None) -> str:
    """
    Расширенный ввод с поддержкой маскирования, таймаута и валидации
    
    Аргументы:
        prompt: Приглашение к вводу
        default: Значение по умолчанию
        mask: Маскировать ввод (для паролей)
        timeout: Таймаут ввода в секундах
        validator: Функция валидации ввода
    
    Возвращает:
        Введенную строку или значение по умолчанию
    """
    if prompt:
        print(prompt, end='', flush=True)
    
    if mask:
        import getpass
        value = getpass.getpass('')
    else:
        value = sys.stdin.readline().rstrip('\n')
    
    if not value and default is not None:
        value = default
    
    if validator and not validator(value):
        raise ValueError("Ввод не прошел валидацию")
    
    return value


def read_file(path: str, encoding: str = 'utf-8', binary: bool = False, 
              chunk_size: int = 0) -> Union[str, bytes, Iterator[Union[str, bytes]]]:
    """
    Читать файл целиком, по частям или как байты
    
    Аргументы:
        path: Путь к файлу
        encoding: Кодировка (если не бинарный режим)
        binary: Читать как байты
        chunk_size: Размер чанка (0 - читать весь файл)
    
    Возвращает:
        Содержимое файла или итератор чанков
    """
    path = Path(path)
    if not path.exists():
        raise FileNotFoundError(f"Файл не найден: {path}")
    
    mode = 'rb' if binary else 'r'
    
    if chunk_size > 0:
        def generator():
            with open(path, mode, encoding=None if binary else encoding) as f:
                while True:
                    chunk = f.read(chunk_size)
                    if not chunk:
                        break
                    yield chunk
        return generator()
    else:
        with open(path, mode, encoding=None if binary else encoding) as f:
            return f.read()


def write_file(path: str, data: Union[str, bytes], encoding: str = 'utf-8', 
               append: bool = False, mkdir: bool = False) -> int:
    """
    Записать данные в файл
    
    Аргументы:
        path: Путь к файлу
        data: Данные для записи
        encoding: Кодировка (если строка)
        append: Добавлять в конец файла
        mkdir: Создать родительские директории
    
    Возвращает:
        Количество записанных байт
    """
    path = Path(path)
    
    if mkdir and not path.parent.exists():
        path.parent.mkdir(parents=True, exist_ok=True)
    
    mode = 'ab' if append else 'wb' if isinstance(data, bytes) else ('a' if append else 'w')
    encoding_param = None if isinstance(data, bytes) or 'b' in mode else encoding
    
    with open(path, mode, encoding=encoding_param) as f:
        return f.write(data)


def copy_file(src: str, dst: str, overwrite: bool = True, preserve_metadata: bool = True) -> bool:
    """
    Копировать файл
    
    Аргументы:
        src: Исходный путь
        dst: Целевой путь
        overwrite: Перезаписать если существует
        preserve_metadata: Сохранить метаданные
    
    Возвращает:
        Успешность операции
    """
    src = Path(src)
    dst = Path(dst)
    
    if not src.exists():
        raise FileNotFoundError(f"Исходный файл не найден: {src}")
    
    if dst.exists() and not overwrite:
        raise FileExistsError(f"Целевой файл уже существует: {dst}")
    
    if preserve_metadata:
        shutil.copy2(src, dst)
    else:
        shutil.copy(src, dst)
    
    return True


def move_file(src: str, dst: str, overwrite: bool = True) -> bool:
    """
    Переместить файл
    
    Аргументы:
        src: Исходный путь
        dst: Целевой путь
        overwrite: Перезаписать если существует
    
    Возвращает:
        Успешность операции
    """
    src = Path(src)
    dst = Path(dst)
    
    if not src.exists():
        raise FileNotFoundError(f"Исходный файл не найден: {src}")
    
    if dst.exists() and not overwrite:
        raise FileExistsError(f"Целевой файл уже существует: {dst}")
    
    shutil.move(src, dst)
    return True


def delete_file(path: str, force: bool = False) -> bool:
    """
    Удалить файл
    
    Аргументы:
        path: Путь к файлу
        force: Не вызывать ошибку если файл не существует
    
    Возвращает:
        Успешность операции
    """
    path = Path(path)
    
    if not path.exists():
        if force:
            return False
        raise FileNotFoundError(f"Файл не найден: {path}")
    
    path.unlink()
    return True


def delete_directory(path: str, recursive: bool = True, force: bool = False) -> bool:
    """
    Удалить директорию
    
    Аргументы:
        path: Путь к директории
        recursive: Удалять рекурсивно
        force: Не вызывать ошибку если директория не существует
    
    Возвращает:
        Успешность операции
    """
    path = Path(path)
    
    if not path.exists():
        if force:
            return False
        raise FileNotFoundError(f"Директория не найдена: {path}")
    
    if not path.is_dir():
        raise NotADirectoryError(f"Не является директорией: {path}")
    
    if recursive:
        shutil.rmtree(path)
    else:
        path.rmdir()
    
    return True


def list_directory(path: str, pattern: str = '*', recursive: bool = False, 
                   include_dirs: bool = True, include_files: bool = True) -> List[str]:
    """
    Список файлов и директорий
    
    Аргументы:
        path: Путь к директории
        pattern: Шаблон для фильтрации
        recursive: Рекурсивный обход
        include_dirs: Включать директории
        include_files: Включать файлы
    
    Возвращает:
        Список путей
    """
    path = Path(path)
    
    if not path.exists():
        raise FileNotFoundError(f"Директория не найдена: {path}")
    
    if not path.is_dir():
        raise NotADirectoryError(f"Не является директорией: {path}")
    
    result = []
    glob_pattern = '**/' + pattern if recursive else pattern
    
    for item in path.glob(glob_pattern):
        if item.is_dir() and include_dirs:
            result.append(str(item))
        elif item.is_file() and include_files:
            result.append(str(item))
    
    return result


def create_directory(path: str, parents: bool = True, exist_ok: bool = True) -> bool:
    """
    Создать директорию
    
    Аргументы:
        path: Путь к директории
        parents: Создать родительские директории
        exist_ok: Не вызывать ошибку если директория существует
    
    Возвращает:
        Успешность операции
    """
    path = Path(path)
    path.mkdir(parents=parents, exist_ok=exist_ok)
    return True


def get_file_info(path: str) -> Dict[str, Any]:
    """
    Получить информацию о файле
    
    Аргументы:
        path: Путь к файлу
    
    Возвращает:
        Словарь с информацией о файле
    """
    path = Path(path)
    
    if not path.exists():
        raise FileNotFoundError(f"Файл не найден: {path}")
    
    stat = path.stat()
    
    return {
        'name': path.name,
        'path': str(path.absolute()),
        'size': stat.st_size,
        'created': stat.st_ctime,
        'modified': stat.st_mtime,
        'accessed': stat.st_atime,
        'is_file': path.is_file(),
        'is_dir': path.is_dir(),
        'is_symlink': path.is_symlink(),
        'extension': path.suffix,
        'stem': path.stem,
        'parent': str(path.parent),
    }


def get_file_hash(path: str, algorithm: str = 'sha256', chunk_size: int = 8192) -> str:
    """
    Вычислить хэш файла
    
    Аргументы:
        path: Путь к файлу
        algorithm: Алгоритм хеширования (md5, sha1, sha256, sha512)
        chunk_size: Размер чанка для чтения
    
    Возвращает:
        Хэш в шестнадцатеричном формате
    """
    path = Path(path)
    
    if not path.exists():
        raise FileNotFoundError(f"Файл не найден: {path}")
    
    if algorithm == 'md5':
        hasher = hashlib.md5()
    elif algorithm == 'sha1':
        hasher = hashlib.sha1()
    elif algorithm == 'sha256':
        hasher = hashlib.sha256()
    elif algorithm == 'sha512':
        hasher = hashlib.sha512()
    else:
        raise ValueError(f"Неизвестный алгоритм: {algorithm}")
    
    with open(path, 'rb') as f:
        while True:
            chunk = f.read(chunk_size)
            if not chunk:
                break
            hasher.update(chunk)
    
    return hasher.hexdigest()


def compress_file(path: str, output: str = None, format: str = 'gzip', level: int = 6) -> str:
    """
    Сжать файл
    
    Аргументы:
        path: Путь к файлу
        output: Путь к выходному файлу
        format: Формат сжатия (gzip, bz2, xz)
        level: Уровень сжатия
    
    Возвращает:
        Путь к сжатому файлу
    """
    path = Path(path)
    
    if not path.exists():
        raise FileNotFoundError(f"Файл не найден: {path}")
    
    if output is None:
        if format == 'gzip':
            output = str(path) + '.gz'
        elif format == 'bz2':
            output = str(path) + '.bz2'
        elif format == 'xz':
            output = str(path) + '.xz'
    
    if format == 'gzip':
        with open(path, 'rb') as f_in:
            with gzip.open(output, 'wb', compresslevel=level) as f_out:
                shutil.copyfileobj(f_in, f_out)
    elif format == 'bz2':
        with open(path, 'rb') as f_in:
            with bz2.open(output, 'wb', compresslevel=level) as f_out:
                shutil.copyfileobj(f_in, f_out)
    elif format == 'xz':
        with open(path, 'rb') as f_in:
            with lzma.open(output, 'wb', preset=level) as f_out:
                shutil.copyfileobj(f_in, f_out)
    else:
        raise ValueError(f"Неизвестный формат сжатия: {format}")
    
    return output


def decompress_file(path: str, output: str = None) -> str:
    """
    Распаковать файл
    
    Аргументы:
        path: Путь к файлу
        output: Путь к выходному файлу
    
    Возвращает:
        Путь к распакованному файлу
    """
    path = Path(path)
    
    if not path.exists():
        raise FileNotFoundError(f"Файл не найден: {path}")
    
    if output is None:
        if path.suffix == '.gz':
            output = str(path)[:-3]
        elif path.suffix == '.bz2':
            output = str(path)[:-4]
        elif path.suffix == '.xz':
            output = str(path)[:-3]
        else:
            raise ValueError(f"Неизвестный формат сжатия: {path.suffix}")
    
    if path.suffix == '.gz':
        with gzip.open(path, 'rb') as f_in:
            with open(output, 'wb') as f_out:
                shutil.copyfileobj(f_in, f_out)
    elif path.suffix == '.bz2':
        with bz2.open(path, 'rb') as f_in:
            with open(output, 'wb') as f_out:
                shutil.copyfileobj(f_in, f_out)
    elif path.suffix == '.xz':
        with lzma.open(path, 'rb') as f_in:
            with open(output, 'wb') as f_out:
                shutil.copyfileobj(f_in, f_out)
    else:
        raise ValueError(f"Неизвестный формат сжатия: {path.suffix}")
    
    return output


def encode_base64(data: Union[str, bytes], url_safe: bool = False) -> str:
    """
    Кодировать в Base64
    
    Аргументы:
        data: Данные для кодирования
        url_safe: Использовать URL-safe алфавит
    
    Возвращает:
        Строка Base64
    """
    if isinstance(data, str):
        data = data.encode('utf-8')
    
    if url_safe:
        return base64.urlsafe_b64encode(data).decode('ascii')
    else:
        return base64.b64encode(data).decode('ascii')


def decode_base64(data: str, url_safe: bool = False) -> bytes:
    """
    Декодировать Base64
    
    Аргументы:
        data: Строка Base64
        url_safe: Использовать URL-safe алфавит
    
    Возвращает:
        Декодированные байты
    """
    if url_safe:
        return base64.urlsafe_b64decode(data)
    else:
        return base64.b64decode(data)


def tail_file(path: str, lines: int = 10, encoding: str = 'utf-8') -> List[str]:
    """
    Прочитать последние строки файла (аналог команды tail)
    
    Аргументы:
        path: Путь к файлу
        lines: Количество строк
        encoding: Кодировка
    
    Возвращает:
        Список последних строк
    """
    path = Path(path)
    
    if not path.exists():
        raise FileNotFoundError(f"Файл не найден: {path}")
    
    with open(path, 'rb') as f:
        # Используем mmap для эффективного чтения с конца
        try:
            mm = mmap.mmap(f.fileno(), 0, access=mmap.ACCESS_READ)
        except ValueError:
            # Пустой файл
            return []
        
        try:
            # Ищем позиции переводов строк с конца
            positions = []
            pos = mm.size() - 1
            while pos >= 0 and len(positions) < lines:
                if mm[pos] == ord('\n'):
                    positions.append(pos)
                pos -= 1
            
            # Читаем строки
            result = []
            if positions:
                start = positions[-1] + 1 if positions else 0
                result.append(mm[start:].decode(encoding).rstrip())
                
                for i in range(len(positions) - 1, 0, -1):
                    start = positions[i] + 1
                    end = positions[i - 1]
                    result.insert(0, mm[start:end].decode(encoding).rstrip())
            else:
                # Файл без переводов строк
                result = [mm[:].decode(encoding).rstrip()]
            
            return result[-lines:]
        finally:
            mm.close()


def head_file(path: str, lines: int = 10, encoding: str = 'utf-8') -> List[str]:
    """
    Прочитать первые строки файла (аналог команды head)
    
    Аргументы:
        path: Путь к файлу
        lines: Количество строк
        encoding: Кодировка
    
    Возвращает:
        Список первых строк
    """
    path = Path(path)
    
    if not path.exists():
        raise FileNotFoundError(f"Файл не найден: {path}")
    
    result = []
    with open(path, 'r', encoding=encoding) as f:
        for i, line in enumerate(f):
            if i >= lines:
                break
            result.append(line.rstrip('\n'))
    
    return result


def watch_file(path: str, callback: Callable[[str], None], 
               ignore_patterns: List[str] = None) -> None:
    """
    Наблюдать за изменениями в файле
    
    Аргументы:
        path: Путь к файлу
        callback: Функция обратного вызова при изменении
        ignore_patterns: Шаблоны игнорируемых изменений
    """
    import time
    
    path = Path(path)
    
    if not path.exists():
        raise FileNotFoundError(f"Файл не найден: {path}")
    
    last_modified = path.stat().st_mtime
    last_size = path.stat().st_size
    
    while True:
        try:
            current_modified = path.stat().st_mtime
            current_size = path.stat().st_size
            
            if current_modified != last_modified or current_size != last_size:
                if ignore_patterns:
                    # Проверка паттернов (упрощенная)
                    should_ignore = False
                    for pattern in ignore_patterns:
                        if pattern in str(path):
                            should_ignore = True
                            break
                    if not should_ignore:
                        callback(str(path))
                else:
                    callback(str(path))
                
                last_modified = current_modified
                last_size = current_size
            
            time.sleep(0.1)
        except KeyboardInterrupt:
            break
        except FileNotFoundError:
            break


def split_file(path: str, chunk_size: int = 1024 * 1024, output_prefix: str = None) -> List[str]:
    """
    Разделить файл на части
    
    Аргументы:
        path: Путь к файлу
        chunk_size: Размер каждой части в байтах
        output_prefix: Префикс для имен выходных файлов
    
    Возвращает:
        Список путей к созданным файлам
    """
    path = Path(path)
    
    if not path.exists():
        raise FileNotFoundError(f"Файл не найден: {path}")
    
    if output_prefix is None:
        output_prefix = str(path) + '.part'
    
    result = []
    chunk_index = 0
    
    with open(path, 'rb') as f:
        while True:
            chunk = f.read(chunk_size)
            if not chunk:
                break
            
            output_path = f"{output_prefix}_{chunk_index:04d}"
            with open(output_path, 'wb') as out:
                out.write(chunk)
            
            result.append(output_path)
            chunk_index += 1
    
    return result


def merge_files(paths: List[str], output: str) -> str:
    """
    Объединить несколько файлов в один
    
    Аргументы:
        paths: Список путей к файлам
        output: Путь к выходному файлу
    
    Возвращает:
        Путь к объединенному файлу
    """
    with open(output, 'wb') as out:
        for path in paths:
            path = Path(path)
            if not path.exists():
                raise FileNotFoundError(f"Файл не найден: {path}")
            
            with open(path, 'rb') as f:
                shutil.copyfileobj(f, out)
    
    return output


def create_temp_file(suffix: str = '', prefix: str = 'tmp', 
                     dir: str = None, delete: bool = False) -> str:
    """
    Создать временный файл
    
    Аргументы:
        suffix: Суффикс имени файла
        prefix: Префикс имени файла
        dir: Директория для создания
        delete: Удалить файл после использования (возвращает путь к несуществующему файлу)
    
    Возвращает:
        Путь к временному файлу
    """
    fd, path = tempfile.mkstemp(suffix=suffix, prefix=prefix, dir=dir)
    os.close(fd)
    
    if delete:
        os.unlink(path)
    
    return path


def create_temp_dir(suffix: str = '', prefix: str = 'tmp', dir: str = None) -> str:
    """
    Создать временную директорию
    
    Аргументы:
        suffix: Суффикс имени директории
        prefix: Префикс имени директории
        dir: Родительская директория
    
    Возвращает:
        Путь к временной директории
    """
    return tempfile.mkdtemp(suffix=suffix, prefix=prefix, dir=dir)


def get_disk_usage(path: str = '/') -> Dict[str, int]:
    """
    Получить информацию о использовании диска
    
    Аргументы:
        path: Путь для проверки
    
    Возвращает:
        Словарь с информацией о диске
    """
    usage = shutil.disk_usage(path)
    return {
        'total': usage.total,
        'used': usage.used,
        'free': usage.free,
        'percent_used': (usage.used / usage.total) * 100,
    }


def get_terminal_size() -> Tuple[int, int]:
    """
    Получить размер терминала
    
    Возвращает:
        Кортеж (колонки, строки)
    """
    size = shutil.get_terminal_size()
    return (size.columns, size.lines)


def clear_screen() -> None:
    """Очистить экран терминала"""
    os.system('cls' if os.name == 'nt' else 'clear')


def beep(frequency: int = 1000, duration: int = 100) -> None:
    """
    Издать звуковой сигнал
    
    Аргументы:
        frequency: Частота в Гц
        duration: Длительность в миллисекундах
    """
    if os.name == 'nt':
        import winsound
        winsound.Beep(frequency, duration)
    else:
        # Для Unix-систем просто выводим символ звонка
        sys.stdout.write('\a')
        sys.stdout.flush()


def progress_bar(current: int, total: int, width: int = 40, 
                 prefix: str = '', suffix: str = '') -> str:
    """
    Создать строку прогресс-бара
    
    Аргументы:
        current: Текущее значение
        total: Общее значение
        width: Ширина бара в символах
        prefix: Префикс строки
        suffix: Суффикс строки
    
    Возвращает:
        Строка прогресс-бара
    """
    if total == 0:
        percent = 0
    else:
        percent = current / total
    
    filled_length = int(width * percent)
    bar = '█' * filled_length + '-' * (width - filled_length)
    
    return f'{prefix}[{bar}] {percent * 100:.1f}%{suffix}'


def log_message(message: str, level: str = 'INFO', 
                filename: str = None, console: bool = True) -> None:
    """
    Записать сообщение в лог
    
    Аргументы:
        message: Сообщение
        level: Уровень логирования
        filename: Путь к файлу лога
        console: Выводить в консоль
    """
    from datetime import datetime
    
    timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    formatted_message = f"[{timestamp}] [{level}] {message}"
    
    if console:
        color = None
        if level == 'ERROR' or level == 'CRITICAL':
            color = 'red'
        elif level == 'WARNING':
            color = 'yellow'
        elif level == 'DEBUG':
            color = 'dim'
        
        print(formatted_message, color=color)
    
    if filename:
        with open(filename, 'a', encoding='utf-8') as f:
            f.write(formatted_message + '\n')


class Logger:
    """Класс для логирования с поддержкой уровней и файлов"""
    
    def __init__(self, name: str = 'app', filename: str = None, 
                 level: str = 'INFO', format_string: str = None):
        self.name = name
        self.filename = filename
        self.level = LOG_LEVELS.get(level, 1)
        self.format_string = format_string or '[{timestamp}] [{level}] [{name}] {message}'
    
    def _format(self, message: str, level: str) -> str:
        from datetime import datetime
        return self.format_string.format(
            timestamp=datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
            level=level,
            name=self.name,
            message=message
        )
    
    def _write(self, message: str, level: str) -> None:
        if LOG_LEVELS.get(level, 1) >= self.level:
            formatted = self._format(message, level)
            
            # Консольный вывод
            color = None
            if level in ['ERROR', 'CRITICAL']:
                color = 'red'
            elif level == 'WARNING':
                color = 'yellow'
            elif level == 'DEBUG':
                color = 'dim'
            
            print(formatted, color=color)
            
            # Запись в файл
            if self.filename:
                with open(self.filename, 'a', encoding='utf-8') as f:
                    f.write(formatted + '\n')
    
    def debug(self, message: str) -> None:
        self._write(message, 'DEBUG')
    
    def info(self, message: str) -> None:
        self._write(message, 'INFO')
    
    def warning(self, message: str) -> None:
        self._write(message, 'WARNING')
    
    def error(self, message: str) -> None:
        self._write(message, 'ERROR')
    
    def critical(self, message: str) -> None:
        self._write(message, 'CRITICAL')


# Экспорт всех функций и классов
__all__ = [
    'COLORS',
    'LOG_LEVELS',
    'IOBuffer',
    'FileStream',
    'DirectoryWatcher',
    'print',
    'input',
    'read_file',
    'write_file',
    'copy_file',
    'move_file',
    'delete_file',
    'delete_directory',
    'list_directory',
    'create_directory',
    'get_file_info',
    'get_file_hash',
    'compress_file',
    'decompress_file',
    'encode_base64',
    'decode_base64',
    'tail_file',
    'head_file',
    'watch_file',
    'split_file',
    'merge_files',
    'create_temp_file',
    'create_temp_dir',
    'get_disk_usage',
    'get_terminal_size',
    'clear_screen',
    'beep',
    'progress_bar',
    'log_message',
    'Logger',
]
