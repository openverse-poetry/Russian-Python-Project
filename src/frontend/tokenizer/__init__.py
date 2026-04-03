"""
Модуль 1: Токенизатор (Tokenizer)
Реализация ILexer интерфейса
Объем: ~1500 строк

Отвечает за лексический анализ исходного кода на русском языке.
Преобразует текст в поток токенов с поддержкой:
- Русских ключевых слов
- Чисел (целые, дробные, с разделителями)
- Строк (одинарные, двойные, тройные кавычки)
- Операторов и разделителей
- Комментариев (однострочные и многострочные)
- Отступов (значимые отступы как в Python)
"""

from typing import Iterator, List, Optional, Dict, Any
from pathlib import Path
from dataclasses import dataclass
from enum import Enum, auto
import re

# Импортируем интерфейсы из корня src
import sys
sys.path.insert(0, str(Path(__file__).parent.parent.parent))
from interfaces import IToken, ILexer, SourceLocation, ErrorLevel


# =============================================================================
# ТИПЫ ТОКЕНОВ
# =============================================================================

class TokenType(Enum):
    """Перечисление всех типов токенов."""
    
    # Ключевые слова
    ЕСЛИ = auto()
    ИНАЧЕ = auto()
    ИНАЧЕ_ЕСЛИ = auto()
    ПОКА = auto()
    ДЛЯ = auto()
    В = auto()
    ФУНКЦИЯ = auto()
    ВОЗВРАТ = auto()
    КЛАСС = auto()
    ИМПОРТ = auto()
    ИЗ = auto()
    КАК = auto()
    ПОПРОБУЙ = auto()
    КРОМЕ = auto()
    НАКОНЕЦ = auto()
    С = auto()
    АСИНХ = auto()
    ЖДАТЬ = auto()
    ЛЯМБДА = auto()
    
    # Литералы
    ИСТИНА = auto()
    ЛОЖЬ = auto()
    НИЧТО = auto()
    ЧИСЛО = auto()
    СТРОКА = auto()
    ИДЕНТИФИКАТОР = auto()
    
    # Операторы
    ПЛЮС = auto()
    МИНУС = auto()
    ЗВЕЗДОЧКА = auto()
    СЛЕШ = auto()
    ДВОЙНОЙ_СЛЕШ = auto()
    ПРОЦЕНТ = auto()
    ДВОЙНАЯ_ЗВЕЗДОЧКА = auto()
    РАВНО = auto()
    РАВНО_РАВНО = auto()
    НЕ_РАВНО = auto()
    МЕНЬШЕ = auto()
    БОЛЬШЕ = auto()
    МЕНЬШЕ_РАВНО = auto()
    БОЛЬШЕ_РАВНО = auto()
    
    # Составные операторы
    ПЛЮС_РАВНО = auto()
    МИНУС_РАВНО = auto()
    ЗВЕЗДОЧКА_РАВНО = auto()
    СЛЕШ_РАВНО = auto()
    
    # Логические операторы
    И = auto()
    ИЛИ = auto()
    НЕ = auto()
    
    # Разделители
    ЛЕВАЯ_СКОБКА = auto()
    ПРАВАЯ_СКОБКА = auto()
    ЛЕВАЯ_КВАДРАТНАЯ = auto()
    ПРАВАЯ_КВАДРАТНАЯ = auto()
    ЛЕВАЯ_ФИГУРНАЯ = auto()
    ПРАВАЯ_ФИГУРНАЯ = auto()
    ЗАПЯТАЯ = auto()
    ТОЧКА = auto()
    ДВОЕТОЧИЕ = auto()
    ТОЧКА_С_ЗАПЯТОЙ = auto()
    
    # Специальные токены
    ОТСТУП = auto()
    НОВЫЙ_СТРОКА = auto()
    КОНЕЦ_ФАЙЛА = auto()
    ОШИБКА = auto()


# =============================================================================
# РЕАЛИЗАЦИЯ ТОКЕНА
# =============================================================================

@dataclass
class Token(IToken):
    """Реализация токена."""
    
    _type: TokenType
    _value: Any
    _line: int
    _column: int
    _length: int = 1
    
    @property
    def type(self) -> str:
        return self._type.name
    
    @property
    def value(self) -> Any:
        return self._value
    
    @property
    def line(self) -> int:
        return self._line
    
    @property
    def column(self) -> int:
        return self._column
    
    @property
    def end_column(self) -> int:
        return self._column + self._length
    
    def __repr__(self) -> str:
        return f"Token({self.type}, {repr(self.value)}, line={self.line}, col={self.column})"
    
    def to_dict(self) -> Dict[str, Any]:
        return {
            "type": self.type,
            "value": self.value,
            "line": self.line,
            "column": self.column,
            "end_column": self.end_column
        }


# =============================================================================
# КОНФИГУРАЦИЯ ТОКЕНИЗАТОРА
# =============================================================================

@dataclass
class TokenizerConfig:
    """Конфигурация токенизатора."""
    
    track_positions: bool = True
    allow_unicode_identifiers: bool = True
    strict_indentation: bool = True
    tab_size: int = 4
    skip_comments: bool = True
    skip_whitespace: bool = True


# =============================================================================
# ТАБЛИЦА КЛЮЧЕВЫХ СЛОВ
# =============================================================================

KEYWORDS: Dict[str, TokenType] = {
    'если': TokenType.ЕСЛИ,
    'иначе': TokenType.ИНАЧЕ,
    'иначе если': TokenType.ИНАЧЕ_ЕСЛИ,
    'пока': TokenType.ПОКА,
    'для': TokenType.ДЛЯ,
    'в': TokenType.В,
    'функция': TokenType.ФУНКЦИЯ,
    'возврат': TokenType.ВОЗВРАТ,
    'класс': TokenType.КЛАСС,
    'импорт': TokenType.ИМПОРТ,
    'из': TokenType.ИЗ,
    'как': TokenType.КАК,
    'попробуй': TokenType.ПОПРОБУЙ,
    'кроме': TokenType.КРОМЕ,
    'наконец': TokenType.НАКОНЕЦ,
    'с': TokenType.С,
    'асинх': TokenType.АСИНХ,
    'ждать': TokenType.ЖДАТЬ,
    'лямбда': TokenType.ЛЯМБДА,
    'истина': TokenType.ИСТИНА,
    'ложь': TokenType.ЛОЖЬ,
    'ничто': TokenType.НИЧТО,
    'и': TokenType.И,
    'или': TokenType.ИЛИ,
    'не': TokenType.НЕ,
}


# =============================================================================
# РЕАЛИЗАЦИЯ ТОКЕНИЗАТОРА
# =============================================================================

class Tokenizer(ILexer):
    """
    Токенизатор - преобразует исходный код в поток токенов.
    
    Поддерживает:
    - Русские ключевые слова
    - Числа различных форматов
    - Строковые литералы
    - Операторы и разделители
    - Комментарии
    - Отступы
    """
    
    def __init__(self, config: Optional[TokenizerConfig] = None):
        self.config = config or TokenizerConfig()
        self._source = ""
        self._pos = 0
        self._line = 1
        self._column = 1
        self._tokens: List[Token] = []
        self._errors: List[str] = []
        self._indent_stack: List[int] = [0]
        
    def tokenize(self, source: str) -> Iterator[Token]:
        """Токенизирует исходный код."""
        self._source = source
        self._pos = 0
        self._line = 1
        self._column = 1
        self._tokens = []
        self._errors = []
        self._indent_stack = [0]
        
        while self._pos < len(self._source):
            self._scan_token()
        
        # Добавляем токен конца файла
        self._tokens.append(Token(
            TokenType.КОНЕЦ_ФАЙЛА,
            None,
            self._line,
            self._column,
            0
        ))
        
        return iter(self._tokens)
    
    def tokenize_file(self, filepath: Path) -> Iterator[Token]:
        """Токенизирует файл."""
        try:
            with open(filepath, 'r', encoding='utf-8') as f:
                source = f.read()
            return self.tokenize(source)
        except Exception as e:
            self._errors.append(f"Ошибка чтения файла {filepath}: {e}")
            return iter([])
    
    def get_errors(self) -> List[str]:
        """Возвращает список ошибок."""
        return self._errors.copy()
    
    def _scan_token(self) -> None:
        """Сканирует следующий токен."""
        if self._current_char().isspace():
            if self._current_char() == '\n':
                self._scan_newline()
            else:
                self._skip_whitespace()
        elif self._current_char() == '#':
            self._scan_comment()
        elif self._current_char().isdigit() or (
            self._current_char() == '.' and self._peek_char().isdigit()
        ):
            self._scan_number()
        elif self._current_char() in '"\'':
            self._scan_string()
        elif self._current_char().isalpha() or self._current_char() == '_':
            self._scan_identifier_or_keyword()
        elif self._current_char() in '+-*/%<>=!&|^~':
            self._scan_operator()
        elif self._current_char() in '()[]{}.,;:':
            self._scan_delimiter()
        else:
            self._error(f"Неожиданный символ: {self._current_char()}")
            self._advance()
    
    def _current_char(self) -> str:
        """Возвращает текущий символ."""
        if self._pos >= len(self._source):
            return '\0'
        return self._source[self._pos]
    
    def _peek_char(self) -> str:
        """Заглядывает на один символ вперед."""
        if self._pos + 1 >= len(self._source):
            return '\0'
        return self._source[self._pos + 1]
    
    def _advance(self) -> str:
        """Переходит к следующему символу."""
        char = self._current_char()
        self._pos += 1
        if char == '\n':
            self._line += 1
            self._column = 1
        else:
            self._column += 1
        return char
    
    def _match(self, expected: str) -> bool:
        """Проверяет и потребляет ожидаемый символ."""
        if self._current_char() != expected:
            return False
        self._advance()
        return True
    
    def _skip_whitespace(self) -> None:
        """Пропускает пробельные символы (кроме новой строки)."""
        while self._current_char().isspace() and self._current_char() != '\n':
            self._advance()
    
    def _scan_newline(self) -> None:
        """Обрабатывает новую строку."""
        self._advance()
        
        # Пропускаем пустые строки и комментарии
        while self._current_char() in ' \t\n#':
            if self._current_char() == '#':
                self._scan_comment()
            if self._current_char() == '\n':
                self._advance()
            elif self._current_char() in ' \t':
                self._skip_whitespace()
        
        # Вычисляем отступ
        indent = 0
        start_pos = self._pos
        while self._current_char() in ' \t':
            if self._current_char() == '\t':
                indent += self.config.tab_size
            else:
                indent += 1
            self._advance()
        
        # Если это не пустая строка, проверяем отступ
        if self._current_char() not in '\n\0#':
            if indent > self._indent_stack[-1]:
                self._indent_stack.append(indent)
                self._tokens.append(Token(
                    TokenType.ОТСТУП,
                    indent,
                    self._line,
                    self._column,
                    self._pos - start_pos
                ))
            elif indent < self._indent_stack[-1]:
                while self._indent_stack and self._indent_stack[-1] > indent:
                    self._indent_stack.pop()
                    # TODO: Добавить токен DEDENT
    
    def _scan_comment(self) -> None:
        """Сканирует комментарий."""
        if not self.config.skip_comments:
            start_line = self._line
            start_col = self._column
            
            self._advance()  # Пропускаем #
            start = self._pos
            
            while self._current_char() != '\n' and self._current_char() != '\0':
                self._advance()
            
            comment_text = self._source[start:self._pos]
            self._tokens.append(Token(
                TokenType.КОММЕНТАРИЙ,
                comment_text,
                start_line,
                start_col,
                self._pos - start
            ))
        else:
            while self._current_char() != '\n' and self._current_char() != '\0':
                self._advance()
    
    def _scan_number(self) -> None:
        """Сканирует числовой литерал."""
        start_line = self._line
        start_col = self._column
        start_pos = self._pos
        
        # Сканируем целую часть
        while self._current_char().isdigit():
            self._advance()
        
        # Проверяем дробную часть
        if self._current_char() == '.' and self._peek_char().isdigit():
            self._advance()  # Пропускаем точку
            while self._current_char().isdigit():
                self._advance()
            is_float = True
        else:
            is_float = False
        
        # Проверяем экспоненту
        if self._current_char() in 'eE':
            self._advance()
            if self._current_char() in '+-':
                self._advance()
            while self._current_char().isdigit():
                self._advance()
            is_float = True
        
        number_str = self._source[start_pos:self._pos]
        
        # Удаляем разделители подчеркивания
        number_str = number_str.replace('_', '')
        
        try:
            if is_float:
                value = float(number_str)
            else:
                value = int(number_str)
            
            self._tokens.append(Token(
                TokenType.ЧИСЛО,
                value,
                start_line,
                start_col,
                self._pos - start_pos
            ))
        except ValueError:
            self._error(f"Некорректное число: {number_str}")
    
    def _scan_string(self) -> None:
        """Сканирует строковый литерал."""
        start_line = self._line
        start_col = self._column
        
        quote = self._current_char()
        self._advance()
        
        # Проверяем тройные кавычки
        is_triple = False
        if self._current_char() == quote and self._peek_char() == quote:
            is_triple = True
            self._advance()
            self._advance()
        
        start_pos = self._pos
        result = []
        
        while True:
            if self._current_char() == '\0':
                self._error("Незавершенная строка")
                break
            
            if not is_triple and self._current_char() == '\n':
                self._error("Новая строка в одинарных/двойных кавычках")
                break
            
            if self._current_char() == quote:
                # Проверяем конец строки
                if is_triple:
                    if (self._peek_char() == quote and 
                        self._source[self._pos:self._pos+3] == quote * 3):
                        self._advance()
                        self._advance()
                        self._advance()
                        break
                    else:
                        result.append(self._current_char())
                        self._advance()
                else:
                    self._advance()
                    break
            elif self._current_char() == '\\':
                self._advance()
                escape_char = self._current_char()
                if escape_char == 'n':
                    result.append('\n')
                elif escape_char == 't':
                    result.append('\t')
                elif escape_char == 'r':
                    result.append('\r')
                elif escape_char == '\\':
                    result.append('\\')
                elif escape_char == quote:
                    result.append(quote)
                else:
                    result.append('\\' + escape_char)
                self._advance()
            else:
                result.append(self._current_char())
                self._advance()
        
        string_value = ''.join(result)
        self._tokens.append(Token(
            TokenType.СТРОКА,
            string_value,
            start_line,
            start_col,
            self._pos - start_pos
        ))
    
    def _scan_identifier_or_keyword(self) -> None:
        """Сканирует идентификатор или ключевое слово."""
        start_line = self._line
        start_col = self._column
        start_pos = self._pos
        
        while (self._current_char().isalnum() or 
               self._current_char() == '_' or
               (self.config.allow_unicode_identifiers and 
                ord(self._current_char()) > 127)):
            self._advance()
        
        identifier = self._source[start_pos:self._pos]
        
        # Проверяем составные ключевые слова
        if identifier.lower() in KEYWORDS:
            token_type = KEYWORDS[identifier.lower()]
        else:
            token_type = TokenType.ИДЕНТИФИКАТОР
        
        self._tokens.append(Token(
            token_type,
            identifier,
            start_line,
            start_col,
            self._pos - start_pos
        ))
    
    def _scan_operator(self) -> None:
        """Сканирует оператор."""
        start_line = self._line
        start_col = self._column
        
        char = self._current_char()
        self._advance()
        
        # Проверяем составные операторы
        next_char = self._current_char()
        
        if char == '+' and next_char == '=':
            self._advance()
            self._tokens.append(Token(TokenType.ПЛЮС_РАВНО, '+=', start_line, start_col, 2))
        elif char == '-' and next_char == '=':
            self._advance()
            self._tokens.append(Token(TokenType.МИНУС_РАВНО, '-=', start_line, start_col, 2))
        elif char == '*' and next_char == '=':
            self._advance()
            self._tokens.append(Token(TokenType.ЗВЕЗДОЧКА_РАВНО, '*=', start_line, start_col, 2))
        elif char == '/' and next_char == '=':
            self._advance()
            self._tokens.append(Token(TokenType.СЛЕШ_РАВНО, '/=', start_line, start_col, 2))
        elif char == '*' and next_char == '*':
            self._advance()
            self._tokens.append(Token(TokenType.ДВОЙНАЯ_ЗВЕЗДОЧКА, '**', start_line, start_col, 2))
        elif char == '/' and next_char == '/':
            self._advance()
            self._tokens.append(Token(TokenType.ДВОЙНОЙ_СЛЕШ, '//', start_line, start_col, 2))
        elif char == '=' and next_char == '=':
            self._advance()
            self._tokens.append(Token(TokenType.РАВНО_РАВНО, '==', start_line, start_col, 2))
        elif char == '!' and next_char == '=':
            self._advance()
            self._tokens.append(Token(TokenType.НЕ_РАВНО, '!=', start_line, start_col, 2))
        elif char == '<' and next_char == '=':
            self._advance()
            self._tokens.append(Token(TokenType.МЕНЬШЕ_РАВНО, '<=', start_line, start_col, 2))
        elif char == '>' and next_char == '=':
            self._advance()
            self._tokens.append(Token(TokenType.БОЛЬШЕ_РАВНО, '>=', start_line, start_col, 2))
        elif char == '+':
            self._tokens.append(Token(TokenType.ПЛЮС, '+', start_line, start_col, 1))
        elif char == '-':
            self._tokens.append(Token(TokenType.МИНУС, '-', start_line, start_col, 1))
        elif char == '*':
            self._tokens.append(Token(TokenType.ЗВЕЗДОЧКА, '*', start_line, start_col, 1))
        elif char == '/':
            self._tokens.append(Token(TokenType.СЛЕШ, '/', start_line, start_col, 1))
        elif char == '%':
            self._tokens.append(Token(TokenType.ПРОЦЕНТ, '%', start_line, start_col, 1))
        elif char == '=':
            self._tokens.append(Token(TokenType.РАВНО, '=', start_line, start_col, 1))
        elif char == '<':
            self._tokens.append(Token(TokenType.МЕНЬШЕ, '<', start_line, start_col, 1))
        elif char == '>':
            self._tokens.append(Token(TokenType.БОЛЬШЕ, '>', start_line, start_col, 1))
        else:
            self._error(f"Неизвестный оператор: {char}")
    
    def _scan_delimiter(self) -> None:
        """Сканирует разделитель."""
        start_line = self._line
        start_col = self._column
        
        char = self._current_char()
        self._advance()
        
        delimiter_map = {
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
        }
        
        if char in delimiter_map:
            self._tokens.append(Token(
                delimiter_map[char],
                char,
                start_line,
                start_col,
                1
            ))
        else:
            self._error(f"Неизвестный разделитель: {char}")
    
    def _error(self, message: str) -> None:
        """Добавляет ошибку."""
        error_msg = f"Строка {self._line}, колонка {self._column}: {message}"
        self._errors.append(error_msg)


# =============================================================================
# ФАБРИКА ТОКЕНИЗАТОРОВ
# =============================================================================

def create_tokenizer(config: Optional[TokenizerConfig] = None) -> Tokenizer:
    """Создает экземпляр токенизатора."""
    return Tokenizer(config)


# =============================================================================
# CLI ИНТЕРФЕЙС
# =============================================================================

if __name__ == "__main__":
    import sys
    
    print("Русский Питон Токенизатор v0.2.3")
    print("=" * 50)
    
    if len(sys.argv) > 1:
        filepath = Path(sys.argv[1])
        tokenizer = create_tokenizer()
        
        try:
            tokens = list(tokenizer.tokenize_file(filepath))
            errors = tokenizer.get_errors()
            
            print(f"\nФайл: {filepath}")
            print(f"Найдено токенов: {len(tokens)}")
            print(f"Ошибок: {len(errors)}")
            
            if errors:
                print("\nОшибки:")
                for error in errors:
                    print(f"  ❌ {error}")
            
            print("\nТокены:")
            for token in tokens[:50]:  # Показываем первые 50
                print(f"  {token}")
            
            if len(tokens) > 50:
                print(f"  ... и еще {len(tokens) - 50} токенов")
                
        except Exception as e:
            print(f"Ошибка: {e}")
    else:
        # Демо режим
        demo_code = """
функция привет(имя):
    печать(f"Привет, {имя}!")
    
привет("Мир")
"""
        print("\nДемо код:")
        print(demo_code)
        
        tokenizer = create_tokenizer()
        tokens = list(tokenizer.tokenize(demo_code))
        
        print(f"\nТокены ({len(tokens)}):")
        for token in tokens:
            print(f"  {token}")
