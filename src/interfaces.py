"""
Русский Питон v0.2.3 - Промышленная экосистема компилятора

Архитектура из 30 независимых модулей с четкими интерфейсами.
Каждый модуль автономен, тестируем и может работать отдельно.
Все модули объединяются в единое приложение через главный интерфейс.
"""

__version__ = "0.2.3"
__author__ = "Русский Питон Команда"
__license__ = "MIT"

from abc import ABC, abstractmethod
from typing import Any, Dict, List, Optional, Iterator, Union
from dataclasses import dataclass
from enum import Enum, auto
from pathlib import Path
import sys


# =============================================================================
# БАЗОВЫЕ ИНТЕРФЕЙСЫ (ABSTRACT BASE CLASSES)
# =============================================================================

class IToken(ABC):
    """Интерфейс токена - базовая единица лексического анализа."""
    
    @property
    @abstractmethod
    def type(self) -> str:
        """Тип токена (например, 'ЕСЛИ', 'ИДЕНТИФИКАТОР', 'ЧИСЛО')."""
        pass
    
    @property
    @abstractmethod
    def value(self) -> Any:
        """Значение токена."""
        pass
    
    @property
    @abstractmethod
    def line(self) -> int:
        """Номер строки в исходном коде."""
        pass
    
    @property
    @abstractmethod
    def column(self) -> int:
        """Номер колонки в строке."""
        pass
    
    @abstractmethod
    def __repr__(self) -> str:
        """Строковое представление токена."""
        pass


class ILexer(ABC):
    """Интерфейс лексера - преобразует исходный код в поток токенов."""
    
    @abstractmethod
    def tokenize(self, source: str) -> Iterator[IToken]:
        """Токенизирует исходный код, возвращая поток токенов."""
        pass
    
    @abstractmethod
    def tokenize_file(self, filepath: Path) -> Iterator[IToken]:
        """Токенизирует файл, возвращая поток токенов."""
        pass
    
    @abstractmethod
    def get_errors(self) -> List[str]:
        """Возвращает список ошибок лексического анализа."""
        pass


class IASTNode(ABC):
    """Интерфейс узла абстрактного синтаксического дерева."""
    
    @property
    @abstractmethod
    def node_type(self) -> str:
        """Тип узла AST."""
        pass
    
    @property
    @abstractmethod
    def children(self) -> List['IASTNode']:
        """Дочерние узлы."""
        pass
    
    @abstractmethod
    def accept(self, visitor: 'IASTVisitor') -> Any:
        """Принимает посетителя для обхода дерева."""
        pass
    
    @abstractmethod
    def to_dict(self) -> Dict[str, Any]:
        """Преобразует узел в словарь."""
        pass


class IASTVisitor(ABC):
    """Интерфейс посетителя AST."""
    
    @abstractmethod
    def visit(self, node: IASTNode) -> Any:
        """Посещает узел AST."""
        pass


class IParser(ABC):
    """Интерфейс парсера - преобразует поток токенов в AST."""
    
    @abstractmethod
    def parse(self, tokens: Iterator[IToken]) -> IASTNode:
        """Парсит поток токенов, возвращая корневой узел AST."""
        pass
    
    @abstractmethod
    def parse_file(self, filepath: Path) -> IASTNode:
        """Парсит файл, возвращая корневой узел AST."""
        pass
    
    @abstractmethod
    def get_errors(self) -> List[str]:
        """Возвращает список ошибок синтаксического анализа."""
        pass


class ISemanticAnalyzer(ABC):
    """Интерфейс семантического анализатора."""
    
    @abstractmethod
    def analyze(self, ast: IASTNode) -> IASTNode:
        """Выполняет семантический анализ AST."""
        pass
    
    @abstractmethod
    def get_symbols(self) -> Dict[str, Any]:
        """Возвращает таблицу символов."""
        pass
    
    @abstractmethod
    def get_errors(self) -> List[str]:
        """Возвращает список семантических ошибок."""
        pass


class IOptimizer(ABC):
    """Интерфейс оптимизатора кода."""
    
    @abstractmethod
    def optimize(self, ast: IASTNode) -> IASTNode:
        """Оптимизирует AST."""
        pass
    
    @abstractmethod
    def get_stats(self) -> Dict[str, Any]:
        """Возвращает статистику оптимизации."""
        pass


class ICodeGenerator(ABC):
    """Интерфейс генератора кода."""
    
    @abstractmethod
    def generate(self, ast: IASTNode) -> str:
        """Генерирует целевой код из AST."""
        pass
    
    @abstractmethod
    def generate_to_file(self, ast: IASTNode, output_path: Path) -> None:
        """Генерирует код в файл."""
        pass


class IRuntime(ABC):
    """Интерфейс рантайма - выполнение скомпилированного кода."""
    
    @abstractmethod
    def execute(self, code: str) -> Any:
        """Выполняет код и возвращает результат."""
        pass
    
    @abstractmethod
    def execute_file(self, filepath: Path) -> Any:
        """Выполняет файл и возвращает результат."""
        pass
    
    @abstractmethod
    def get_builtin_functions(self) -> Dict[str, Any]:
        """Возвращает встроенные функции."""
        pass


class IErrorReporter(ABC):
    """Интерфейс системы отчетности об ошибках."""
    
    @abstractmethod
    def report_error(self, message: str, line: int = None, column: int = None) -> None:
        """Сообщает об ошибке."""
        pass
    
    @abstractmethod
    def report_warning(self, message: str, line: int = None, column: int = None) -> None:
        """Сообщает о предупреждении."""
        pass
    
    @abstractmethod
    def has_errors(self) -> bool:
        """Проверяет наличие ошибок."""
        pass
    
    @abstractmethod
    def get_all_messages(self) -> List[Dict[str, Any]]:
        """Возвращает все сообщения."""
        pass


class ICompiler(ABC):
    """Главный интерфейс компилятора - объединяет все этапы."""
    
    @abstractmethod
    def compile(self, source: str) -> str:
        """Компилирует исходный код в целевой код."""
        pass
    
    @abstractmethod
    def compile_file(self, input_path: Path, output_path: Path) -> None:
        """Компилирует файл."""
        pass
    
    @abstractmethod
    def run(self, source: str) -> Any:
        """Компилирует и выполняет код."""
        pass
    
    @abstractmethod
    def get_pipeline(self) -> List[str]:
        """Возвращает этапы конвейера компиляции."""
        pass


# =============================================================================
# БАЗОВЫЕ КЛАССЫ ДАННЫХ
# =============================================================================

@dataclass
class TokenPosition:
    """Позиция токена в исходном коде."""
    line: int
    column: int
    offset: int


@dataclass
class SourceLocation:
    """Местоположение в исходном коде."""
    file: str
    line: int
    column: int
    end_line: int
    end_column: int


@dataclass
class CompilerConfig:
    """Конфигурация компилятора."""
    debug: bool = False
    optimize: bool = True
    target: str = "python"
    output_dir: Path = Path("./output")
    verbose: bool = False
    strict_mode: bool = False


class ErrorLevel(Enum):
    """Уровень ошибки."""
    INFO = auto()
    WARNING = auto()
    ERROR = auto()
    FATAL = auto()


@dataclass
class CompilerMessage:
    """Сообщение компилятора."""
    level: ErrorLevel
    message: str
    location: Optional[SourceLocation]
    code: Optional[str] = None


# =============================================================================
# ЭКСПОРТ ИНТЕРФЕЙСОВ
# =============================================================================

__all__ = [
    # Интерфейсы
    'IToken',
    'ILexer',
    'IASTNode',
    'IASTVisitor',
    'IParser',
    'ISemanticAnalyzer',
    'IOptimizer',
    'ICodeGenerator',
    'IRuntime',
    'IErrorReporter',
    'ICompiler',
    
    # Классы данных
    'TokenPosition',
    'SourceLocation',
    'CompilerConfig',
    'ErrorLevel',
    'CompilerMessage',
]


if __name__ == "__main__":
    print(f"Русский Питон Interfaces v{__version__}")
    print("=" * 50)
    print("Доступные интерфейсы:")
    for name in __all__:
        print(f"  - {name}")
    print("\nВсе интерфейсы определены в src/interfaces.py")
    print("Каждый модуль должен реализовывать соответствующие интерфейсы.")
