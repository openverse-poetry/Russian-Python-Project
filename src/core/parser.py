# Русский Питон - Абстрактное Синтаксическое Дерево (AST)
# Версия 1.0.0 - Полная система узлов

from __future__ import annotations
from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from typing import List, Optional, Dict, Any, Union, Tuple
from enum import Enum, auto


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


if __name__ == "__main__":
    demo_ast()
