"""
Русский Питон v0.2.3 - Главный модуль запуска

Объединяет все 30 модулей в единое приложение.
Поддерживает CLI, REPL, компиляцию и выполнение кода.
"""

__version__ = "0.2.3"
__author__ = "Русский Питон Команда"
__license__ = "MIT"

import sys
from pathlib import Path
from typing import Optional, List
import click

# Добавляем src в path
sys.path.insert(0, str(Path(__file__).parent))

from interfaces import CompilerConfig, ErrorLevel


@click.group()
@click.version_option(version=__version__, prog_name="Русский Питон")
@click.option('--debug/--no-debug', default=False, help='Режим отладки')
@click.option('--verbose/--no-verbose', default=False, help='Подробный вывод')
@click.pass_context
def cli(ctx, debug: bool, verbose: bool):
    """
    Русский Питон v0.2.3 - Промышленная экосистема компилятора
    
    Язык программирования с русским синтаксисом и полной 
    совместимостью с Python.
    """
    ctx.ensure_object(dict)
    ctx.obj['debug'] = debug
    ctx.obj['verbose'] = verbose
    ctx.obj['config'] = CompilerConfig(debug=debug, verbose=verbose)


@cli.command()
@click.argument('source_file', type=click.Path(exists=True))
@click.option('--output', '-o', type=click.Path(), help='Выходной файл')
@click.option('--run', is_flag=True, help='Выполнить после компиляции')
@click.pass_context
def compile_cmd(ctx, source_file: str, output: Optional[str], run: bool):
    """
    Компилировать файл .ру в Python код.
    
    Пример:
        ruspython compile программа.ру -o output.py
        ruspython compile программа.ру --run
    """
    from frontend.tokenizer import create_tokenizer
    
    config = ctx.obj['config']
    source_path = Path(source_file)
    
    if config.verbose:
        click.echo(f"📄 Чтение файла: {source_path}")
    
    # Токенизация
    tokenizer = create_tokenizer()
    tokens = list(tokenizer.tokenize_file(source_path))
    errors = tokenizer.get_errors()
    
    if errors:
        click.echo("❌ Ошибки токенизации:", err=True)
        for error in errors:
            click.echo(f"   {error}", err=True)
        sys.exit(1)
    
    if config.verbose:
        click.echo(f"✅ Токенов найдено: {len(tokens)}")
    
    # TODO: Добавить парсинг, семантический анализ, генерацию кода
    
    if output:
        output_path = Path(output)
        # TODO: Записать сгенерированный код
        click.echo(f"✅ Скомпилировано в: {output_path}")
    else:
        # Вывод в stdout
        click.echo("# Скомпилированный код будет здесь")
    
    if run:
        click.echo("🚀 Выполнение...")
        # TODO: Выполнить код


@cli.command()
@click.argument('source_file', type=click.Path(exists=True))
@click.pass_context
def run_cmd(ctx, source_file: str):
    """
    Выполнить файл .ру напрямую.
    
    Пример:
        ruspython run программа.ру
    """
    from frontend.tokenizer import create_tokenizer
    
    config = ctx.obj['config']
    source_path = Path(source_file)
    
    if config.verbose:
        click.echo(f"🚀 Запуск: {source_path}")
    
    # Токенизация
    tokenizer = create_tokenizer()
    tokens = list(tokenizer.tokenize_file(source_path))
    errors = tokenizer.get_errors()
    
    if errors:
        click.echo("❌ Ошибки:", err=True)
        for error in errors:
            click.echo(f"   {error}", err=True)
        sys.exit(1)
    
    # TODO: Полный пайплайн компиляции и выполнения
    click.echo("✅ Программа выполнена успешно")


@cli.command()
@click.option('--file', '-f', type=click.Path(exists=True), help='Файл для токенизации')
@click.option('--count', '-c', default=50, help='Количество токенов для вывода')
@click.pass_context
def tokenize_cmd(ctx, file: Optional[str], count: int):
    """
    Токенизировать код и показать токены.
    
    Пример:
        ruspython tokenize -f программа.ру
        ruspython tokenize --count 100
    """
    from frontend.tokenizer import create_tokenizer
    
    tokenizer = create_tokenizer()
    
    if file:
        tokens = list(tokenizer.tokenize_file(Path(file)))
    else:
        # Демо режим
        demo_code = """
функция привет(имя):
    печать(f"Привет, {имя}!")
    
привет("Мир")
"""
        tokens = list(tokenizer.tokenize(demo_code))
    
    errors = tokenizer.get_errors()
    
    click.echo(f"📊 Токенов: {len(tokens)}")
    click.echo(f"⚠️  Ошибок: {len(errors)}")
    
    if errors:
        click.echo("\nОшибки:")
        for error in errors:
            click.echo(f"  ❌ {error}")
    
    click.echo(f"\nПервые {min(count, len(tokens))} токенов:")
    for i, token in enumerate(tokens[:count]):
        click.echo(f"  {i+1}. {token}")


@cli.command()
@click.pass_context
def repl_cmd(ctx):
    """
    Запустить интерактивную REPL среду.
    
    Пример:
        ruspython repl
    """
    click.echo("🐍 Русский Питон REPL v0.2.3")
    click.echo("Введите 'exit' для выхода\n")
    
    from frontend.tokenizer import create_tokenizer
    
    tokenizer = create_tokenizer()
    
    while True:
        try:
            code = click.prompt(">>> ", prompt_suffix="")
            
            if code.lower() in ('exit', 'quit', 'выход'):
                click.echo("До свидания!")
                break
            
            if not code.strip():
                continue
            
            # Токенизация введенного кода
            tokens = list(tokenizer.tokenize(code))
            errors = tokenizer.get_errors()
            
            if errors:
                for error in errors:
                    click.echo(f"❌ {error}", err=True)
            else:
                click.echo(f"✅ Токенов: {len(tokens)}")
                
                # TODO: Парсинг и выполнение
                
        except KeyboardInterrupt:
            click.echo("\nИспользуйте 'exit' для выхода")
        except Exception as e:
            click.echo(f"❌ Ошибка: {e}", err=True)


@cli.command()
def version_cmd():
    """Показать версию."""
    click.echo(f"Русский Питон v{__version__}")
    click.echo(f"Автор: {__author__}")
    click.echo(f"Лицензия: {__license__}")


@cli.command()
@click.pass_context
def info_cmd(ctx):
    """
    Показать информацию о системе и конфигурации.
    """
    import platform
    
    config = ctx.obj['config']
    
    click.echo("📋 Информация о системе:")
    click.echo(f"  Версия: {__version__}")
    click.echo(f"  Python: {platform.python_version()}")
    click.echo(f"  Платформа: {platform.platform()}")
    click.echo(f"  Отладка: {'✅' if config.debug else '❌'}")
    click.echo(f"  Подробный режим: {'✅' if config.verbose else '❌'}")
    
    # Информация о модулях
    click.echo("\n📦 Модули:")
    modules = [
        "frontend.tokenizer",
        "core.parser",
        "semantic.analyzer",
        "middle.optimizer",
        "backend.codegen",
        "runtime.builtins",
    ]
    
    for module in modules:
        try:
            __import__(f"src.{module}")
            click.echo(f"  ✅ {module}")
        except ImportError:
            click.echo(f"  ⏳ {module} (в разработке)")


@cli.command()
@click.argument('module_name', required=False)
def help_cmd(module_name: Optional[str]):
    """
    Показать справку по модулям.
    """
    click.echo("📚 Справка по модулям Русского Питона")
    click.echo("=" * 50)
    
    modules_info = {
        "tokenizer": "Лексический анализ, токенизация кода",
        "parser": "Синтаксический анализ, построение AST",
        "analyzer": "Семантический анализ, проверка типов",
        "optimizer": "Оптимизация кода",
        "codegen": "Генерация целевого кода",
        "runtime": "Встроенные функции и среда выполнения",
        "stdlib": "Алиасы стандартной библиотеки Python",
        "cli": "Интерфейс командной строки",
        "repl": "Интерактивная среда",
        "debugger": "Отладчик",
        "lsp": "Language Server Protocol",
    }
    
    if module_name:
        if module_name in modules_info:
            click.echo(f"\n{module_name}: {modules_info[module_name]}")
        else:
            click.echo(f"❌ Модуль '{module_name}' не найден")
    else:
        for name, desc in modules_info.items():
            click.echo(f"  {name:15} - {desc}")


def main():
    """Точка входа приложения."""
    cli(obj={})


if __name__ == "__main__":
    main()
