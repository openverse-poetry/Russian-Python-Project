# Русский Питон - Абстрактное Синтаксическое Дерево (AST) и Парсер
# Версия 1.1.0 - Полноценный парсер и исполнитель

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
    ВЫБРОСИТЬ = auto()
    ВОЗВРАТ = auto()
    ПРЕРВАТЬ = auto()
    ПРОДОЛЖИТЬ = auto()
    ПРИСВАИВАНИЕ = auto()
    БИНАРНАЯ = auto()
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
    ЖДАТЬ = auto()
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
        prefix = "  " * indent
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
                result += f"{prefix}  {name}: "
                result += child.print_tree(indent + 2)
        else:
            result += f" (line={self.line})\n"
        return result


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
    test: ASTNode = field(default_factory=lambda: Boolean(True))
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
        prefix = "  " * self.indent
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
    print("=== AST Дерево ===")
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
        
        while self._current() and not self._match(TokenType.КОНЕЦ_ФАЙЛА):
            stmt = self._parse_statement()
            if stmt:
                module.body.append(stmt)
        
        return module
    
    def _parse_statement(self) -> Optional[ASTNode]:
        """Парсинг утверждения."""
        token = self._current()
        if not token or token.type == TokenType.КОНЕЦ_ФАЙЛА:
            return None
        
        # Пропуск токенов НОВАЯ_СТРОКА
        if token.type == TokenType.НОВАЯ_СТРОКА:
            self._advance()
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
        elif token.type == TokenType.РАВНО or token.type == TokenType.ИДЕНТИФИКАТОР:
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
        """Парсинг условия если."""
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
        """Парсинг цикла для."""
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
        
        # Ожидаем ОТСТУП после двоеточия
        if self._match(TokenType.ОТСТУП):
            self._advance()
        
        while self._current() and not self._match(TokenType.DEDENT, TokenType.ИНАЧЕ, TokenType.КОНЕЦ_ФАЙЛА):
            stmt = self._parse_statement()
            if stmt:
                statements.append(stmt)
            else:
                break
        
        # Закрываем блок с DEDENT
        if self._match(TokenType.DEDENT):
            self._advance()
        
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
    
    lexer = RussianLexer(test_code)
    tokens = lexer.tokenize()
    
    print("=== Токены ===")
    for t in tokens[:20]:
        print(t)
    
    print("\n=== Парсинг ===")
    parser = RussianParser(tokens)
    ast = parser.parse()
    print(ast.print_tree())
