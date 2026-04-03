# Русский Питон - CLI интерфейс
# Версия 1.1.0 - Полноценное исполнение с обновлением
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
    """Выполнение файла с полным циклом: токенизация -> парсинг -> исполнение."""
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
    print("Обновление Русский Питон до последней версии...")
    print("Команда: pip install --upgrade ruspython\n")
    
    try:
        result = subprocess.run(
            [sys.executable, "-m", "pip", "install", "--upgrade", "ruspython"],
            capture_output=True,
            text=True
        )
        
        if result.returncode == 0:
            print("✓ Успешно обновлено!")
            print(result.stdout)
        else:
            print("✗ Ошибка обновления:")
            print(result.stderr)
    except Exception as e:
        print(f"Ошибка: {e}")


def repl():
    """REPL режим с полным исполнением."""
    print("Русский Питон v1.1.0 - REPL режим (полное исполнение)")
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
        description="Русский Питон - язык программирования с русским синтаксисом",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Примеры использования:
  ruspython examples/hello.ру       Выполнить файл
  ruspython --tokens hello.ру       Показать токены
  ruspython --ast hello.ру          Показать AST дерево
  ruspython --repl                  Запустить REPL режим
  ruspython --update                Обновить до новой версии
        """
    )
    
    parser.add_argument('file', nargs='?', help='Файл для выполнения')
    parser.add_argument('--tokens', '-t', action='store_true', help='Показать токены')
    parser.add_argument('--ast', '-a', action='store_true', help='Показать AST дерево')
    parser.add_argument('--translate', action='store_true', help='Транслировать в Python')
    parser.add_argument('--repl', '-r', action='store_true', help='Запустить REPL режим')
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
        print(f"Ошибка: Файл не найден: {filepath}")
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
        
        print(f"\n=== AST Дерево ===")
        print(ast.print_tree())
    
    elif args.translate:
        print("Трансляция в Python (в разработке)...")
    
    else:
        run_file(filepath)


if __name__ == "__main__":
    main()
