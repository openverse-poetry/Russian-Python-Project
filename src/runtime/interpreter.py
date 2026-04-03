# Русский Питон - Интерпретатор
from __future__ import annotations
import sys
sys.path.insert(0, '/workspace')

from src.core.parser import (
    ASTNode, Module, FunctionDef, Parameter, If, For, While,
    Return, Assign, BinaryOp, Call, Identifier, Number, String,
    Boolean, ExpressionStatement, NodeType
)


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
            '+': lambda a, b: a + b,
            '-': lambda a, b: a - b,
            '*': lambda a, b: a * b,
            '/': lambda a, b: a / b,
            '//': lambda a, b: a // b,
            '%': lambda a, b: a % b,
            '**': lambda a, b: a ** b,
            '==': lambda a, b: a == b,
            '!=': lambda a, b: a != b,
            '<': lambda a, b: a < b,
            '>': lambda a, b: a > b,
            '<=': lambda a, b: a <= b,
            '>=': lambda a, b: a >= b,
        }
        
        op_func = op_map.get(node.op)
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


def demo_interpret():
    from src.core.parser import Module, FunctionDef, Parameter, If, For, Return, Assign, BinaryOp, Call, Identifier, Number, String, Boolean, ExpressionStatement
    
    func = FunctionDef(
        name="привет",
        args=[Parameter(name="имя")],
        body=[
            ExpressionStatement(value=Call(func=Identifier(name="печать"), args=[String(value="Привет!")])),
            Return(value=Boolean(value=True))
        ],
        line=1
    )
    
    module = Module(body=[func], line=0)
    
    interpreter = RussianInterpreter()
    interpreter.interpret(module)
    
    print("=== Результат интерпретации ===")
    return interpreter


if __name__ == "__main__":
    demo_interpret()
