"""
Лексический анализатор для языка Русский Питон
Версия 0.1.0

Поддерживаемые токены:
- Ключевые слова: если, иначе, пока, для, функция, класс, вернуть, импорт, из
- Типы данных: целый, дробный, строка, булевый, список, кортеж, словарь
- Операторы: +, -, *, /, //, %, **, ==, !=, <, >, <=, >=, =, +=, -=, *=, /=
- Логические операторы: и, или, не
- Скобки и разделители: (, ), [, ], {, }, :, ,, ., ;
- Идентификаторы и числа
- Строки (одинарные, двойные, тройные)
- Комментарии (однострочные и многострочные)
"""

import re
from enum import Enum, auto
from dataclasses import dataclass, field
from typing import List, Optional, Dict, Any, Tuple
from collections import OrderedDict


class TokenType(Enum):
    """Типы токенов для лексера"""
    # Ключевые слова
    ЕСЛИ = auto()
    ИНАЧЕ = auto()
    ПОКА = auto()
    ДЛЯ = auto()
    ФУНКЦИЯ = auto()
    КЛАСС = auto()
    ВЕРНУТЬ = auto()
    ИМПОРТ = auto()
    ИЗ = auto()
    КАК = auto()
    
    # Типы данных
    ЦЕЛЫЙ = auto()
    ДРОБНЫЙ = auto()
    СТРОКА = auto()
    БУЛЕВЫЙ = auto()
    СПИСОК = auto()
    КОРТЕЖ = auto()
    СЛОВАРЬ = auto()
    НИЧТО = auto()
    
    # Логические значения
    ИСТИНА = auto()
    ЛОЖЬ = auto()
    
    # Логические операторы
    И = auto()
    ИЛИ = auto()
    НЕ = auto()
    
    # Операторы присваивания и сравнения
    ПРИСВОИТЬ = auto()
    РАВНО = auto()
    НЕ_РАВНО = auto()
    МЕНЬШЕ = auto()
    БОЛЬШЕ = auto()
    МЕНЬШЕ_ИЛИ_РАВНО = auto()
    БОЛЬШЕ_ИЛИ_РАВНО = auto()
    
    # Арифметические операторы
    ПЛЮС = auto()
    МИНУС = auto()
    УМНОЖИТЬ = auto()
    РАЗДЕЛИТЬ = auto()
    ЦЕЛОЧИСЛЕННОЕ_ДЕЛЕНИЕ = auto()
    ОСТАТОК = auto()
    СТЕПЕНЬ = auto()
    
    # Составные операторы
    ПЛЮС_РАВНО = auto()
    МИНУС_РАВНО = auto()
    УМНОЖИТЬ_РАВНО = auto()
    РАЗДЕЛИТЬ_РАВНО = auto()
    ОСТАТОК_РАВНО = auto()
    СТЕПЕНЬ_РАВНО = auto()
    
    # Скобки и разделители
    ЛЕВАЯ_СКОБКА = auto()
    ПРАВАЯ_СКОБКА = auto()
    ЛЕВАЯ_КВАДРАТНАЯ = auto()
    ПРАВАЯ_КВАДРАТНАЯ = auto()
    ЛЕВАЯ_ФИГУРНАЯ = auto()
    ПРАВАЯ_ФИГУРНАЯ = auto()
    ДВОЕТОЧИЕ = auto()
    ЗАПЯТАЯ = auto()
    ТОЧКА = auto()
    ТОЧКА_С_ЗАПЯТОЙ = auto()
    
    # Литералы
    ЧИСЛО = auto()
    ДРОБНОЕ_ЧИСЛО = auto()
    СТРОКА_ЛИТ = auto()
    ИДЕНТИФИКАТОР = auto()
    
    # Специальные токены
    НОВАЯ_СТРОКА = auto()
    КОНЕЦ_ФАЙЛА = auto()
    КОММЕНТАРИЙ = auto()
    НЕИЗВЕСТНЫЙ = auto()


@dataclass
class Token:
    """Представление токена"""
    type: TokenType
    value: Any
    line: int
    column: int
    source: str = ""
    
    def __str__(self) -> str:
        return f"Token({self.type.name}, {repr(self.value)}, {self.line}:{self.column})"
    
    def __repr__(self) -> str:
        return self.__str__()


@dataclass
class LexerConfig:
    """Конфигурация лексера"""
    track_positions: bool = True
    skip_whitespace: bool = True
    skip_comments: bool = False
    case_sensitive: bool = True
    allow_unicode_identifiers: bool = True


class LexerError(Exception):
    """Исключение лексера"""
    def __init__(self, message: str, line: int = 0, column: int = 0, source: str = ""):
        self.message = message
        self.line = line
        self.column = column
        self.source = source
        super().__init__(self.format_message())
    
    def format_message(self) -> str:
        pos = f"строка {self.line}, столбец {self.column}" if self.line > 0 else "неизвестная позиция"
        return f"Лексическая ошибка в {pos}: {self.message}"


class RussianLexer:
    """
    Лексический анализатор для русского языка программирования
    
    Поддерживает:
    - Русские ключевые слова
    - Юникод идентификаторы
    - Многострочные строки
    - Вложенные комментарии
    - Числа с разделителями (1_000_000)
    - Экранированные последовательности
    """
    
    # Ключевые слова русского языка
    KEYWORDS = {
        'если': TokenType.ЕСЛИ,
        'иначе': TokenType.ИНАЧЕ,
        'пока': TokenType.ПОКА,
        'для': TokenType.ДЛЯ,
        'функция': TokenType.ФУНКЦИЯ,
        'класс': TokenType.КЛАСС,
        'вернуть': TokenType.ВЕРНУТЬ,
        'импорт': TokenType.ИМПОРТ,
        'из': TokenType.ИЗ,
        'как': TokenType.КАК,
        
        'целый': TokenType.ЦЕЛЫЙ,
        'дробный': TokenType.ДРОБНЫЙ,
        'строка': TokenType.СТРОКА,
        'булевый': TokenType.БУЛЕВЫЙ,
        'список': TokenType.СПИСОК,
        'кортеж': TokenType.КОРТЕЖ,
        'словарь': TokenType.СЛОВАРЬ,
        'ничто': TokenType.НИЧТО,
        
        'истина': TokenType.ИСТИНА,
        'ложь': TokenType.ЛОЖЬ,
        
        'и': TokenType.И,
        'или': TokenType.ИЛИ,
        'не': TokenType.НЕ,
    }
    
    # Паттерны для токенов
    TOKEN_PATTERNS: List[Tuple[TokenType, str]] = [
        # Составные операторы
        (TokenType.ПЛЮС_РАВНО, r'\+='),
        (TokenType.МИНУС_РАВНО, r'-='),
        (TokenType.УМНОЖИТЬ_РАВНО, r'\*='),
        (TokenType.РАЗДЕЛИТЬ_РАВНО, r'/='),
        (TokenType.ОСТАТОК_РАВНО, r'%='),
        (TokenType.СТЕПЕНЬ_РАВНО, r'\*\*='),
        
        # Сравнения
        (TokenType.РАВНО, r'=='),
        (TokenType.НЕ_РАВНО, r'!='),
        (TokenType.МЕНЬШЕ_ИЛИ_РАВНО, r'<='),
        (TokenType.БОЛЬШЕ_ИЛИ_РАВНО, r'>='),
        
        # Арифметика
        (TokenType.СТЕПЕНЬ, r'\*\*'),
        (TokenType.ЦЕЛОЧИСЛЕННОЕ_ДЕЛЕНИЕ, r'//'),
        
        # Присваивание
        (TokenType.ПРИСВОИТЬ, r'='),
        
        # Операторы
        (TokenType.ПЛЮС, r'\+'),
        (TokenType.МИНУС, r'-'),
        (TokenType.УМНОЖИТЬ, r'\*'),
        (TokenType.РАЗДЕЛИТЬ, r'/'),
        (TokenType.ОСТАТОК, r'%'),
        
        # Скобки
        (TokenType.ЛЕВАЯ_СКОБКА, r'\('),
        (TokenType.ПРАВАЯ_СКОБКА, r'\)'),
        (TokenType.ЛЕВАЯ_КВАДРАТНАЯ, r'\['),
        (TokenType.ПРАВАЯ_КВАДРАТНАЯ, r'\]'),
        (TokenType.ЛЕВАЯ_ФИГУРНАЯ, r'\{'),
        (TokenType.ПРАВАЯ_ФИГУРНАЯ, r'\}'),
        
        # Разделители
        (TokenType.ДВОЕТОЧИЕ, r':'),
        (TokenType.ЗАПЯТАЯ, r','),
        (TokenType.ТОЧКА, r'\.'),
        (TokenType.ТОЧКА_С_ЗАПЯТОЙ, r';'),
        
        # Сравнения (одиночные)
        (TokenType.МЕНЬШЕ, r'<'),
        (TokenType.БОЛЬШЕ, r'>'),
    ]
    
    def __init__(self, config: Optional[LexerConfig] = None):
        self.config = config or LexerConfig()
        self.source = ""
        self.pos = 0
        self.line = 1
        self.column = 1
        self.tokens: List[Token] = []
        self.errors: List[LexerError] = []
        self._compiled_patterns: Optional[List[Tuple[TokenType, re.Pattern]]] = None
    
    def _compile_patterns(self):
        """Компиляция регулярных выражений для производительности"""
        if self._compiled_patterns is None:
            self._compiled_patterns = [
                (token_type, re.compile(pattern))
                for token_type, pattern in self.TOKEN_PATTERNS
            ]
    
    def tokenize(self, source: str) -> List[Token]:
        """
        Токенизация исходного кода
        
        :param source: Исходный код на русском языке
        :return: Список токенов
        :raises LexerError: При обнаружении лексической ошибки
        """
        self.source = source
        self.pos = 0
        self.line = 1
        self.column = 1
        self.tokens = []
        self.errors = []
        
        self._compile_patterns()
        
        while self.pos < len(self.source):
            token = self._next_token()
            if token:
                if token.type == TokenType.КОММЕНТАРИЙ and not self.config.skip_comments:
                    self.tokens.append(token)
                elif token.type not in (TokenType.КОММЕНТАРИЙ,) or not self.config.skip_whitespace:
                    if token.type != TokenType.КОММЕНТАРИЙ:
                        self.tokens.append(token)
        
        # Добавляем токен конца файла
        self.tokens.append(Token(
            type=TokenType.КОНЕЦ_ФАЙЛА,
            value=None,
            line=self.line,
            column=self.column,
            source=self.source
        ))
        
        if self.errors:
            raise self.errors[0]
        
        return self.tokens
    
    def _next_token(self) -> Optional[Token]:
        """Получение следующего токена"""
        # Пропуск пробельных символов
        if self._skip_whitespace():
            return None
        
        # Проверка на комментарий
        comment = self._try_comment()
        if comment:
            return comment
        
        # Проверка на строку
        string_token = self._try_string()
        if string_token:
            return string_token
        
        # Проверка на число
        number_token = self._try_number()
        if number_token:
            return number_token
        
        # Проверка на идентификатор или ключевое слово
        ident_token = self._try_identifier()
        if ident_token:
            return ident_token
        
        # Проверка на операторы и символы
        op_token = self._try_operator()
        if op_token:
            return op_token
        
        # Неизвестный символ
        char = self._current_char()
        start_line, start_col = self.line, self.column
        self._advance()
        
        error = LexerError(f"Неожиданный символ: '{char}'", start_line, start_col, self.source)
        self.errors.append(error)
        
        return Token(
            type=TokenType.НЕИЗВЕСТНЫЙ,
            value=char,
            line=start_line,
            column=start_col,
            source=self.source
        )
    
    def _skip_whitespace(self) -> bool:
        """Пропуск пробельных символов"""
        skipped = False
        while self.pos < len(self.source) and self.source[self.pos].isspace():
            if self.source[self.pos] == '\n':
                self.line += 1
                self.column = 1
            else:
                self.column += 1
            self.pos += 1
            skipped = True
        return skipped
    
    def _try_comment(self) -> Optional[Token]:
        """Попытка распознать комментарий"""
        if self.pos + 1 >= len(self.source):
            return None
        
        if self.source[self.pos:self.pos + 2] == '#':
            start_line, start_col = self.line, self.column
            self.pos += 2
            self.column += 2
            
            start_pos = self.pos
            while self.pos < len(self.source) and self.source[self.pos] != '\n':
                self.pos += 1
                self.column += 1
            
            comment_text = self.source[start_pos:self.pos]
            
            return Token(
                type=TokenType.КОММЕНТАРИЙ,
                value=comment_text,
                line=start_line,
                column=start_col,
                source=self.source
            )
        
        # Многострочный комментарий
        if self.pos + 1 < len(self.source) and self.source[self.pos:self.pos + 2] == '//':
            return self._multiline_comment()
        
        return None
    
    def _multiline_comment(self) -> Token:
        """Обработка многострочного комментария // ... //"""
        start_line, start_col = self.line, self.column
        self.pos += 2
        self.column += 2
        
        start_pos = self.pos
        depth = 1
        
        while self.pos < len(self.source) and depth > 0:
            if self.pos + 1 < len(self.source):
                if self.source[self.pos:self.pos + 2] == '//':
                    depth += 1
                    self.pos += 2
                    self.column += 2
                    continue
                elif self.source[self.pos:self.pos + 2] == '/':
                    pass
            
            if self.source[self.pos] == '\n':
                self.line += 1
                self.column = 1
            else:
                self.column += 1
            self.pos += 1
        
        comment_text = self.source[start_pos:self.pos - 2] if self.pos >= 2 else ""
        
        return Token(
            type=TokenType.КОММЕНТАРИЙ,
            value=comment_text,
            line=start_line,
            column=start_col,
            source=self.source
        )
    
    def _try_string(self) -> Optional[Token]:
        """Попытка распознать строковый литерал"""
        quote_chars = ['"', "'", '"""', "'''"]
        
        for quote in sorted(quote_chars, key=len, reverse=True):
            if self.source.startswith(quote, self.pos):
                start_line, start_col = self.line, self.column
                self.pos += len(quote)
                self.column += len(quote)
                
                string_parts = []
                is_triple = len(quote) == 3
                
                while self.pos < len(self.source):
                    # Проверка на конец строки
                    if self.source.startswith(quote, self.pos):
                        self.pos += len(quote)
                        self.column += len(quote)
                        break
                    
                    # Обработка экранирования
                    if self.source[self.pos] == '\\':
                        self.pos += 1
                        self.column += 1
                        
                        if self.pos >= len(self.source):
                            error = LexerError("Незавершенная экранированная последовательность", 
                                             self.line, self.column, self.source)
                            self.errors.append(error)
                            break
                        
                        escape_char = self.source[self.pos]
                        if escape_char == 'n':
                            string_parts.append('\n')
                        elif escape_char == 't':
                            string_parts.append('\t')
                        elif escape_char == 'r':
                            string_parts.append('\r')
                        elif escape_char == '\\':
                            string_parts.append('\\')
                        elif escape_char == quote[0]:
                            string_parts.append(quote[0])
                        elif escape_char == '"':
                            string_parts.append('"')
                        elif escape_char == "'":
                            string_parts.append("'")
                        else:
                            string_parts.append('\\' + escape_char)
                        
                        self.pos += 1
                        self.column += 1
                    else:
                        char = self.source[self.pos]
                        string_parts.append(char)
                        
                        if char == '\n':
                            if not is_triple:
                                error = LexerError("Новая строка в одинарной/двойной строке", 
                                                 self.line, self.column, self.source)
                                self.errors.append(error)
                            self.line += 1
                            self.column = 1
                        else:
                            self.column += 1
                        
                        self.pos += 1
                
                string_value = ''.join(string_parts)
                
                return Token(
                    type=TokenType.СТРОКА_ЛИТ,
                    value=string_value,
                    line=start_line,
                    column=start_col,
                    source=self.source
                )
        
        return None
    
    def _try_number(self) -> Optional[Token]:
        """Попытка распознать числовой литерал"""
        start_line, start_col = self.line, self.column
        start_pos = self.pos
        
        # Проверка на отрицательное число (если минус перед цифрой)
        has_minus = False
        if (self.pos > 0 and 
            self.source[self.pos - 1] in ' \t\n([{,:;+-*/%<>=!&|^~' and
            self.pos < len(self.source) and 
            self.source[self.pos] == '-'):
            has_minus = True
            self.pos += 1
            self.column += 1
        
        if self.pos >= len(self.source) or not self.source[self.pos].isdigit():
            if has_minus:
                self.pos -= 1
                self.column -= 1
            return None
        
        # Чтение целой части
        while self.pos < len(self.source) and (self.source[self.pos].isdigit() or self.source[self.pos] == '_'):
            if self.source[self.pos] == '_':
                if self.pos + 1 >= len(self.source) or not self.source[self.pos + 1].isdigit():
                    break
            self.pos += 1
            self.column += 1
        
        is_float = False
        
        # Проверка на дробную часть
        if self.pos < len(self.source) and self.source[self.pos] == '.':
            if self.pos + 1 < len(self.source) and self.source[self.pos + 1].isdigit():
                is_float = True
                self.pos += 1
                self.column += 1
                
                while self.pos < len(self.source) and (self.source[self.pos].isdigit() or self.source[self.pos] == '_'):
                    if self.source[self.pos] == '_':
                        if self.pos + 1 >= len(self.source) or not self.source[self.pos + 1].isdigit():
                            break
                    self.pos += 1
                    self.column += 1
        
        # Проверка на экспоненциальную форму
        if self.pos < len(self.source) and self.source[self.pos] in 'eE':
            is_float = True
            self.pos += 1
            self.column += 1
            
            if self.pos < len(self.source) and self.source[self.pos] in '+-':
                self.pos += 1
                self.column += 1
            
            if self.pos >= len(self.source) or not self.source[self.pos].isdigit():
                error = LexerError("Ожидаются цифры после экспоненты", self.line, self.column, self.source)
                self.errors.append(error)
            else:
                while self.pos < len(self.source) and self.source[self.pos].isdigit():
                    self.pos += 1
                    self.column += 1
        
        number_str = self.source[start_pos:self.pos]
        if has_minus:
            number_str = '-' + number_str
        
        # Удаление подчеркиваний для парсинга
        clean_number = number_str.replace('_', '')
        
        if is_float:
            try:
                value = float(clean_number)
            except ValueError:
                error = LexerError(f"Некорректное дробное число: {number_str}", start_line, start_col, self.source)
                self.errors.append(error)
                value = 0.0
        else:
            try:
                value = int(clean_number)
            except ValueError:
                error = LexerError(f"Некорректное целое число: {number_str}", start_line, start_col, self.source)
                self.errors.append(error)
                value = 0
        
        token_type = TokenType.ДРОБНОЕ_ЧИСЛО if is_float else TokenType.ЧИСЛО
        
        return Token(
            type=token_type,
            value=value,
            line=start_line,
            column=start_col,
            source=self.source
        )
    
    def _try_identifier(self) -> Optional[Token]:
        """Попытка распознать идентификатор или ключевое слово"""
        if not self._is_identifier_start(self._current_char()):
            return None
        
        start_line, start_col = self.line, self.column
        start_pos = self.pos
        
        # Чтение идентификатора
        while self.pos < len(self.source) and self._is_identifier_char(self.source[self.pos]):
            self.pos += 1
            self.column += 1
        
        identifier = self.source[start_pos:self.pos]
        
        # Проверка на ключевое слово
        if identifier.lower() in self.KEYWORDS:
            token_type = self.KEYWORDS[identifier.lower()]
        else:
            token_type = TokenType.ИДЕНТИФИКАТОР
        
        return Token(
            type=token_type,
            value=identifier,
            line=start_line,
            column=start_col,
            source=self.source
        )
    
    def _is_identifier_start(self, char: str) -> bool:
        """Проверка, может ли символ быть началом идентификатора"""
        if char is None:
            return False
        return char.isalpha() or char == '_' or ord(char) > 127
    
    def _is_identifier_char(self, char: str) -> bool:
        """Проверка, может ли символ быть частью идентификатора"""
        if char is None:
            return False
        return char.isalnum() or char == '_' or ord(char) > 127
    
    def _try_operator(self) -> Optional[Token]:
        """Попытка распознать оператор"""
        for token_type, pattern in self._compiled_patterns:
            match = pattern.match(self.source, self.pos)
            if match:
                start_line, start_col = self.line, self.column
                matched_text = match.group(0)
                
                self.pos += len(matched_text)
                self.column += len(matched_text)
                
                return Token(
                    type=token_type,
                    value=matched_text,
                    line=start_line,
                    column=start_col,
                    source=self.source
                )
        
        return None
    
    def _current_char(self) -> Optional[str]:
        """Получение текущего символа"""
        if self.pos >= len(self.source):
            return None
        return self.source[self.pos]
    
    def _advance(self):
        """Переход к следующему символу"""
        if self.pos < len(self.source):
            if self.source[self.pos] == '\n':
                self.line += 1
                self.column = 1
            else:
                self.column += 1
            self.pos += 1
    
    def get_token_stream(self) -> List[Token]:
        """Получение потока токенов (алиас для tokenize)"""
        return self.tokenize(self.source)
    
    def peek_token(self, index: int = 0) -> Optional[Token]:
        """Просмотр токена по индексу"""
        if not self.tokens:
            self.tokenize(self.source)
        
        if 0 <= index < len(self.tokens):
            return self.tokens[index]
        return None
    
    def get_errors(self) -> List[LexerError]:
        """Получение списка ошибок"""
        return self.errors
    
    def has_errors(self) -> bool:
        """Проверка наличия ошибок"""
        return len(self.errors) > 0


def tokenize_source(source: str, config: Optional[LexerConfig] = None) -> List[Token]:
    """
    Удобная функция для токенизации исходного кода
    
    :param source: Исходный код
    :param config: Конфигурация лексера
    :return: Список токенов
    """
    lexer = RussianLexer(config)
    return lexer.tokenize(source)


def print_tokens(tokens: List[Token], show_source: bool = False):
    """Вывод токенов в читаемом формате"""
    print("=" * 80)
    print("ТОКЕНИЗИРОВАННЫЙ ВЫВОД")
    print("=" * 80)
    
    for i, token in enumerate(tokens):
        if token.type == TokenType.КОНЕЦ_ФАЙЛА:
            print(f"{i:4d}: EOF")
            break
        print(f"{i:4d}: {token.type.name:25s} | {repr(token.value):20s} | L{token.line:3d}:C{token.column:3d}")
    
    print("=" * 80)
    print(f"Всего токенов: {len(tokens) - 1}")  # Минус EOF
    print("=" * 80)


if __name__ == "__main__":
    # Демо-пример использования лексера
    demo_code = '''
# Это пример программы на Русском Питоне
функция главная():
    печать("Привет, мир!")
    
    число х = 10
    число у = 20
    
    если х < у:
        печать("х меньше у")
    иначе:
        печать("х больше или равен у")
    
    пока х < 100:
        х = х + 5
    
    вернуть х
'''
    
    print("Исходный код:")
    print(demo_code)
    print("\n")
    
    try:
        tokens = tokenize_source(demo_code)
        print_tokens(tokens)
        
        print(f"\n✅ Успешная токенизация! Найдено {len(tokens) - 1} токенов.")
    except LexerError as e:
        print(f"\n❌ Ошибка: {e}")
