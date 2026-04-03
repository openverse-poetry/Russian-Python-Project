# Русский Питон - Промышленный компилятор с русским синтаксисом
# Версия 1.0.0 - Полная совместимость с Python, расширенные возможности

"""
Русский Питон v1.0.0 - Промышленная версия языка программирования

Особенности версии 1.0.0:
- Полный русский синтаксис для всех конструкций Python
- Совместимость с экосистемой Python (импорт .py модулей)
- Улучшенная система типов с поддержкой русских аннотаций
- Встроенный оптимизатор байт-кода
- Параллельное выполнение через конструкцию "параллельно"
- Асинхронные конструкции на русском языке
- Встроенная система профилирования и отладки
- Интеграция с Jupyter Notebook через русские магические команды
- Поддержка макросов и метапрограммирования
- Расширенная обработка ошибок с русскими сообщениями
- Автодополнение в REPL с учетом морфологии
- Лингвистический анализ кода через pymorphy2
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
