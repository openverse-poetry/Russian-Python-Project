# Русский Питон - CLI интерфейс
from __future__ import annotations
import sys
import os
import argparse
from pathlib import Path

sys.path.insert(0, '/workspace')

from src.core.lexer import RussianLexer, Token, TokenType
from src.core.parser import Module, ASTPrinter
from src.backend.translator import PythonTranslator
from src.runtime.interpreter import RussianInterpreter


def tokenize_file(filepath: str) -> list:
    """Токенизация файла."""
    with open(filepath, 'r', encoding='utf-8') as f:
        source = f.read()
    
    lexer = RussianLexer(source, filepath)
    tokens = lexer.tokenize()
    return tokens


def parse_file(filepath: str) -> Module:
    """Парсинг файла в AST."""
    # Пока заглушка - в будущем будет полноценный парсер
    from src.core.parser import FunctionDef, Parameter, ExpressionStatement, Call, Identifier, String, Return, Boolean
    
    with open(filepath, 'r', encoding='utf-8') as f:
        source = f.read()
    
    lexer = RussianLexer(source, filepath)
    tokens = lexer.tokenize()
    
    print(f"Файл прочитан: {filepath}")
    print(f"Токенов: {len(tokens)}")
    
    for token in tokens[:20]:
        print(f"  {token}")
    
    if len(tokens) > 20:
        print(f"  ... и еще {len(tokens) - 20} токенов")
    
    return None


def run_file(filepath: str):
    """Выполнение файла."""
    print(f"Выполнение файла: {filepath}")
    
    with open(filepath, 'r', encoding='utf-8') as f:
        source = f.read()
    
    lexer = RussianLexer(source, filepath)
    tokens = lexer.tokenize()
    
    print(f"Токенизация завершена. Найдено {len(tokens)} токенов.")
    
    interpreter = RussianInterpreter()
    
    print("\n=== Результат выполнения ===")
    
    for token in tokens:
        if token.type == TokenType.ИДЕНТИФИКАТОР and token.value == "печать":
            print("Найдена функция печать")
        elif token.type == TokenType.СТРОКА:
            print(f"Строка: {token.value}")
        elif token.type == TokenType.ЧИСЛО:
            print(f"Число: {token.value}")


def repl():
    """REPL режим."""
    print("Русский Питон v1.0.0 - REPL режим")
    print("Введите 'выход' для выхода\n")
    
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
            
            for token in tokens:
                print(f"  {token}")
            
        except KeyboardInterrupt:
            print("\n")
            continue
        except Exception as e:
            print(f"Ошибка: {e}")


def main():
    parser = argparse.ArgumentParser(
        description="Русский Питон - язык программирования с русским синтаксисом",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Примеры использования:
  ruspython examples/hello.ру       Выполнить файл
  ruspython --tokens hello.ру       Показать токены
  ruspython --repl                  Запустить REPL
        """
    )
    
    parser.add_argument('file', nargs='?', help='Файл для выполнения')
    parser.add_argument('--tokens', '-t', action='store_true', help='Показать токены')
    parser.add_argument('--ast', '-a', action='store_true', help='Показать AST')
    parser.add_argument('--translate', action='store_true', help='Транслировать в Python')
    parser.add_argument('--repl', '-r', action='store_true', help='Запустить REPL режим')
    parser.add_argument('--version', '-v', action='version', version='Русский Питон 1.0.0')
    
    args = parser.parse_args()
    
    if args.repl:
        repl()
        return
    
    if not args.file:
        parser.print_help()
        return
    
    filepath = args.file
    
    if not os.path.exists(filepath):
        print(f"Ошибка: Файл не найден: {filepath}")
        sys.exit(1)
    
    if args.tokens:
        tokens = tokenize_file(filepath)
        print(f"\n=== Токены ({len(tokens)}) ===")
        for token in tokens:
            print(token)
    
    elif args.ast:
        parse_file(filepath)
    
    elif args.translate:
        print("Трансляция в Python (в разработке)...")
    
    else:
        run_file(filepath)


if __name__ == "__main__":
    main()
