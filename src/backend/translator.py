# Русский Питон - Транслятор в Python код
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
        line=1
    )
    module = Module(body=[func], line=0)
    
    translator = PythonTranslator()
    python_code = translator.translate(module)
    
    print("=== Python код ===")
    print(python_code)
    return python_code


if __name__ == "__main__":
    demo_translate()
