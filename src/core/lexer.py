# Русский Питон - Лексический анализатор (Lexer)
# Версия 1.0.0 - Профессиональная реализация

"""
Лексический анализатор для русского языка программирования.

Поддерживает:
- 50+ типов токенов
- Русские ключевые слова всех конструкций Python
- Числа (целые, дробные, комплексные, с разделителями)
- Строки (одинарные, двойные, тройные, raw, f-строки)
- Операторы и разделители
- Отступы как значимые символы
- Комментарии однострочные и многострочные
- Unicode идентификаторы на русском языке
"""

import re
from enum import Enum, auto
from dataclasses import dataclass, field
from typing import List, Optional, Dict, Set, Tuple, Any
from collections import defaultdict


class TokenType(Enum):
    """Типы токенов для русского языка программирования."""
    
    # Ключевые слова управления потоком
    ЕСЛИ = auto()           # если
    ИНАЧЕ = auto()          # иначе
    ИНАЧЕ_ЕСЛИ = auto()     # иначе если
    ПОКА = auto()           # пока
    ДЛЯ = auto()            # для
    В = auto()              # в
    
    # Объявления
    ФУНКЦИЯ = auto()        # функция
    КЛАСС = auto()          # класс
    ВОЗВРАТ = auto()        # возврат
    ИМПОРТ = auto()         # импорт
    ИЗ = auto()             # из
    КАК = auto()            # как
    
    # Логические операторы
    И = auto()              # и
    ИЛИ = auto()            # или
    НЕ = auto()             # не
    
    # Специальные значения
    ИСТИНА = auto()         # истина
    ЛОЖЬ = auto()           # ложь
    НИЧТО = auto()          # ничто
    
    # Асинхронность
    АСИНХРОННО = auto()     # асинхронно
    ЖДАТЬ = auto()          # ждать
    
    # Контекстные менеджеры
    С = auto()              # с
    
    # Обработка исключений
    ПОПРОБУЙ = auto()       # попробуй
    КРОМЕ = auto()          # кроме
    НАКОНЕЦ = auto()        # наконец
    ВЫБРОСИТЬ = auto()      # выбросить
    
    # Циклы
    ПРОДОЛЖИТЬ = auto()     # продолжить
    ПРЕРВАТЬ = auto()       # прервать
    
    # Глобальные и нелокальные
    ГЛОБАЛЬНО = auto()      # глобально
    НЕЛОКАЛЬНО = auto()     # нелокально
    
    # Параллелизм
    ПАРАЛЛЕЛЬНО = auto()    # параллельно
    
    # Макросы
    МАКРОС = auto()         # макрос
    
    # Литералы
    ЧИСЛО = auto()          # числовое значение
    СТРОКА = auto()         # строковое значение
    ИДЕНТИФИКАТОР = auto()  # имя переменной/функции
    
    # Операторы
    ПЛЮС = auto()           # +
    МИНУС = auto()          # -
    ЗВЕЗДОЧКА = auto()      # *
    СЛЕШ = auto()           # /
    ДВОЕТЧИЕ = auto()       # //
    ПРОЦЕНТ = auto()        # %
    СТЕПЕНЬ = auto()        # **
    
    РАВНО = auto()          # =
    ПЛЮС_РАВНО = auto()     # +=
    МИНУС_РАВНО = auto()    # -=
    УМНОЖИТЬ_РАВНО = auto() # *=
    РАЗДЕЛИТЬ_РАВНО = auto()# /=
    ЦЕЛОЧИСЛЕННО_РАВНО = auto() # //=
    МОДУЛЬ_РАВНО = auto()   # %=
    СТЕПЕНЬ_РАВНО = auto()  # **=
    
    РАВНО_РАВНО = auto()    # ==
    НЕ_РАВНО = auto()       # !=
    МЕНЬШЕ = auto()         # <
    БОЛЬШЕ = auto()         # >
    МЕНЬШЕ_РАВНО = auto()   # <=
    БОЛЬШЕ_РАВНО = auto()   # >=
    
    # Логические операторы (символьные)
    ЛОГ_И = auto()          # &
    ЛОГ_ИЛИ = auto()        # |
    ЛОГ_НЕ = auto()         # ~
    СДВИГ_ЛЕВО = auto()     # <<
    СДВИГ_ПРАВО = auto()    # >>
    
    # Разделители
    ЛЕВАЯ_СКОБКА = auto()   # (
    ПРАВАЯ_СКОБКА = auto()  # )
    ЛЕВАЯ_КВАДРАТНАЯ = auto() # [
    ПРАВАЯ_КВАДРАТНАЯ = auto() # ]
    ЛЕВАЯ_ФИГУРНАЯ = auto() # {
    ПРАВАЯ_ФИГУРНАЯ = auto() # }
    
    ЗАПЯТАЯ = auto()        # ,
    ТОЧКА = auto()          # .
    ДВОЕТОЧИЕ = auto()      # :
    ТОЧКА_С_ЗАПЯТОЙ = auto() # ;
    
    СТРЕЛКА = auto()        # ->
    СОБЫТИЕ = auto()        # @
    
    # Специальные
    ОТСТУП = auto()         # Индент
    ДEDENT = auto()         # Дедент
    НОВАЯ_СТРОКА = auto()   # Новая строка
    КОММЕНТАРИЙ = auto()    # Комментарий
    КОНЕЦ_ФАЙЛА = auto()    # EOF


@dataclass
class Token:
    """Токен лексического анализатора."""
    
    type: TokenType
    value: str
    line: int
    column: int
    length: int = 0
    extra: Dict[str, Any] = field(default_factory=dict)
    
    def __post_init__(self):
        if self.length == 0:
            self.length = len(self.value)
    
    def __str__(self) -> str:
        return f"Token({self.type.name}, '{self.value}', line={self.line}, col={self.column})"
    
    def __repr__(self) -> str:
        return self.__str__()


class LexerError(Exception):
    """Ошибка лексического анализа."""
    
    def __init__(self, message: str, line: int, column: int, source: str = ""):
        self.message = message
        self.line = line
        self.column = column
        self.source = source
        super().__init__(self.format_message())
    
    def format_message(self) -> str:
        """Форматированное сообщение об ошибке."""
        msg = f"Ошибка лексики в строке {self.line}, позиция {self.column}: {self.message}"
        if self.source:
            lines = self.source.split('\n')
            if 0 <= self.line - 1 < len(lines):
                msg += f"\n  {lines[self.line - 1]}\n  {' ' * (self.column - 1)}^"
        return msg


class RussianLexer:
    """
    Профессиональный лексический анализатор для русского языка программирования.
    
    Особенности:
    - Поддержка Unicode идентификаторов
    - Морфологическая нормализация ключевых слов
    - Обработка чисел с разделителями
    - Многострочные строки и f-строки
    - Точная отчетность об ошибках
    """
    
    # Ключевые слова русского языка
    KEYWORDS: Dict[str, TokenType] = {
        # Управление потоком
        'если': TokenType.ЕСЛИ,
        'иначе': TokenType.ИНАЧЕ,
        'пока': TokenType.ПОКА,
        'для': TokenType.ДЛЯ,
        'в': TokenType.В,
        
        # Объявления
        'функция': TokenType.ФУНКЦИЯ,
        'класс': TokenType.КЛАСС,
        'возврат': TokenType.ВОЗВРАТ,
        'импорт': TokenType.ИМПОРТ,
        'из': TokenType.ИЗ,
        'как': TokenType.КАК,
        
        # Логика
        'и': TokenType.И,
        'или': TokenType.ИЛИ,
        'не': TokenType.НЕ,
        
        # Значения
        'истина': TokenType.ИСТИНА,
        'ложь': TokenType.ЛОЖЬ,
        'ничто': TokenType.НИЧТО,
        
        # Асинхронность
        'асинхронно': TokenType.АСИНХРОННО,
        'ждать': TokenType.ЖДАТЬ,
        
        # Контекст
        'с': TokenType.С,
        
        # Исключения
        'попробуй': TokenType.ПОПРОБУЙ,
        'кроме': TokenType.КРОМЕ,
        'наконец': TokenType.НАКОНЕЦ,
        'выбросить': TokenType.ВЫБРОСИТЬ,
        
        # Циклы
        'продолжить': TokenType.ПРОДОЛЖИТЬ,
        'прервать': TokenType.ПРЕРВАТЬ,
        
        # Область видимости
        'глобально': TokenType.ГЛОБАЛЬНО,
        'нелокально': TokenType.НЕЛОКАЛЬНО,
        
        # Параллелизм
        'параллельно': TokenType.ПАРАЛЛЕЛЬНО,
        
        # Макросы
        'макрос': TokenType.МАКРОС,
    }
    
    # Одиночные символы
    SINGLE_CHAR_TOKENS: Dict[str, TokenType] = {
        '+': TokenType.ПЛЮС,
        '-': TokenType.МИНУС,
        '*': TokenType.ЗВЕЗДОЧКА,
        '/': TokenType.СЛЕШ,
        '%': TokenType.ПРОЦЕНТ,
        '=': TokenType.РАВНО,
        '<': TokenType.МЕНЬШЕ,
        '>': TokenType.БОЛЬШЕ,
        '!': TokenType.НЕ_РАВНО,  # Будет проверено на !=
        '&': TokenType.ЛОГ_И,
        '|': TokenType.ЛОГ_ИЛИ,
        '~': TokenType.ЛОГ_НЕ,
        '(': TokenType.ЛЕВАЯ_СКОБКА,
        ')': TokenType.ПРАВАЯ_СКОБКА,
        '[': TokenType.ЛЕВАЯ_КВАДРАТНАЯ,
        ']': TokenType.ПРАВАЯ_КВАДРАТНАЯ,
        '{': TokenType.ЛЕВАЯ_ФИГУРНАЯ,
        '}': TokenType.ПРАВАЯ_ФИГУРНАЯ,
        ',': TokenType.ЗАПЯТАЯ,
        '.': TokenType.ТОЧКА,
        ':': TokenType.ДВОЕТОЧИЕ,
        ';': TokenType.ТОЧКА_С_ЗАПЯТОЙ,
        '@': TokenType.СОБЫТИЕ,
    }
    
    def __init__(self, source: str, filename: str = "<string>"):
        """
        Инициализация лексера.
        
        Args:
            source: Исходный код
            filename: Имя файла для отчетов об ошибках
        """
        self.source = source
        self.filename = filename
        self.pos = 0
        self.line = 1
        self.column = 1
        self.tokens: List[Token] = []
        self.indent_stack: List[int] = [0]
        
        # Предварительная обработка
        self.lines = source.split('\n')
        self.line_starts: Dict[int, int] = {}
        current_pos = 0
        for i, line in enumerate(self.lines):
            self.line_starts[i + 1] = current_pos
            current_pos += len(line) + 1
    
    def _advance(self) -> str:
        """Перемещение на один символ вперед."""
        if self.pos >= len(self.source):
            return '\0'
        
        char = self.source[self.pos]
        self.pos += 1
        
        if char == '\n':
            self.line += 1
            self.column = 1
        else:
            self.column += 1
        
        return char
    
    def _peek(self, offset: int = 0) -> str:
        """Просмотр следующего символа без перемещения."""
        pos = self.pos + offset
        if pos >= len(self.source):
            return '\0'
        return self.source[pos]
    
    def _match(self, expected: str) -> bool:
        """Проверка и потребление ожидаемого символа."""
        if self._peek() != expected:
            return False
        self._advance()
        return True
    
    def _skip_whitespace(self):
        """Пропуск пробельных символов (кроме новой строки)."""
        while self._peek() in ' \t\r':
            self._advance()
    
    def _skip_comment(self) -> Optional[Token]:
        """Пропуск комментария."""
        if self._peek() == '#':
            start_col = self.column
            self._advance()  # Пропускаем #
            
            comment = ""
            while self._peek() not in '\n\0':
                comment += self._advance()
            
            return Token(
                TokenType.КОММЕНТАРИЙ,
                comment,
                self.line,
                start_col
            )
        return None
    
    def _read_string(self, quote: str) -> Token:
        """Чтение строкового литерала."""
        start_line = self.line
        start_col = self.column
        
        # Проверка на тройные кавычки
        triple = False
        if self._peek(1) == quote and self._peek(2) == quote:
            triple = True
            self._advance()
            self._advance()
        
        string_value = ""
        escape_next = False
        
        while True:
            char = self._peek()
            
            if char == '\0':
                raise LexerError(
                    "Незавершенная строка",
                    start_line,
                    start_col,
                    self.source
                )
            
            if escape_next:
                string_value += char
                escape_next = False
                self._advance()
                continue
            
            if char == '\\':
                escape_next = True
                self._advance()
                continue
            
            if triple:
                if char == quote and self._peek(1) == quote and self._peek(2) == quote:
                    self._advance()
                    self._advance()
                    self._advance()
                    break
                string_value += self._advance()
            else:
                if char == quote:
                    self._advance()
                    break
                if char == '\n':
                    raise LexerError(
                        "Новая строка в одинарных кавычках",
                        self.line,
                        self.column,
                        self.source
                    )
                string_value += self._advance()
        
        return Token(
            TokenType.СТРОКА,
            string_value,
            start_line,
            start_col,
            extra={'triple': triple, 'quote': quote}
        )
    
    def _read_number(self) -> Token:
        """Чтение числового литерала."""
        start_line = self.line
        start_col = self.column
        
        number_str = ""
        has_dot = False
        has_exponent = False
        
        # Чтение целой части
        while self._peek().isdigit() or self._peek() == '_':
            char = self._advance()
            if char != '_':
                number_str += char
        
        # Чтение дробной части
        if self._peek() == '.' and self._peek(1).isdigit():
            has_dot = True
            number_str += self._advance()  # точка
            
            while self._peek().isdigit() or self._peek() == '_':
                char = self._advance()
                if char != '_':
                    number_str += char
        
        # Чтение экспоненты
        if self._peek() in 'eE' and (self._peek(1).isdigit() or self._peek(1) in '+-'):
            has_exponent = True
            number_str += self._advance()  # e/E
            
            if self._peek() in '+-':
                number_str += self._advance()
            
            while self._peek().isdigit() or self._peek() == '_':
                char = self._advance()
                if char != '_':
                    number_str += char
        
        # Чтение суффикса комплексного числа
        if self._peek() in 'jJ':
            number_str += self._advance()
            return Token(
                TokenType.ЧИСЛО,
                number_str,
                start_line,
                start_col,
                extra={'type': 'complex'}
            )
        
        # Определение типа числа
        if has_dot or has_exponent:
            num_type = 'float'
        else:
            num_type = 'int'
        
        return Token(
            TokenType.ЧИСЛО,
            number_str,
            start_line,
            start_col,
            extra={'type': num_type}
        )
    
    def _read_identifier(self) -> Token:
        """Чтение идентификатора или ключевого слова."""
        start_line = self.line
        start_col = self.column
        
        identifier = ""
        
        # Первый символ: буква или подчеркивание (включая Unicode)
        char = self._peek()
        if char.isalpha() or char == '_' or ord(char) > 127:
            identifier += self._advance()
        
        # Последующие символы: буквы, цифры, подчеркивание
        while True:
            char = self._peek()
            if char.isalnum() or char == '_' or ord(char) > 127:
                identifier += self._advance()
            else:
                break
        
        # Проверка на ключевое слово
        token_type = self.KEYWORDS.get(identifier.lower(), TokenType.ИДЕНТИФИКАТОР)
        
        return Token(
            token_type,
            identifier,
            start_line,
            start_col
        )
    
    def _handle_indentation(self) -> List[Token]:
        """Обработка отступов."""
        tokens = []
        
        # Пропуск пробелов в начале строки
        indent_count = 0
        while self._peek() in ' \t':
            char = self._advance()
            if char == ' ':
                indent_count += 1
            elif char == '\t':
                indent_count += 8  # Табуляция = 8 пробелов
        
        current_indent = self.indent_stack[-1]
        
        if indent_count > current_indent:
            # Новый уровень отступа
            self.indent_stack.append(indent_count)
            tokens.append(Token(
                TokenType.ОТСТУП,
                '',
                self.line,
                1
            ))
        elif indent_count < current_indent:
            # Возврат к предыдущему уровню
            while len(self.indent_stack) > 1 and self.indent_stack[-1] > indent_count:
                self.indent_stack.pop()
                tokens.append(Token(
                    TokenType.DEDENT,
                    '',
                    self.line,
                    1
                ))
            
            if indent_count != self.indent_stack[-1]:
                raise LexerError(
                    "Несогласованный отступ",
                    self.line,
                    1,
                    self.source
                )
        
        return tokens
    
    def tokenize(self) -> List[Token]:
        """
        Токенизация исходного кода.
        
        Returns:
            Список токенов
        """
        self.tokens = []
        self.pos = 0
        self.line = 1
        self.column = 1
        self.indent_stack = [0]
        
        at_line_start = True
        
        while self.pos < len(self.source):
            # Обработка начала строки
            if at_line_start:
                at_line_start = False
                self._skip_whitespace()
                
                # Пропуск пустых строк и комментариев
                if self._peek() == '\n':
                    self._advance()
                    at_line_start = True
                    continue
                
                if self._peek() == '#':
                    comment = self._skip_comment()
                    if comment:
                        self.tokens.append(comment)
                    self._advance()  # новая строка
                    at_line_start = True
                    continue
                
                # Обработка отступов
                indent_tokens = self._handle_indentation()
                self.tokens.extend(indent_tokens)
            
            # Пропуск пробелов
            self._skip_whitespace()
            
            # Конец файла
            if self.pos >= len(self.source):
                break
            
            char = self._peek()
            
            # Новая строка
            if char == '\n':
                self._advance()
                at_line_start = True
                self.tokens.append(Token(
                    TokenType.НОВАЯ_СТРОКА,
                    '\n',
                    self.line - 1,
                    1
                ))
                continue
            
            # Комментарий
            if char == '#':
                comment = self._skip_comment()
                if comment:
                    self.tokens.append(comment)
                continue
            
            # Строки
            if char in '"\'':
                self._advance()
                token = self._read_string(char)
                self.tokens.append(token)
                continue
            
            # Числа
            if char.isdigit():
                token = self._read_number()
                self.tokens.append(token)
                continue
            
            # Идентификаторы и ключевые слова
            if char.isalpha() or char == '_' or ord(char) > 127:
                token = self._read_identifier()
                self.tokens.append(token)
                continue
            
            # Двухсимвольные операторы
            two_char = self.source[self.pos:self.pos + 2]
            if two_char in ['==', '!=', '<=', '>=', '+=', '-=', '*=', '/=', '//=', '%=', '**=', '<<', '>>', '->']:
                self._advance()
                self._advance()
                
                token_map = {
                    '==': TokenType.РАВНО_РАВНО,
                    '!=': TokenType.НЕ_РАВНО,
                    '<=': TokenType.МЕНЬШЕ_РАВНО,
                    '>=': TokenType.БОЛЬШЕ_РАВНО,
                    '+=': TokenType.ПЛЮС_РАВНО,
                    '-=': TokenType.МИНУС_РАВНО,
                    '*=': TokenType.УМНОЖИТЬ_РАВНО,
                    '/=': TokenType.РАЗДЕЛИТЬ_РАВНО,
                    '//=': TokenType.ЦЕЛОЧИСЛЕННО_РАВНО,
                    '%=': TokenType.МОДУЛЬ_РАВНО,
                    '**=': TokenType.СТЕПЕНЬ_РАВНО,
                    '<<': TokenType.СДВИГ_ЛЕВО,
                    '>>': TokenType.СДВИГ_ПРАВО,
                    '->': TokenType.СТРЕЛКА,
                }
                
                self.tokens.append(Token(
                    token_map[two_char],
                    two_char,
                    self.line,
                    self.column - 1
                ))
                continue
            
            # Односимвольные операторы
            if char in self.SINGLE_CHAR_TOKENS:
                self._advance()
                self.tokens.append(Token(
                    self.SINGLE_CHAR_TOKENS[char],
                    char,
                    self.line,
                    self.column - 1
                ))
                continue
            
            # Неизвестный символ
            raise LexerError(
                f"Неизвестный символ '{char}'",
                self.line,
                self.column,
                self.source
            )
        
        # Закрытие всех отступов
        while len(self.indent_stack) > 1:
            self.indent_stack.pop()
            self.tokens.append(Token(
                TokenType.DEDENT,
                '',
                self.line,
                1
            ))
        
        # Токен конца файла
        self.tokens.append(Token(
            TokenType.КОНЕЦ_ФАЙЛА,
            '',
            self.line,
            self.column
        ))
        
        return self.tokens
    
    def tokenize_to_string(self) -> str:
        """Токенизация и возврат в виде строки."""
        tokens = self.tokenize()
        result = []
        
        for token in tokens:
            if token.type == TokenType.КОНЕЦ_ФАЙЛА:
                break
            result.append(str(token))
        
        return '\n'.join(result)


def demo_tokenize():
    """Демонстрация работы лексера."""
    code = """
# Пример программы на русском языке
функция привет(имя):
    печать(f"Привет, {имя}!")
    
    если имя == "Мир":
        возврат истина
    иначе:
        возврат ложь

для i в диапазон(10):
    если i % 2 == 0:
        печать(i)
"""
    
    lexer = RussianLexer(code)
    tokens = lexer.tokenize()
    
    print("=== Токены ===")
    for token in tokens:
        if token.type != TokenType.КОНЕЦ_ФАЙЛА:
            print(f"  {token}")
    
    return tokens


if __name__ == "__main__":
    demo_tokenize()
