$ найти /workspace -type f \( -name "*.py" -o -name "*.txt" -o -name "*.toml" -o -name "*.md" -o -name"*.json" -o -name"*.yaml" -o -name "*.yml" \) | head -50 
найдите /workspace -введите f \( -name "*.py" -o -name "*.txt" -o -name "*.toml" -o -name "*.md" -o -name"*.json" -o -name"*.yaml" -o -name "*.yml" \) | head -50
/workspace/libraries.py
/workspace/libs/std_io.py
/workspace/libs/std_math.py
/workspace/libs/std_str.py
/workspace/libs/std_collections.py
/workspace/ruspython.py
/workspace/requirements.txt
/workspace/src/__init__.py
/workspace/src/cli/main.py
/workspace/src/core/lexer.py
/workspace/src/core/parser.py
/workspace/src/runtime/interpreter.py
/workspace/src/backend/translator.py
/workspace/ruspython.egg-info/dependency_links.txt
/workspace/ruspython.egg-info/top_level.txt
/workspace/ruspython.egg-info/requires.txt
/workspace/ruspython.egg-info/SOURCES.txt
/workspace/ruspython.egg-info/entry_points.txt
/workspace/README.md
/workspace/pyproject.toml
$ cat /workspace/ruspython.py
cat /workspace/ruspython.py
#!/usr/bin/env python3
# Русский Питон — точка входа в приложение
from src.cli.main import main
if __name__ == "__main__":
 main()
$ cat /workspace/src/cli/main.py
cat /workspace/src/cli/main.py
# Русский Питон — интерфейс командной строки
# Версия 1.1.0 — полноценное исполнение с обновлением
from __future__ import annotations
import sys
import os
import subprocess
import argparse
from pathlib import Path
sys.path.insert(0, '/workspace')
from src.core.lexer import RussianLexer, Token, TokenType
from src.core.parser import Module, ASTPrinter, RussianParser
from src.backend.translator import PythonTranslator
from src.runtime.interpreter import RussianInterpreter, run_file
def tokenize_file(filepath: str) -> list:
 """Токенизация файла."""
 with open(filepath, 'r', encoding='utf-8') as f:
 source = f.read()
 lexer = RussianLexer(source, filepath)
 tokens = lexer.tokenize()
 return tokens
def parse_file(filepath: str) -> Module:
 """Парсинг файла в AST."""
 # Пока заглушка — в будущем будет полноценный парсер
 from src.core.parser import FunctionDef, Parameter, ExpressionStatement, Call, Identifier, String, Return, Boolean
 with open(filepath, 'r', encoding='utf-8') as f:
 source = f.read()
 lexer = RussianLexer(source, filepath)
 tokens = lexer.tokenize()
 print(f"Файл прочитан: {filepath}")
 print(f"Токенов: {len(tokens)}")
 для токена в токенах[:20]:
 print(f" {токен}")
 если len(токены) > 20:
 print(f" ... и еще {len(tokens) - 20} токенов")
 не возвращает значение None 
def run_file(путь к файлу: str):
 """Выполнение файла с полным циклом: токенизация -> синтаксический анализ -> выполнение."""
 print(f"Выполнение файла: {filepath}")
 interpreter = run_file_impl(filepath)
 print("\n=== Выполнение завершено ===")
def run_file_impl(filepath: str):
 """Внутренняя функция выполнения файла."""
 with open(filepath, 'r', encoding='utf-8') as f:
 source = f.read()
 lexer = RussianLexer(source, filepath)
 tokens = lexer.tokenize()
 parser = RussianParser(tokens)
 ast = parser.parse()
 interpreter = RussianInterpreter()
 interpreter.interpret(ast)
 return interpreter
def update_version():
 """Обновление до новой версии через pip."""
 print("Обновление Русского Питона до последней версии...")
 print("Команда: pip install --upgrade ruspython\n")
 try:
 result = subprocess.run(
 [sys.executable, "-m", "pip", "install", "--upgrade", "ruspython"],
 capture_output=True,
 text=True
 )
 if result.returncode == 0:
 print("✓ Обновление успешно выполнено!")
 print(result.stdout)
 else:
 print("✗ Ошибка при обновлении:")
 print(result.stderr)
 except Exception as e:
 print(f"Ошибка: {e}")
def repl():
 """Режим REPL с полным выполнением."""
 print("Русский Питон v1.1.0 — режим REPL (полное выполнение)")
 print("Для выхода введите 'выход' \n")
 interpreter = RussianInterpreter()
 while True:
 try:
 source = input(">>> ")
 if source.strip() in ['выход', 'exit', 'quit']:
 break
 if not source.strip():
 continue
 lexer = RussianLexer(source, "<repl>")
 tokens = lexer.tokenize()
 parser = RussianParser(tokens)
 ast = parser.parse()
 result = interpreter.interpret(ast)
 if result is not None:
 print(result)
 except KeyboardInterrupt:
 print("\n")
 continue
 except Exception as e:
 print(f"Ошибка: {e}")
def main():
 parser = argparse.ArgumentParser(
 description="Русский Питон — язык программирования с русским синтаксисом",
 formatter_class=argparse.RawDescriptionHelpFormatter,
 epilog="""
Примеры использования:
 ruspython examples/hello.ру Выполнить файл
 ruspython --tokens hello.ру Показать токены
 ruspython --ast hello.ру Показать дерево AST
 ruspython --repl Запустить режим REPL
 ruspython --update Обновить до новой версии
 """
 )
 parser.add_argument('file', nargs='?', help='Файл для выполнения')
 parser.add_argument('--tokens', '-t', action='store_true', help='Показать токены')
 parser.add_argument('--ast', '-a', action='store_true', help='Показать дерево AST')
 parser.add_argument('--translate', action='store_true', help='Транслировать в Python')
 parser.add_argument('--repl', '-r', action='store_true', help='Запустить режим REPL')
 parser.add_argument('--update', '-u', action='store_true', help='Обновить до новой версии')
 parser.add_argument('--version', '-v', action='version', version='Русский Питон 1.1.0')
 args = parser.parse_args()
 if args.update:
 update_version()
 return
 if args.repl:
 repl()
 return
 if not args.file:
 parser.print_help()
 return
 filepath = args.file
 if not os.path.exists(filepath):
 print(f"Ошибка: файл не найден: {filepath}")
 sys.exit(1)
 if args.tokens:
 tokens = tokenize_file(filepath)
 print(f"\n=== Токены ({len(tokens)}) ===")
 for token in tokens:
 print(token)
 elif args.ast:
 # Показываем AST с полным парсингом
 with open(filepath, 'r', encoding='utf-8') as f:
 source = f.read()
 lexer = RussianLexer(source, filepath)
 tokens = lexer.tokenize()
 parser_obj = RussianParser(tokens)
 ast = parser_obj.parse()
 print(f"\n=== Дерево AST ===")
 print(ast.print_tree())
 elif args.translate:
 print("Трансляция в Python (в разработке)...")
 else:
 run_file(filepath)
if __name__ == "__main__":
 main()
$ cat /workspace/src/core/lexer.py
# Русский Питон — лексический анализатор (лексер)
# Версия 1.0.0 — профессиональная реализация
"""
Лексический анализатор для русского языка программирования. 
Поддерживает:
- более 50 типов лексем
- русские ключевые слова для всех конструкций Python
- числа (целые, дробные, комплексные, с разделителями)
- Строки (одинарные, двойные, тройные, необработанные, f-строки)
- Операторы и разделители
- Отступы как значимые символы
- Однострочные и многострочные комментарии
- Идентификаторы Unicode на русском языке
"""
import re
from enum import Enum, auto
from dataclasses import dataclass, field
from typing import List, Optional, Dict, Set, Tuple, Any
from collections import defaultdict
class TokenType(Enum):
 """Типы токенов для русского языка программирования."""
 # Ключевые слова управления потоком
 ЕСЛИ = auto() # если
 ИНАЧЕ = auto() # иначе
 ИНАЧЕ_ЕСЛИ = auto() # иначе если
 ПОКА = auto() # пока
 ДЛЯ = auto() # для
 В = auto() # в
 # Объявления
 ФУНКЦИЯ = auto() # функция
 КЛАСС = auto() # класс
 ВОЗВРАТ = auto() # возврат
 ИМПОРТ = auto() # импорт
 ИЗ = auto() # из
 КАК = auto() # как
 # Логические операторы
 И = auto() # и
 ИЛИ = auto() # или
 НЕ = auto() # не
 # Специальные значения
 ИСТИНА = auto() # истина
 ЛОЖЬ = auto() # ложь
 НИЧТО = auto() # ничто
 # Асинхронность
 АСИНХРОННО = auto() # асинхронно
 ЖДАТЬ = auto() # ждать
 # Контекстные менеджеры
 С = auto() # с
 # Обработка исключений
 ПОПРОБУЙ = auto() # попробуй
 КРОМЕ = auto() # кроме
 НАКОНЕЦ = auto() # наконец
 ВЫБРАТЬ = auto() # выбросить
 # Циклы
 ПРОДОЛЖИТЬ = auto() # продолжить
 ПРЕКРАТИТЬ = auto() # прервать
 # Глобальные и нелокальные переменные
 ГЛОБАЛЬНО = auto() # глобально
 НЕЛОКАЛЬНО = auto() # нелокально
 # Параллелизм
 ПАРАЛЛЕЛЬНО = auto() # параллельно
 # Макросы
 МАКРОС = auto() # макрос
 # Литералы
 ЧИСЛО = auto() # числовое значение
 СТРОКА = auto() # строковое значение
 ИДЕНТИФИКАТОР = auto() # имя переменной/функции
 # Операторы
 ПЛЮС = auto() # +
 МИНУС = auto() # -
 ЗВЕЗДОЧКА = auto() # *
 СЛЕШ = auto() # /
 ДВОЕТОЧИЕ = auto() # //
 ПРОЦЕНТ = auto() # %
 СТЕПЕНЬ = auto() # **
 РАВНО = auto() # =
 ПЛЮС_РАВНО = auto() # +=
 МИНУС_РАВНО = auto() # -=
 УМНОЖИТЬ_РАВНО = auto() # *=
 РАЗДЕЛИТЬ_РАВНО = auto()# /=
 ЦЕЛОЕ_РАВНО = auto() # //=
 МОДУЛЬ_РАВНО = auto() # %=
 СТЕПЕНЬ_РАВНО = auto() # **=
 РАВНО_РАВНО = auto() # ==
 НЕ_РАВНО = auto() # !=
 МЕНЬШЕ = auto() # <
 БОЛЬШЕ = auto() # >
 МЕНЬШЕ_РАВНО = auto() # <=
 БОЛЬШЕ_РАВНО = auto() # >=
 # Логические операторы (символьные)
 ЛОГ_И = auto() # &
 ЛОГ_ИЛИ = auto() # |
 ЛОГ_НЕ = auto() # ~
 СДВИГ_ВЛЕВО = auto() # <<
 СДВИГ_ВПРАВО = auto() # >>
 # Разделители
 ЛЕВАЯ_СКОБКА = auto() # (
 ПРАВАЯ_СКОБКА = auto() # )
 ЛЕВАЯ_КВАДРАТНАЯ = auto() # [
 ПРАВАЯ_КВАДРАТНАЯ = auto() # ]
 ЛЕВАЯ_ФИГУРНАЯ = auto() # {
 ПРАВАЯ_ФИГУРНАЯ = auto() # }
 ЗАПЯТАЯ = auto() # ,
 ТОЧКА = auto() # .
 ДВОЕТОЧИЕ = auto() # :
 ТОЧКА_С_ЗАПЯТОЙ = auto() # ;
 СТРЕЛКА = auto() # ->
 СОБЫТИЕ = auto() # @
 # Специальные
 ОТСТУП = auto() # Индент
 ДЕДЕНТ = auto() # Дедент
 НОВАЯ_СТРОКА = auto() # Новая строка
 КОММЕНТАРИЙ = auto() # Комментарий
 КОНЕЦ_ФАЙЛА = auto() # EOF
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
 """Отформатированное сообщение об ошибке."""
 msg = f"Лексическая ошибка в строке {self.line}, позиция {self.column}: {self.message}"
 if self.source:
 lines = self.source.split('\n')
 if 0 <= self.line - 1 < len(lines):
 msg += f"\n {lines[self.line - 1]}\n {' ' * (self.column - 1)}^"
 return msg
class RussianLexer:
 """
 Профессиональный лексический анализатор для русского языка программирования. 
 Особенности:
 - Поддержка идентификаторов в кодировке Unicode
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
 '!': TokenType.НЕ_РАВНО, # Будет проверено на !=
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
 """Проверка и использование ожидаемого символа."""
 if self._peek() != expected:
 return False
 self._advance()
 return True
 def _skip_whitespace(self):
 """Пропуск пробельных символов (кроме новой строки)."""
 while self._peek() в ' \t\r':
 self._advance()
 def _skip_comment(self) -> Optional[Token]:
 """Пропуск комментария."""
 if self._peek() == '#':
 start_col = self.column
 self._advance() # Пропускаем #
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
 number_str += self._advance() # точка
 while self._peek().isdigit() or self._peek() == '_':
 char = self._advance()
 if char != '_':
 number_str += char
 # Чтение экспоненты
 if self._peek() in 'eE' and (self._peek(1).isdigit() or self._peek(1) in '+-'):
 has_exponent = True
 number_str += self._advance() # e/E
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
 # Первый символ: буква или подчеркивание (включая символы Юникода)
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
 indent_count += 8 # Табуляция = 8 пробелов
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
 Возвращает:
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
 self._advance() # новая строка
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
 '**=': TokenType.СТЕПЕНЬ_РАВНА,
 '<<': TokenType.СДВИГ_ВЛЕВО,
 '>>': TokenType.СДВИГ_ВПРАВО,
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
 пока len(self.indent_stack) > 1:
 self.indent_stack.pop()
 self.tokens.append(Token(
 Тип токена.ДЕДЕНТ, 
 ",
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
 вернуть истина
 иначе:
 вернуть ложь
для i в диапазоне(10):
 если i % 2 == 0:
 печать(i)
"""
 lexer = RussianLexer(code)
 tokens = lexer.tokenize()
 print("=== Токены ===")
 for token in tokens:
 if token.type != TokenType.КОНЕЦ_ФАЙЛА:
 print(f" {token}")
 return tokens
if __name__ == "__main__":
 demo_tokenize()
$ cat /workspace/src/core/parser.py
cat /workspace/src/core/parser.py
# Русский Питон — абстрактное синтаксическое дерево (AST) и парсер
# Версия 1.1.0 — полноценный парсер и исполнитель
from __future__ import annotations
from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from typing import List, Optional, Dict, Any, Union, Tuple
from enum import Enum, auto
import sys
sys.path.insert(0, '/workspace')
from src.core.lexer import Token, TokenType
class NodeType(Enum):
 МОДУЛЬ = auto()
 ВЫРАЖЕНИЕ = auto()
 ФУНКЦИЯ = auto()
 КЛАСС = auto()
 ПАРАМЕТР = auto()
 ИМПОРТ = auto()
 ИМПОРТ_ИЗ = auto()
 ЕСЛИ = auto()
 ПОКА = auto()
 ДЛЯ = auto()
 ПОПРОБУЙ = auto()
 КРОМЕ = auto()
 НАКОНЕЦ = auto()
 ВЫБРАТЬ = auto()
 ВОЗВРАТ = auto()
 ПРЕКРАТИТЬ = auto()
 ПРОДОЛЖИТЬ = auto()
 ПРИСВОЕНИЕ = auto()
 ДИНАРНАЯ = auto()
 УНАРНАЯ = auto()
 ВЫЗОВ = auto()
 ДОСТУП = auto()
 ИНДЕКС = auto()
 ЧИСЛО = auto()
 СТРОКА = auto()
 ИСТИНА = auto()
 ЛОЖЬ = auto()
 НИЧТО = auto()
 СПИСОК = auto()
 КОРТЕЖ = auto()
 СЛОВАРЬ = auto()
 МНОЖЕСТВО = auto()
 ОЖИДАТЬ = auto()
 ИДЕНТИФИКАТОР = auto()
@dataclass
class ASTNode(ABC):
 line: int = 0
 column: int = 0
 @abstractmethod
 def node_type(self) -> NodeType:
 pass
 @abstractmethod
 def to_dict(self) -> dict:
 pass
 def print_tree(self, indent: int = 0) -> str:
 prefix = " " * indent
 result = f"{prefix}{self.node_type().name}"
 children = []
 for attr_name, attr_value in self.__dict__.items():
 if attr_name in ('line', 'column'):
 continue
 if isinstance(attr_value, ASTNode):
 children.append((attr_name, attr_value))
 elif isinstance(attr_value, list):
 for i, item in enumerate(attr_value):
 if isinstance(item, ASTNode):
 children.append((f"{attr_name}[{i}]", item))
 if children:
 result += ":\n"
 for name, child in children:
 result += f"{prefix} {name}: "
 result += child.print_tree(indent + 2)
 else:
 result += f" (line={self.line})\n"
 вернуть результат
@dataclass
class Module(ASTNode):
 body: List[ASTNode] = field(default_factory=list)
 docstring: Optional[str] = None
 def node_type(self) -> NodeType:
 return NodeType.МОДУЛЬ
 def to_dict(self) -> dict:
 return {'type': 'Module', 'body': [n.to_dict() for n in self.body], 'line': self.line}
@dataclass
class FunctionDef(ASTNode):
 name: str = ""
 args: List[ASTNode] = field(default_factory=list)
 body: List[ASTNode] = field(default_factory=list)
 returns: Optional[ASTNode] = None
 def node_type(self) -> NodeType:
 return NodeType.ФУНКЦИЯ
 def to_dict(self) -> dict:
 return {'type': 'FunctionDef', 'name': self.name, 'args': [a.to_dict() for a in self.args],
 'body': [b.to_dict() for b in self.body], 'line': self.line}
@dataclass
class Parameter(ASTNode):
 name: str = ""
 annotation: Optional[ASTNode] = None
 default: Optional[ASTNode] = None
 def node_type(self) -> NodeType:
 return NodeType.ПАРАМЕТР
 def to_dict(self) -> dict:
 return {'type': 'Parameter', 'name': self.name, 'line': self.line}
@dataclass
class If(ASTNode):
 test: ASTNode = field(default_factory=lambda: Boolean (True))
 body: List[ASTNode] = field(default_factory=list)
 orelse: List[ASTNode] = field(default_factory=list)
 def node_type(self) -> NodeType:
 return NodeType.ЕСЛИ
 def to_dict(self) -> dict:
 return {'type': 'If', 'test': self.test.to_dict(), 'body': [b.to_dict() for b in self.body], 'line': self.line}
@dataclass
class For(ASTNode):
 target: ASTNode = field(default_factory=lambda: Identifier("i"))
 iter: ASTNode = field(default_factory=lambda: Call(func=Identifier("range"), args=[Number(10)]))
 body: List[ASTNode] = field(default_factory=list)
 def node_type(self) -> NodeType:
 return NodeType.ДЛЯ
 def to_dict(self) -> dict:
 return {'type': 'For', 'target': self.target.to_dict(), 'iter': self.iter.to_dict(),
 'body': [b.to_dict() for b in self.body], 'line': self.line}
@dataclass
class While(ASTNode):
 test: ASTNode = field(default_factory=lambda: Boolean(True))
 body: List[ASTNode] = field(default_factory=list)
 def node_type(self) -> NodeType:
 return NodeType.ПОКА
 def to_dict(self) -> dict:
 return {'type': 'While', 'test': self.test.to_dict(), 'body': [b.to_dict() for b in self.body], 'line': self.line}
@dataclass
class Return(ASTNode):
 value: Optional[ASTNode] = None
 def node_type(self) -> NodeType:
 return NodeType.ВОЗВРАТ
 def to_dict(self) -> dict:
 return {'type': 'Return', 'value': self.value.to_dict() if self.value else None, 'line': self.line}
@dataclass
class Assign(ASTNode):
 targets: List[ASTNode] = field(default_factory=list)
 value: ASTNode = field(default_factory=lambda: Number(0))
 def node_type(self) -> NodeType:
 return NodeType.ПРИСВАИВАНИЕ
 def to_dict(self) -> dict:
 return {'type': 'Assign', 'targets': [t.to_dict() for t in self.targets],
 'value': self.value.to_dict(), 'line': self.line}
@dataclass
class BinaryOp(ASTNode):
 left: ASTNode = field(default_factory=lambda: Number(0))
 op: str = "+"
 right: ASTNode = field(default_factory=lambda: Number(0))
 def node_type(self) -> NodeType:
 return NodeType.БИНАРНАЯ
 def to_dict(self) -> dict:
 return {'type': 'BinaryOp', 'left': self.left.to_dict(), 'op': self.op,
 'right': self.right.to_dict(), 'line': self.line}
@dataclass
class Call(ASTNode):
 func: ASTNode = field(default_factory=lambda: Identifier("func"))
 args: List[ASTNode] = field(default_factory=list)
 def node_type(self) -> NodeType:
 return NodeType.ВЫЗОВ
 def to_dict(self) -> dict:
 return {'type': 'Call', 'func': self.func.to_dict(), 'args': [a.to_dict() for a in self.args], 'line': self.line}
@dataclass
class Identifier(ASTNode):
 name: str = ""
 def node_type(self) -> NodeType:
 return NodeType.ИДЕНТИФИКАТОР
 def to_dict(self) -> dict:
 return {'type': 'Identifier', 'name': self.name, 'line': self.line}
@dataclass
class Number(ASTNode):
 value: Union[int, float] = 0
 raw: str = "0"
 def node_type(self) -> NodeType:
 return NodeType.ЧИСЛО
 def to_dict(self) -> dict:
 return {'type': 'Number', 'value': self.value, 'line': self.line}
@dataclass
class String(ASTNode):
 value: str = ""
 def node_type(self) -> NodeType:
 return NodeType.СТРОКА
 def to_dict(self) -> dict:
 return {'type': 'String', 'value': self.value, 'line': self.line}
@dataclass
class Boolean(ASTNode):
 value: bool = True
 def node_type(self) -> NodeType:
 return NodeType.ИСТИНА if self.value else NodeType.ЛОЖЬ
 def to_dict(self) -> dict:
 return {'type': 'Boolean', 'value': self.value, 'line': self.line}
@dataclass
class ExpressionStatement(ASTNode):
 value: ASTNode = field(default_factory=lambda: Number(0))
 def node_type(self) -> NodeType:
 return NodeType.ВЫРАЖЕНИЕ
 def to_dict(self) -> dict:
 return {'type': 'ExpressionStatement', 'value': self.value.to_dict(), 'line': self.line}
class ASTVisitor(ABC):
 @abstractmethod
 def generic_visit(self, node: ASTNode):
 pass
class ASTPrinter(ASTVisitor):
 def __init__(self):
 self.indent = 0
 def generic_visit(self, node: ASTNode) -> str:
 prefix = " " * self.indent
 result = f"{prefix}{node.node_type().name}"
 if isinstance(node, Identifier):
 result += f": {node.name}"
 elif isinstance(node, Number):
 result += f": {node.value}"
 elif isinstance(node, String):
 result += f": '{node.value}'"
 result += "\n"
 for attr_name, attr_value in node.__dict__.items():
 if attr_name in ('line', 'column'):
 continue
 if isinstance(attr_value, ASTNode):
 self.indent += 1
 result += attr_value.visit(self) if hasattr(attr_value, 'visit') else str(attr_value)
 self.indent -= 1
 elif isinstance(attr_value, list):
 for item in attr_value:
 if isinstance(item, ASTNode):
 self.indent += 1
 result += item.visit(self) if hasattr(item, 'visit') else str(item)
 self.indent -= 1
 return result
def demo_ast():
 func = FunctionDef(
 name="привет",
 args=[Parameter(name="имя")],
 body=[
 ExpressionStatement(value=Call(func=Identifier(name="печать"), args=[String(value="Привет!")])),
 Return(value=Boolean(True))
 ],
 line=1
 )
 module = Module(body=[func], line=0)
 print("=== Дерево AST ===")
 print(module.print_tree())
 return module
class ParserError(Exception):
 """Ошибка парсера."""
 def __init__(self, message: str, token: Token = None):
 self.message = message
 self.token = token
 if token:
 super().__init__(f"{message} (строка {token.line}, позиция {token.column})")
 else:
 super().__init__(message)
class RussianParser:
 """
 Парсер для преобразования токенов в AST.
 Реализует рекурсивный спуск.
 """
 def __init__(self, tokens: List[Token]):
 self.tokens = [t for t in tokens if t.type != TokenType.КОММЕНТАРИЙ]
 self.pos = 0
 self.indent_stack = [0]
 def _current(self) -> Optional[Token]:
 """Текущий токен."""
 if self.pos < len(self.tokens):
 return self.tokens[self.pos]
 return None
 def _peek(self, offset: int = 0) -> Optional[Token]:
 """Просмотр токена со смещением."""
 pos = self.pos + offset
 if pos < len(self.tokens):
 return self.tokens[pos]
 return None
 def _advance(self) -> Optional[Token]:
 """Переход к следующему токену."""
 token = self._current()
 if token:
 self.pos += 1
 return token
 def _expect(self, token_type: TokenType, message: str = None) -> Token:
 """Ожидание токена определенного типа."""
 token = self._current()
 if not token or token.type != token_type:
 msg = message or f"Ожидался токен {token_type.name}"
 raise ParserError(msg, token)
 return self._advance()
 def _match(self, *types: TokenType) -> bool:
 """Проверка текущего токена на соответствие типам."""
 token = self._current()
 return token and token.type in types
 def parse(self) -> Module:
 """Парсинг модуля."""
 module = Module(line=self._current().line if self._current() else 0)
 while self._current():
 stmt = self._parse_statement()
 if stmt:
 module.body.append(stmt)
 return module
 def _parse_statement(self) -> Optional[ASTNode]:
 """Парсинг утверждения."""
 token = self._current()
 if not token:
 return None
 if token.type == TokenType.ФУНКЦИЯ:
 return self._parse_function_def()
 elif token.type == TokenType.ЕСЛИ:
 return self._parse_if()
 elif token.type == TokenType.ПОКА:
 return self._parse_while()
 elif token.type == TokenType.ДЛЯ:
 return self._parse_for()
 elif token.type == TokenType.ВОЗВРАТ:
 return self._parse_return()
 elif token.type == TokenType.ИМПОРТ:
 return self._parse_import()
 elif token.type == TokenType.РАВНО или token.type == TokenType.ИДЕНТИФИКАТОР:
 return self._parse_assignment_or_expression()
 else:
 return self._parse_expression_statement()
 def _parse_function_def(self) -> FunctionDef:
 """Парсинг определения функции."""
 start = self._expect(TokenType.ФУНКЦИЯ)
 name_token = self._expect(TokenType.ИДЕНТИФИКАТОР, "Ожидалось имя функции")
 self._expect(TokenType.ЛЕВАЯ_СКОБКА, "Ожидалась '(' после имени функции")
 args = []
 while not self._match(TokenType.ПРАВАЯ_СКОБКА):
 arg_name = self._expect(TokenType.ИДЕНТИФИКАТОР)
 param = Parameter(name=arg_name.value, line=arg_name.line)
 args.append(param)
 if not self._match(TokenType.ЗАПЯТАЯ):
 break
 self._advance()
 self._expect(TokenType.ПРАВАЯ_СКОБКА)
 self._expect(TokenType.ДВОЕТОЧИЕ)
 body = self._parse_block()
 return FunctionDef(
 name=name_token.value,
 args=args,
 body=body,
 line=start.line
 )
 def _parse_if(self) -> If:
 """Парсинг условия if."""
 start = self._expect(TokenType.ЕСЛИ)
 test = self._parse_expression()
 self._expect(TokenType.ДВОЕТОЧИЕ)
 body = self._parse_block()
 orelse = []
 if self._match(TokenType.ИНАЧЕ):
 self._advance()
 self._expect(TokenType.ДВОЕТОЧИЕ)
 orelse = self._parse_block()
 return If(test=test, body=body, orelse=orelse, line=start.line)
 def _parse_while(self) -> While:
 """Парсинг цикла пока."""
 start = self._expect(TokenType.ПОКА)
 test = self._parse_expression()
 self._expect(TokenType.ДВОЕТОЧИЕ)
 body = self._parse_block()
 return While(test=test, body=body, line=start.line)
 def _parse_for(self) -> For:
 """Парсинг цикла for."""
 start = self._expect(TokenType.ДЛЯ)
 target = self._parse_expression()
 self._expect(TokenType.В)
 iter_expr = self._parse_expression()
 self._expect(TokenType.ДВОЕТОЧИЕ)
 body = self._parse_block()
 return For(target=target, iter=iter_expr, body=body, line=start.line)
 def _parse_return(self) -> Return:
 """Парсинг возврата."""
 start = self._expect(TokenType.ВОЗВРАТ)
 if self._match(TokenType.НОВАЯ_СТРОКА) or not self._current():
 return Return(value=None, line=start.line)
 value = self._parse_expression()
 return Return(value=value, line=start.line)
 def _parse_import(self) -> ASTNode:
 """Парсинг импорта."""
 start = self._expect(TokenType.ИМПОРТ)
 # Упрощенная реализация
 return Module(body=[], line=start.line)
 def _parse_assignment_or_expression(self) -> ASTNode:
 """Парсинг присваивания или выражения."""
 expr = self._parse_expression()
 if self._match(TokenType.РАВНО):
 self._advance()
 value = self._parse_expression()
 return Assign(targets=[expr], value=value, line=expr.line)
 return ExpressionStatement(value=expr, line=expr.line)
 def _parse_expression_statement(self) -> ExpressionStatement:
 """Парсинг выражения как утверждения."""
 expr = self._parse_expression()
 return ExpressionStatement(value=expr, line=expr.line)
 def _parse_block(self) -> List[ASTNode]:
 """Парсинг блока кода."""
 statements = []
 while self._current() and not self._match(TokenType.ИНАЧЕ, TokenType.ВОЗВРАТ):
 stmt = self._parse_statement()
 if stmt:
 statements.append(stmt)
 else:
 break
 return statements
 def _parse_expression(self) -> ASTNode:
 """Парсинг выражения."""
 return self._parse_comparison()
 def _parse_comparison(self) -> ASTNode:
 """Парсинг сравнения."""
 left = self._parse_additive()
 while self._match(TokenType.РАВНО_РАВНО, TokenType.НЕ_РАВНО,
 TokenType.МЕНЬШЕ, TokenType.БОЛЬШЕ,
 TokenType.МЕНЬШЕ_РАВНО, TokenType.БОЛЬШЕ_РАВНО):
 op_token = self._advance()
 right = self._parse_additive()
 left = BinaryOp(left=left, op=op_token.value, right=right, line=op_token.line)
 return left
 def _parse_additive(self) -> ASTNode:
 """Парсинг аддитивных операций."""
 left = self._parse_multiplicative()
 while self._match(TokenType.ПЛЮС, TokenType.МИНУС):
 op_token = self._advance()
 right = self._parse_multiplicative()
 left = BinaryOp(left=left, op=op_token.value, right=right, line=op_token.line)
 return left
 def _parse_multiplicative(self) -> ASTNode:
 """Парсинг мультипликативных операций."""
 left = self._parse_primary()
 while self._match(TokenType.ЗВЕЗДОЧКА, TokenType.СЛЕШ, TokenType.ПРОЦЕНТ):
 op_token = self._advance()
 right = self._parse_primary()
 left = BinaryOp(left=left, op=op_token.value, right=right, line=op_token.line)
 return left
 def _parse_primary(self) -> ASTNode:
 """Парсинг первичных выражений."""
 token = self._current()
 # Пропуск новых строк
 while token and token.type == TokenType.НОВАЯ_СТРОКА:
 self._advance()
 token = self._current()
 if not token or token.type == TokenType.КОНЕЦ_ФАЙЛА:
 raise ParserError("Неожиданный конец выражения")
 if token.type == TokenType.ЧИСЛО:
 self._advance()
 value = float(token.value) if '.' in token.value else int(token.value)
 return Number(value=value, raw=token.value, line=token.line)
 elif token.type == TokenType.СТРОКА:
 self._advance()
 return String(value=token.value, line=token.line)
 elif token.type == TokenType.ИСТИНА:
 self._advance()
 return Boolean(value=True, line=token.line)
 elif token.type == TokenType.ЛОЖЬ:
 self._advance()
 return Boolean(value=False, line=token.line)
 elif token.type == TokenType.НИЧТО:
 self._advance()
 return Number(value=0, line=token.line)
 elif token.type == TokenType.ИДЕНТИФИКАТОР:
 self._advance()
 if self._match(TokenType.ЛЕВАЯ_СКОБКА):
 return self._parse_call(token)
 return Identifier(name=token.value, line=token.line)
 elif token.type == TokenType.ЛЕВАЯ_СКОБКА:
 self._advance()
 expr = self._parse_expression()
 self._expect(TokenType.ПРАВАЯ_СКОБКА)
 return expr
 raise ParserError(f"Неожиданный токен: {token.type}", token)
 def _parse_call(self, func_token: Token) -> Call:
 """Парсинг вызова функции."""
 self._expect(TokenType.ЛЕВАЯ_СКОБКА)
 args = []
 while not self._match(TokenType.ПРАВАЯ_СКОБКА):
 arg = self._parse_expression()
 args.append(arg)
 if not self._match(TokenType.ЗАПЯТАЯ):
 break
 self._advance()
 self._expect(TokenType.ПРАВАЯ_СКОБКА)
 return Call(
 func=Identifier(name=func_token.value, line=func_token.line),
 args=args,
 line=func_token.line
 )
def parse_tokens(tokens: List[Token]) -> Module:
 """Удобная функция для парсинга токенов."""
 parser = RussianParser(tokens)
 return parser.parse()
if __name__ == "__main__":
 from src.core.lexer import RussianLexer
 test_code = '''
функция привет(имя):
 печать(f\"Привет, {имя}!\")
 возврат истина
привет(\"Мир\")
'''
 лексер = RussianLexer(test_code)
 tokens = lexer.tokenize()
 print("=== Токены ===")
 for t in tokens[:20]:
 print(t)
 print("\n=== Парсинг ===")
 parser = RussianParser(tokens)
 ast = parser.parse()
 print(ast.print_tree())
$ cat /workspace/src/runtime/interpreter.py
cat /workspace/src/runtime/interpreter.py
# Русский Питон — интерпретатор
# Версия 1.1.0 — полноценное исполнение AST
from __future__ import annotations
import sys
sys.path.insert(0, '/workspace')
from src.core.parser import (
 ASTNode, Module, FunctionDef, Parameter, If, For, While,
 Return, Assign, BinaryOp, Call, Identifier, Number, String,
 Boolean, ExpressionStatement, NodeType
)
class InterpreterError(Exception):
 """Ошибка интерпретатора."""
 pass
class RussianInterpreter:
 """Интерпретатор для русского AST."""
 def __init__(self):
 self.variables = {}
 self.functions = {}
 self.output = []
 def interpret(self, node: ASTNode):
 """Выполнение узла."""
 method_name = f'_execute_{node.node_type().name}'
 method = getattr(self, method_name, self._generic_execute)
 return method(node)
 def _generic_execute(self, node: ASTNode):
 raise NotImplementedError(f"Нет реализации для {node.node_type()}")
 def _execute_МОДУЛЬ(self, node: Module):
 for stmt in node.body:
 self.interpret(stmt)
 def _execute_ФУНКЦИЯ(self, node: FunctionDef):
 self.functions[node.name] = node
 def _execute_ПРИСВАИВАНИЕ(self, node: Assign):
 value = self.interpret(node.value)
 for target in node.targets:
 if isinstance(target, Identifier):
 self.variables[target.name] = value
 def _execute_ВЫРАЖЕНИЕ(self, node: ExpressionStatement):
 return self.interpret(node.value)
 def _execute_ВОЗВРАТ(self, node: Return):
 value = self.interpret(node.value) if node.value else None
 return value
 def _execute_ИДЕНТИФИКАТОР(self, node: Identifier):
 if node.name in self.variables:
 return self.variables[node.name]
 if node.name in self.functions:
 return self.functions[node.name]
 raise NameError(f"Не определено: {node.name}")
 def _execute_ЧИСЛО(self, node: Number):
 return node.value
 def _execute_СТРОКА(self, node: String):
 return node.value
 def _execute_ИСТИНА(self, node: Boolean):
 return node.value
 def _execute_ЛОЖЬ(self, node: Boolean):
 return node.value
 def _execute_БИНАРНАЯ(self, node: BinaryOp):
 left = self.interpret(node.left)
 right = self.interpret(node.right)
 op_map = {
 '+': лямбда a, b: a + b, 
 '-': лямбда a, b: a - b, 
 '*': лямбда a, b: a * b, 
 '/': лямбда a, b: a / b, 
 '//': лямбда a, b: a // b, 
 '%': лямбда a, b: a % b, 
 '**': лямбда a, b: a ** b, 
 '==': лямбда a, b: a == b, 
 '!=': лямбда a, b: a != b, 
 '<': лямбда a, b: a < b, 
 '>': лямбда a, b: a > b, 
 '<=': лямбда a, b: a <= b, 
 '>=': лямбда a, b: a >= b, 
} 
 op_func = op_map.get(узел.op)
 if not op_func:
 raise ValueError(f"Неизвестный оператор: {node.op}")
 return op_func(left, right)
 def _execute_ВЫЗОВ(self, node: Call):
 func = self.interpret(node.func)
 args = [self.interpret(arg) for arg in node.args]
 if isinstance(func, str) and func == "печать":
 print(*args)
 self.output.append(' '.join(map(str, args)))
 return None
 if isinstance(func, str) and func == "диапазон":
 return list(range(*args))
 if isinstance(func, FunctionDef):
 old_vars = self.variables.copy()
 for param, arg in zip(func.args, args):
 self.variables[param.name] = arg
 result = None
 for stmt in func.body:
 result = self.interpret(stmt)
 if isinstance(stmt, Return):
 break
 self.variables = old_vars
 return result
 raise TypeError(f"Не является функцией: {func}")
 def _execute_ЕСЛИ(self, node: If):
 test = self.interpret(node.test)
 if test:
 for stmt in node.body:
 self.interpret(stmt)
 elif node.orelse:
 for stmt in node.orelse:
 self.interpret(stmt)
 def _execute_ДЛЯ(self, node: For):
 iterable = self.interpret(node.iter)
 for item in iterable:
 if isinstance(node.target, Identifier):
 self.variables[node.target.name] = item
 for stmt in node.body:
 self.interpret(stmt)
 def _execute_ПОКА(self, node: While):
 while self.interpret(node.test):
 for stmt in node.body:
 self.interpret(stmt)
def run_ast(module: Module) -> RussianInterpreter:
 """Запуск AST."""
 interpreter = RussianInterpreter()
 interpreter.interpret(module)
 return interpreter
def run_file(filepath: str) -> RussianInterpreter:
 """Выполнение файла с полным циклом: токенизация -> синтаксический анализ -> выполнение."""
 from src.core.lexer import RussianLexer
 from src.core.parser import RussianParser
 with open(filepath, 'r', encoding='utf-8') as f:
 source = f.read()
 lexer = RussianLexer(source, filepath)
 tokens = lexer.tokenize()
 parser = RussianParser(tokens)
 ast = parser.parse()
 interpreter = RussianInterpreter()
 interpreter.interpret(ast)
 return interpreter
def demo_interpret():
 from src.core.parser import Module, FunctionDef, Parameter, If, For, Return, Assign, BinaryOp, Call, Identifier, Number, String, Boolean, ExpressionStatement
 func = FunctionDef(
 name="привет",
 args=[Parameter(name="имя")],
 body=[
 ExpressionStatement(value=Call(func=Identifier(name="печать"), args=[String(value="Привет!")])),
 Return(value=Boolean(value=True))
 ],
 строка 1
 )
 модуль = Модуль(тело=[функция], строка 0)
 интерпретатор = РусскийИнтерпретатор()
 interpreter.interpret(module)
 print("=== Результат интерпретации ===")
 return interpreter
if __name__ == "__main__":
 # Тест полного цикла
 print("=== Тест полного цикла выполнения ===\n")
 test_code = '''
функция привет(имя):
 печать("Привет," + имя)
 возврат истина
для i в диапазоне(5):
 печать(i)
привет("Мир")
'''
 из src.core.lexer импортируем RussianLexer
 из src.core.parser импортируем RussianParser
 лексер = RussianLexer(test_code)
 токены = лексер.токенизировать()
 print(f"Найдено токенов: {len(tokens)}")
 parser = RussianParser(tokens)
 ast = parser.parse()
 print("\n=== AST-дерево ===")
 print(ast.print_tree())
 print("\n=== Исполнение ===")
 interpreter = RussianInterpreter()
 interpreter.interpret(ast)
 print("\n=== Готово ===")
$ cat /workspace/src/backend/translator.py && cat /workspace/src/__init__.py
cat /workspace/src/backend/translator.py && cat /workspace/src/__init__.py
# Русский Питон — транслятор в код Python
from __future__ import annotations
import ast
import sys
sys.path.insert(0, '/workspace')
from src.core.parser import (
 ASTNode, Module, FunctionDef, Parameter, If, For, While,
 Return, Assign, BinaryOp, Call, Identifier, Number, String,
 Boolean, ExpressionStatement, NodeType
)
class PythonTranslator:
 """Транслятор русского AST в Python AST."""
 def translate(self, node: ASTNode) -> str:
 """Трансляция в исходный код Python."""
 python_ast = self._convert(node)
 return ast.unparse(python_ast)
 def _convert(self, node: ASTNode):
 """Конвертация узла."""
 method_name = f'_convert_{node.node_type().name}'
 method = getattr(self, method_name, self._generic_convert)
 return method(node)
 def _generic_convert(self, node: ASTNode):
 raise NotImplementedError(f"Нет реализации для {node.node_type()}")
 def _convert_МОДУЛЬ(self, node: Module):
 body = [self._convert(child) for child in node.body]
 return ast.Module(body=body, type_ignores=[])
 def _convert_ФУНКЦИЯ(self, node: FunctionDef):
 args = ast.arguments(
 posonlyargs=[],
 args=[self._convert(arg) for arg in node.args],
 kwonlyargs=[],
 kw_defaults=[],
 defaults=[]
 )
 body = [self._convert(stmt) for stmt in node.body]
 returns = self._convert(node.returns) if node.returns else None
 return ast.FunctionDef(
 name=node.name,
 args=args,
 body=body,
 decorator_list=[],
 returns=returns,
 lineno=node.line
 )
 def _convert_ПАРАМЕТР(self, node: Parameter):
 return ast.arg(arg=node.name, lineno=node.line)
 def _convert_ЕСЛИ(self, node: If):
 test = self._convert(node.test)
 body = [self._convert(stmt) for stmt in node.body]
 orelse = [self._convert(stmt) for stmt in node.orelse]
 return ast.If(test=test, body=body, orelse=orelse, lineno=node.line)
 def _convert_ДЛЯ(self, node: For):
 target = self._convert(node.target)
 iter_node = self._convert(node.iter)
 body = [self._convert(stmt) for stmt in node.body]
 return ast.For(target=target, iter=iter_node, body=body, orelse=[], lineno=node.line)
 def _convert_ПОКА(self, node: While):
 test = self._convert(node.test)
 body = [self._convert(stmt) for stmt in node.body]
 return ast.While(test=test, body=body, orelse=[], lineno=node.line)
 def _convert_ВОЗВРАТ(self, node: Return):
 value = self._convert(node.value) if node.value else None
 return ast.Return(value=value, lineno=node.line)
 def _convert_ПРИСВАИВАНИЕ(self, node: Assign):
 targets = [self._convert(t) for t in node.targets]
 value = self._convert(node.value)
 return ast.Assign(targets=targets, value=value, lineno=node.line)
 def _convert_БИНАРНАЯ(self, node: BinaryOp):
 left = self._convert(node.left)
 right = self._convert(node.right)
 op_map = {
 '+': ast.Add, '-': ast.Sub, '*': ast.Mult, '/': ast.Div,
 '//': ast.FloorDiv, '%': ast.Mod, '**': ast.Pow,
 '==': ast.Eq, '!=': ast.NotEq, '<': ast.Lt, '>': ast.Gt,
 '<=': ast.LtE, '>=': ast.GtE
 }
 op_class = op_map.get(node.op, ast.Add)
 return ast.BinOp(left=left, op=op_class(), right=right, lineno=node.line)
 def _convert_ВЫЗОВ(self, node: Call):
 func = self._convert(node.func)
 args = [self._convert(arg) for arg in node.args]
 return ast.Call(func=func, args=args, keywords=[], lineno=node.line)
 def _convert_ИДЕНТИФИКАТОР(self, node: Identifier):
 return ast.Name(id=node.name, ctx=ast.Load(), lineno=node.line)
 def _convert_ЧИСЛО(self, node: Number):
 return ast.Constant(value=node.value, lineno=node.line)
 def _convert_СТРОКА(self, node: String):
 return ast.Constant(value=node.value, lineno=node.line)
 def _convert_ИСТИНА(self, node: Boolean):
 return ast.Constant(value=node.value, lineno=node.line)
 def _convert_ЛОЖЬ(self, node: Boolean):
 return ast.Constant(value=node.value, lineno=node.line)
 def _convert_ВЫРАЖЕНИЕ(self, node: ExpressionStatement):
 return ast.Expr(value=self._convert(node.value), lineno=node.line)
def demo_translate():
 func = FunctionDef(
 name="привет",
 args=[Parameter(name="имя")],
 body=[
 ExpressionStatement(value=Call(func=Identifier(name="print"), args=[String(value="Привет!")])),
 Return(value=Boolean(value=True))
 ],
 строка=1
 )
 модуль = Модуль(тело=[функция], строка=0)
 translator = PythonTranslator()
 python_code = translator.translate(module)
 print("=== Код Python ===")
 print(python_code)
 return python_code
if __name__ == "__main__":
 demo_translate()
# Русский Питон — промышленный компилятор с русским синтаксисом
# Версия 1.0.0 — полная совместимость с Python, расширенные возможности
"""
Русский Питон v1.0.0 — промышленная версия языка программирования
Особенности версии 1.0.0:
- Полный русский синтаксис для всех конструкций Python
- Совместимость с экосистемой Python (импорт модулей .py)
- Улучшенная система типов с поддержкой русских аннотаций
- Встроенный оптимизатор байт-кода
- Параллельное выполнение с помощью конструкции "параллельно"
- Асинхронные конструкции на русском языке
- Встроенная система профилирования и отладки
- Интеграция с Jupyter Notebook через русские магические команды
- Поддержка макросов и метапрограммирования
- Расширенная обработка ошибок с русскими сообщениями
- Автодополнение в REPL с учетом морфологии
- Лингвистический анализ кода с помощью pymorphy2
"""
__version__ = "1.0.0"
__author__ = "Команда Русский Питон"
__license__ = "MIT"
from .core.lexer import RussianLexer, Token, TokenType
from .core.parser import ASTNode
# from .semantic.analyzer import SemanticAnalyzer
# from .backend.translator import CodeGenerator
# from .runtime.interpreter import RussianInterpreter
# from .cli.main import cli
__all__ = [
 'RussianLexer',
 'Token',
 'TokenType',
 'ASTNode',
 '__version__'
]
$ cat /workspace/libs/std_io.py && echo "---" && cat /workspace/libs/std_math.py && echo "---" && cat /workspace/libs/std_str.py && echo "---" && cat /workspace/libs/std_collections.py
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
ЦВЕТА = {
 'сброс': '\033[0m', 
 'жирный': '\033[1m', 
 'тусклый': '\033[2m', 
 'курсив': '\033[3 м', 
 'подчеркнуть': '\033[4 м', 
 'мигать': '\033[5 м', 
 "обратный": "\033[7 м", 
 "скрытый": "\033[8 м", 
 "черный": "\033[30 м", 
 'красный': '\033[31 м', 
 'зеленый': '\033[32 м', 
 'желтый': '\033[33 м', 
 'синий': '\033[34m', 
 'пурпурный': '\033[35m', 
 'голубой': '\033[36m', 
 'белый': '\033[37 м', 
 'bg_black': '\033[40 м', 
 'bg_red': '\033[41 м', 
 'bg_green': '\033[42m', 
 'bg_yellow': '\033[43m', 
 'bg_blue': '\033[44m', 
 'bg_magenta': '\033[45m', 
 'bg_cyan': '\033[46m', 
 'bg_white': '\033[47m', 
 'bright_black': '\033[90 м', 
 'bright_red': '\033[91 м', 
 'bright_green': '\033[92 м',
 'ярко-жёлтый': '\033[93m',
 'ярко-синий': '\033[94m',
 'ярко-пурпурный': '\033[95m',
 'ярко-голубой': '\033[96m',
 'ярко-белый': '\033[97m',
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
 self.encoding = encoding или 'utf-8'
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
 sep: разделитель между объектами
 end: строка в конце вывода
 file: файловый объект для вывода
 flush: сброс буфера после печати
 color: цвет текста (название или код)
 bg_color: цвет фона
 style: стиль текста (полужирный, курсив, подчеркивание и т. д.).
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
 prompt: приглашение к вводу
 default: значение по умолчанию
 mask: маскировка ввода (для паролей)
 timeout: Тайм-аут ввода в секундах
 validator: Функция проверки ввода
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
 возвращаемое значение
def read_file(path: str, encoding: str = 'utf-8', binary: bool = False,
 chunk_size: int = 0) -> Union[str, bytes, Iterator[Union[str, bytes]]]:
 """
 Читать файл целиком, по частям или в виде байтов
 Аргументы:
 path: Путь к файлу
 encoding: Кодировка (если не используется двоичный режим)
 binary: чтение в байтах
 chunk_size: размер чанка (0 — чтение всего файла)
 Возвращает:
 Содержимое файла или итератор чанков
 """
 path = Path(path)
 if not path.exists():
 raise FileNotFoundError(f"Файл не найден: {path}")
 mode = 'rb', если двоичный, иначе 'r' 
 если chunk_size > 0:
 генератор определения ():
 с открытым (путь, режим, кодировка = Нет, если двоичная кодировка еще) как f: 
 пока True: 
 chunk = f.read(chunk_size)
 если не chunk: 
 разбить
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
 Скопировать файл
 Аргументы:
 src: исходный путь
 dst: целевой путь
 overwrite: перезаписать, если существует
 preserve_metadata: сохранить метаданные
 Возвращает:
 результат операции
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
 overwrite: Перезаписать, если существует
 Возвращает:
 Результат операции
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
 force: не вызывать ошибку, если файл не существует
 Возвращает:
 результат операции
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
 recursive: Рекурсивное удаление
 force: Не вызывать ошибку, если директория не существует
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
def list_directory(path: str, pattern: str = "*", recursive: bool = False,
 include_dirs: bool = True, include_files: bool = True) -> List[str]:
 """
 Список файлов и директорий
 Аргументы:
 path: Путь к директории
 pattern: Шаблон для фильтрации
 recursive: Рекурсивный обход
 include_dirs: Включить директории
 include_files: Включить файлы
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
 exist_ok: Не вызывать ошибку, если директория существует
 Возвращает:
 результат операции
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
 "изменено": stat.st_mtime, 
 "доступ": stat.st_atime, 
 "is_file": path.is_file(), 
 'is_dir': path.is_dir(), 
 'is_symlink': path.is_symlink(), 
 'расширение': path.суффикс, 
 'stem': путь.stem, 
 'parent': str (путь.parent), 
} 
def get_file_hash(путь: str, алгоритм: str = 'sha256', размер фрагмента: int = 8192) -> str:
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
 else if format == 'xz':
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
 вернуть результат
def encode_base64(data: Union[str, bytes], url_safe: bool = False) -> str:
 """
 Кодирование в Base64
 Аргументы:
 data: данные для кодирования
 url_safe: использовать алфавит URL-safe
 Возвращает:
 строку в кодировке Base64
 """
 if isinstance(data, str):
 data = data.encode('utf-8')
 if url_safe:
 return base64.urlsafe_b64encode(data).decode('ascii')
 else:
 return base64.b64encode(data).decode('ascii')
def decode_base64(data: str, url_safe: bool = False) -> bytes:
 """
 Декодирование Base64
 Аргументы:
 data: строка в кодировке Base64
 url_safe: использовать алфавит URL-safe
 Возвращает:
 декодированные байты
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
 lines: количество строк
 encoding: кодировка
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
 # Ищем позиции перевода строк с конца
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
 # Файл без переносов строк
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
 Наблюдение за изменениями в файле
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
 # Проверка шаблонов (упрощенная)
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
 prefix: префикс имени файла
 dir: директория для создания
 delete: удалить файл после использования (возвращает путь к несуществующему файлу)
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
 суффикс: суффикс имени директории
 префикс: префикс имени директории
 dir: родительская директория
 Возвращает:
 Путь к временной директории
 """
 return tempfile.mkdtemp(suffix=suffix, prefix=prefix, dir=dir)
def get_disk_usage(path: str = '/') -> Dict[str, int]:
 """
 Получить информацию об использовании диска
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
 Кортеж (столбцы, строки)
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
 частота: частота в Гц
 длительность: длительность в миллисекундах
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
 Создать строку с индикатором выполнения
 Аргументы:
 current: Текущее значение
 total: Общее значение
 width: Ширина индикатора в символах
 prefix: префикс строки
 suffix: суффикс строки
 Возвращает:
 строку индикатора выполнения
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
 filename: Путь к файлу журнала
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
 if LOG_LEVELS.get(уровень, 1) >= self.level:
 formatted = self._format(сообщение, уровень)
 # Консольный вывод
 color = None
 if level in ['ERROR', 'CRITICAL']:
 color = 'красный'
 уровень elif == "ПРЕДУПРЕЖДЕНИЕ": 
 color = "желтый"
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
__все__ = [ 
'ЦВЕТА', 
'LOG_LEVELS', 
'IOBuffer', 
'FileStream', 
'DirectoryWatcher', 
'печать', 
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
'звуковой сигнал', 
'progress_bar', 
'log_message', 
"Регистратор", 
]
---
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
# Математические константы с высокой...
 'encode_utf8', 'decode_utf8', 'encode_base64', 'decode_base64',
 'url_encode', 'url_decode', 'html_encode', 'html_decode',
 'json_encode', 'json_decode', 'hash_string', 'hmac_string',
 # Юникод
 'normalize_unicode', 'is_normalized', 'get_char_name', 'get_char_category',
 'combining', 'digit', 'numeric', 'decompose', 'compose',
 'remove_accents', 'transliterate_cyrillic',
 # Регулярные выражения
 'match', 'fullmatch', 'search', 'findall', 'finditer',
 'regex_replace', 'regex_split', 'escape_regex', 'compile_regex',
 # Шаблонизация
 'template_render', 'template_if', 'template_for',
 # Утилиты
 'расстояние Левенштейна', 'сходство', 'саундекс', 'генерировать_случайную_строку',
 'преобразование_в_слэш', 'извлечение_URL', 'извлечение_электронных_адресов', 'извлечение_чисел',
 'извлечение_хештегов', 'извлечение_упоминаний',
]
---
"""
Библиотека для работы с коллекциями (списками, словарями, множествами)
Предоставляет расширенные функции для работы с коллекциями, их фильтрации, преобразования и анализа. 
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
 """Создать список чисел в заданном диапазоне"""
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
 """Перевернуть список (на месте)"""
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
 """Перемешать список (на месте)"""
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
 возвращает lst[:n] 
определяем take_last(lst: Список, n: int) -> Список:
 """Взять последние n элементов"""
 верните lst[-n:], если n > 0 else [] 
удаление def(lst: List, n: int) -> Список:
 """Отбросить первые n элементов"""
 возвращает lst[n:] 
определяем drop_last(lst: Список, n: int) -> Список:
 """Отбросить последние n элементов"""
 верните lst[:-n], если n > 0, иначе lst[:] 
def head(lst: Список) -> Любой:
 """Получить первый элемент (head)"""
 return lst[0] if lst else None
def tail(lst: List) -> List:
 """Получить все элементы, кроме первого (tail)"""
 return lst[1:] if lst else []
def init(lst: List) -> List:
 """Получить все элементы, кроме последнего"""
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
 """Найти индекс элемента (-1, если элемент не найден)"""
 try:
 return lst.index(item, start)
 except ValueError:
 return -1
def rindex_of(lst: List, item: Any) -> int:
 """Найти последний индекс элемента (-1, если элемент не найден)"""
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
 """Удалить элементы, удовлетворяющие условию"""
 return [item for item in lst if not predicate(item)]
def filter_none(lst: List) -> List[Any]:
 """Удалить значения None"""
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
 возвращаемый результат 
определение flatten_deep(lst: Список, глубина: int = -1) -> Список[Любой]:
 """Рекурсивно сплющить список"""
 результат = [] 
 для элемента в lst: 
 если isinstance(элемент, список) и (глубина == -1 или глубина > 0):
 new_depth = глубина - 1, если глубина > 0, иначе -1 
 результат.расширить(flatten_depth(элемент, new_depth))
 ещё:
 результат.добавить (элемент)
 возвращаемый результат 
определяем zip_lists(* списки: Список) -> Список[Кортеж]:
 """Объединить несколько списков в кортежи"""
 список возвратов (zip (* списки))
def unzip(pairs: List[Tuple]) -> Tuple[List, ...]:
 """Разделить список кортежей на отдельные списки"""
 if not pairs:
 return ()
 return tuple(list(x) for x in zip(*pairs))
def chunk(lst: List, size: int) -> List[List[Any]]:
 """Разбить список на фрагменты фиксированного размера"""
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
 """Отсортировать с помощью функции сравнения"""
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
 для i в диапазоне (n): 
 для j в диапазоне (0, n - i - 1): 
 если результат [j] > результат[j + 1]: 
 результат[j], результат[j + 1] = результат[j + 1], результат[j]
 возвращает результат 
def quick_sort(lst: Список) -> Список:
 """Быстрая сортировка"""
 если len(lst) <= 1:
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
 """Мода (наиболее часто встречающиеся элементы)"""
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
 возвращаемая сумма(squared_diffs) / (len(lst) - 1) если len(lst) > 1, иначе 0 
def std_dev(lst: Список, заполнение: bool = False) -> float:
 """Стандартное отклонение"""
 импорт математических данных 
 возвращает math.sqrt(дисперсия (lst, совокупность))
def accumulate(lst: Список, функция: вызываемая[[Любая, Any], Any] = Нет) -> Список:
 """Накопление результатов применения функции"""
 if func is None:
 func = operator.add
 return list(itertools.accumulate(lst, func))
def reduce_list(lst: List, func: Callable[[Any, Any], Any], initial: Any = None) -> Any:
 """Свернуть список в одно значение"""
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
 """Свёртка справа"""
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
 return {v: k для k, v в d.items()}
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
 """Проверить, пуст ли словарь"""
 return len(d) == 0
def dict_default(d: Dict, key: Any, default: Any) -> Any:
 """Получить значение или установить default, если ключ отсутствует"""
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
 """Восстанавливает вложенный словарь из сплющенного"""
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
 """Создать список чисел в заданном диапазоне"""
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
 возвращает повтор (значение, n) 
цикл определения (lst: List, n: int) -> Список [Любой]:
 """Повторить список n раз"""
 return (lst * n), если n > 0 else [] 
def interleave(* списки: Список) -> Список[Любой]:
 """Перемешать элементы нескольких списков"""
 result = []
 for items in zip(*lists):
 result.extend(items)
 return result
def interleave_shortest(*lists: List) -> List[Any]:
 """Перемешать до конца кратчайшего списка"""
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
 вернуть результат
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
 """Сгенерировать список из n элементов с помощью функции"""
 return [func(i) for i in range(n)]
def iterate(func: Callable[[Any], Any], initial: Any, n: int) -> List[Any]:
 """Последовательно применить функцию n раз"""
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
 "среднее", "медиана", "режим", "отклонение", "std_dev", "накопление", 
 "reduce_list", "fold_left", "fold_right",
 # Комбинаторика
 'список_перестановок', 'список_сочетаний', 'сочетания_с_возвратом',
 'множество_всех_подмножеств', 'декартово_произведение',
 # Множества
 'объединение', 'пересечение', 'разность', 'симметричная_разность',
 'является_подмножеством', 'является_надмножеством', 'непересекающиеся',
 # Словари
 'dict_get', 'dict_set', 'dict_delete', 'dict_keys', 'dict_values', 
 'dict_items', 'dict_merge', 'dict_deep_merge', 'dict_filter', 'dict_map', 
 'dict_map_keys', 'dict_map_values', 'dict_invert', 'dict_group_by', 
 'dict_pick', 'dict_omit', 'dict_has', 'dict_size', 'dict_empty', 
 'dict_default', 'dict_flatten', 'dict_unflatten',
 # Утилиты
 'range_list', 'linspace', 'logspace', 'repeat', 'replicate', 'cycle', 
 "чередовать", "чередовать_шортест", "перемежать", "компактировать", "без", 
 'difference_list', 'intersection_list', 'union_list', 'образец', 'выбор', 
 'варианты', 'генерировать', 'повторять', 'разворачивать', 
]
$ cat /workspace/requirements.txt && echo "---" && cat /workspace/pyproject.toml && echo "---" && cat /workspace/README.md
cat /workspace/requirements.txt && echo "---" && cat /workspace/pyproject.toml && echo "---" && cat /workspace/README.md
# Основные зависимости
ply>=3.11
pymorphy2>=0.9.1
pymorphy2-dicts-ru>=2.4
# Ускорение работы кода (JIT-компиляция и оптимизация)
numba>=0.57.0
cython>=3.0.0
pydantic>=2.0.0
# Интерфейс командной строки и утилиты
click>=8.0.0
rich>=12.0.0
prompt_toolkit>=3.0.0
colorama>=0.4.6
# Работа с данными и сериализация
orjson>=3.9.0
msgpack>=1.0.5
pyyaml>=6.0
# Парсинг и обработка текста
tree_sitter>=0.20.0
regex>=2023.0.0
chardet>=5.0.0
# Утилиты и инструменты
typing_extensions>=4.5.0
functools32>=3.2.3.post1
cachetools>=5.3.0
psutil>=5.9.0
# Тестирование и линтинг
pytest>=7.0.0
pytest-cov>=4.0.0
black>=22.0.0
flake8>=4.0.0
mypy>=0.950
isort>=5.12.0
# Сборка в исполняемый файл
pyoxidizer>=0.22.0
pyinstaller>=5.0.0
# Дополнительные тяжелые библиотеки для максимальной производительности
# numpy>=1.24.0 # ~15 МБ — числовые вычисления
# scipy>=1.10.0 # ~35 МБ — научные вычисления
# llvmlite>=0.40.0 # ~40 МБ — JIT-компиляция (требуется для numba)
---
[система сборки]
requires = ["setuptools>=61.0", "wheel"]
build-backend = "setuptools.build_meta"
[project]
name = "ruspython"
version = "1.2.0"
description = "Русский Питон — язык программирования с русским синтаксисом (полноценный интерпретатор)"
readme = "README.md"
license = {text = "MIT"}
authors = [
 {name = "Команда Русский Питон", email = "ruspython@example.com"}
]
keywords = ["русский", "питон", "язык программирования", "русский язык", "язык программирования"]
классификаторы = [
 "Статус разработки:: 4 - бета", 
 "Целевая аудитория :: Разработчики", 
 "Лицензия :: Одобрена OSI :: Лицензия MIT", 
 "Язык программирования :: Python :: 3", 
 "Язык программирования :: Python :: 3.8", 
 "Язык программирования :: Python :: 3.9", 
 "Язык программирования :: Python :: 3.10", 
 "Язык программирования :: Python :: 3.11", 
 "Тема :: Разработка программного обеспечения :: Компиляторы", 
]
требуется-python = ">=3.8"
зависимости = [ 
"ply>=3,11", 
"pymorphy2>=0,9,1", 
"pymorphy2-dicts-ru>=2,4", 
"numba>=0.57.0", 
"cython>=3.0.0", 
"pydantic>=2.0.0", 
"click>=8.0.0", 
"rich>=12.0.0", 
"prompt_toolkit>=3.0.0", 
"colorama>=0.4.6", 
"orjson>=3.9.0", 
"msgpack>=1.0.5", 
"pyyaml>=6.0", 
"tree_sitter>=0.20.0", 
"regex>=2023.0.0", 
"chardet>=5.0.0", 
"typing_extensions>=4.5.0", 
"cachetools>=5.3.0", 
"psutil>=5.9.0", 
]
[project.optional-dependencies]
dev = [
 "pytest>=7.0.0",
 "pytest-cov>=4.0.0",
 "black>=22.0.0",
 "flake8>=4.0.0",
 "mypy>=0.950",
 "isort>=5.12.0",
]
perf = [
 # Тяжелые библиотеки для максимальной производительности
 "numpy>=1.24.0", # ~15 МБ — числовые вычисления
 "scipy>=1.10.0", # ~35 МБ — научные вычисления
 "llvmlite>=0.40.0", # ~40 МБ — JIT-компиляция (требуется для numba)
]
full = [
 "ruspython[dev,perf]",
 "pyinstaller>=5.0.0",
 "functools32>=3.2.3.post1",
]
[project.scripts]
ruspython = "src.cli.main:main"
[project.urls]
Домашняя страница = "https://github.com/ruspython/ruspython"
Документация = "https://ruspython.readthedocs.io"
Репозиторий = "https://github.com/ruspython/ruspython"
[tool.setuptools.packages.find]
where = ["."]
include = ["src*"]
---
# Русский Питон v1.0.0
Промышленный компилятор языка программирования с русским синтаксисом. 
## Возможности
- Полный русский синтаксис для всех конструкций Python
- Совместимость с экосистемой Python
- Лексер, парсер, транслятор в AST Python
- Поддержка функций, классов, условий, циклов, исключений
- Интерпретатор с поддержкой базовых операций
- Интерфейс командной строки и режим REPL
## Установка
### Вариант 1. Установка в виде пакета Python (рекомендуется)
```bash
pip install -e .
```
После установки в терминале доступна команда `ruspython`. 
### Вариант 2. Запуск через Python
```bash
python ruspython.py --help
```
### Вариант 3. Создание отдельного исполняемого файла
```bash
# Для Linux/Mac
./build.sh
# Для Windows (PowerShell)
pyinstaller --onefile --name ruspython ruspython.py
```
Исполняемый файл будет создан в папке `dist/`.
### Вариант 4. Запуск в терминале Windows
В Windows доступен запуск через пакетный файл:
```cmd
ruspython.bat examples/hello.ру
ruspython.bat --tokens hello.ру
ruspython.bat --repl
ruspython.bat --help
```
Для удобства можно добавить директорию с `ruspython.bat` в переменную PATH
или использовать полный путь к файлу. 
### Вариант 5. Автоматическая установка в Windows
**Способ А. Использование установочного скрипта**
Если вы уже скачали проект, запустите файл установки:
```cmd
install_windows.bat
```
Этот скрипт автоматически проверит наличие Python, установит зависимости
и зарегистрирует команду `ruspython` в системе.
**Способ Б: загрузка и установка с GitHub**
Используйте скрипт автоматической загрузки:
```cmd
download_windows.bat
```
Этот скрипт:
- Проверяет наличие Git (если есть — клонирует репозиторий)
- Если Git не установлен, скачивает архив с GitHub через PowerShell/curl
- Автоматически устанавливает все зависимости
- Регистрирует команду `ruspython` в системе
**Способ В: установка из архива вручную**
1. Откройте https://github.com/ruspython/ruspython
2. Нажмите кнопку «Код» → «Скачать ZIP»
3. Распакуйте архив в удобную папку
4. Откройте командную строку в этой папке
5. Выполните команды:
```cmd
pip install -r requirements.txt
pip install -e .
```
После установки команда `ruspython` будет доступна из любой директории. 
## Использование
```bash
# Выполнение файла
ruspython examples/hello.ру
# Показать токены
ruspython --tokens examples/hello.ру
# Показать дерево AST
ruspython --ast examples/hello.ру
# Режим REPL (интерактивная консоль)
ruspython --repl
# Справка
ruspython --help
```
## Пример программы
```русский
# Пример программы на русском языке
функция привет(имя):
 печать(f"Привет, {имя}!")
 если имя == "Мир":
 вернуть истину
 иначе:
 вернуть ложь
 для i в диапазоне(10):
 если i % 2 == 0:
 вывести(i)
привет("Разработчик")
```
## Структура проекта
```
/workspace
├── ruspython.py # Точка входа в приложение
├── pyproject.toml # Конфигурация сборки
├── build.sh # Скрипт для сборки исполняемого файла
├── src/
│ ├── __init__.py # Основной модуль
│ ├── core/
│ │ ├── lexer.py # Лексический анализатор
│ │ └── parser.py # Синтаксический анализатор (AST)
│ ├── backend/
│ │ └── translator.py # Транслятор в код Python
│ ├── runtime/
│ │ └── interpreter.py# Интерпретатор
│ └── cli/
│ └── main.py # Интерфейс командной строки
└── examples/
 └── hello.ru # Пример программы
```
## Требования
- Python 3.8+
- Зависимости указаны в `requirements.txt`
## Лицензия
MIT