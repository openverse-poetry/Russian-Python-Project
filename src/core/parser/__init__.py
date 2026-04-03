"""
Модуль 2: Синтаксический анализатор (Parser)
Реализация IParser интерфейса
Объем: ~1800 строк

Отвечает за синтаксический анализ потока токенов и построение AST.
Поддерживает все конструкции языка:
- Объявления функций и классов
- Управляющие конструкции (если, пока, для)
- Выражения всех видов
- Операторы присваивания
- Импорт и импорт из
- Обработка исключений
- Контекстные менеджеры
"""

from typing import Iterator, List, Optional, Dict, Any, Union
from pathlib import Path
from dataclasses import dataclass, field
from enum import Enum, auto
import sys

sys.path.insert(0, str(Path(__file__).parent.parent.parent))
from interfaces import IParser, IASTNode, IToken, SourceLocation


# =============================================================================
# ТИПЫ УЗЛОВ AST
# =============================================================================

class NodeType(Enum):
    """Типы узлов AST."""
    # Программные конструкции
    PROGRAM = auto()
    FUNCTION_DEF = auto()
    CLASS_DEF = auto()
    IMPORT = auto()
    IMPORT_FROM = auto()
    
    # Управляющие конструкции
    IF_STMT = auto()
    WHILE_STMT = auto()
    FOR_STMT = auto()
    TRY_STMT = auto()
    WITH_STMT = auto()
    RETURN_STMT = auto()
    BREAK_STMT = auto()
    CONTINUE_STMT = auto()
    PASS_STMT = auto()
    
    # Выражения
    BINARY_OP = auto()
    UNARY_OP = auto()
    CALL = auto()
    ATTRIBUTE = auto()
    SUBSCRIPT = auto()
    SLICE = auto()
    
    # Литералы
    NUMBER = auto()
    STRING = auto()
    BOOLEAN = auto()
    NONE = auto()
    LIST = auto()
    TUPLE = auto()
    DICT = auto()
    SET = auto()
    
    # Идентификаторы
    IDENTIFIER = auto()
    ASSIGNMENT = auto()
    AUGMENTED_ASSIGN = auto()


@dataclass
class ASTNode(IASTNode):
    """Базовый узел AST."""
    
    _node_type: NodeType = field(default=NodeType.PROGRAM, init=False)
    children: List['ASTNode'] = field(default_factory=list)
    attributes: Dict[str, Any] = field(default_factory=dict)
    line: int = 0
    column: int = 0
    
    @property
    def node_type(self) -> str:
        return self._node_type.name if isinstance(self._node_type, NodeType) else str(self._node_type)
    
    def accept(self, visitor: 'IASTVisitor') -> Any:
        return visitor.visit(self)
    
    def to_dict(self) -> Dict[str, Any]:
        return {
            "type": self.node_type,
            "children": [child.to_dict() for child in self.children],
            "attributes": self.attributes,
            "line": self.line,
            "column": self.column
        }
    
    def __repr__(self) -> str:
        return f"ASTNode({self.node_type}, line={self.line})"


# =============================================================================
# КОНКРЕТНЫЕ ТИПЫ УЗЛОВ
# =============================================================================

@dataclass
class ProgramNode(ASTNode):
    """Корневой узел программы."""
    
    statements: List[ASTNode] = field(default_factory=list)
    
    def __post_init__(self):
        self.node_type = NodeType.PROGRAM
        self.children = self.statements


@dataclass
class FunctionDefNode(ASTNode):
    """Объявление функции."""
    
    name: str = ""
    parameters: List[str] = field(default_factory=list)
    body: List[ASTNode] = field(default_factory=list)
    decorators: List[ASTNode] = field(default_factory=list)
    return_type: Optional[str] = None
    
    def __post_init__(self):
        self.node_type = NodeType.FUNCTION_DEF


@dataclass
class IfStmtNode(ASTNode):
    """Оператор if."""
    
    condition: Optional[ASTNode] = None
    then_body: List[ASTNode] = field(default_factory=list)
    else_body: List[ASTNode] = field(default_factory=list)
    elif_clauses: List[tuple] = field(default_factory=list)  # (condition, body)
    
    def __post_init__(self):
        self.node_type = NodeType.IF_STMT


@dataclass
class WhileStmtNode(ASTNode):
    """Оператор while."""
    
    condition: Optional[ASTNode] = None
    body: List[ASTNode] = field(default_factory=list)
    else_body: List[ASTNode] = field(default_factory=list)
    
    def __post_init__(self):
        self.node_type = NodeType.WHILE_STMT


@dataclass
class ForStmtNode(ASTNode):
    """Оператор for."""
    
    target: Optional[ASTNode] = None
    iterable: Optional[ASTNode] = None
    body: List[ASTNode] = field(default_factory=list)
    else_body: List[ASTNode] = field(default_factory=list)
    
    def __post_init__(self):
        self.node_type = NodeType.FOR_STMT


@dataclass
class BinaryOpNode(ASTNode):
    """Бинарная операция."""
    
    operator: str = ""
    left: Optional[ASTNode] = None
    right: Optional[ASTNode] = None
    
    def __post_init__(self):
        self.node_type = NodeType.BINARY_OP


@dataclass
class CallNode(ASTNode):
    """Вызов функции."""
    
    func: Optional[ASTNode] = None
    args: List[ASTNode] = field(default_factory=list)
    kwargs: Dict[str, ASTNode] = field(default_factory=dict)
    
    def __post_init__(self):
        self.node_type = NodeType.CALL


@dataclass
class NumberNode(ASTNode):
    """Числовой литерал."""
    
    value: Union[int, float] = 0
    
    def __post_init__(self):
        self._node_type = NodeType.NUMBER
        self.attributes["value"] = self.value
        self.children = []


@dataclass
class StringNode(ASTNode):
    """Строковый литерал."""
    
    value: str = ""
    
    def __post_init__(self):
        self._node_type = NodeType.STRING
        self.attributes["value"] = self.value
        self.children = []


@dataclass
class IdentifierNode(ASTNode):
    """Идентификатор."""
    
    name: str = ""
    
    def __post_init__(self):
        self._node_type = NodeType.IDENTIFIER
        self.attributes["name"] = self.name
        self.children = []


# =============================================================================
# ПАРСЕР
# =============================================================================

class Parser(IParser):
    """
    Синтаксический анализатор с рекурсивным спуском.
    
    Грамматика (упрощенная):
        program     ::= statement*
        statement   ::= function_def | class_def | if_stmt | while_stmt | 
                        for_stmt | try_stmt | with_stmt | return_stmt | 
                        assignment | expression_stmt
        function_def ::= 'функция' identifier '(' parameters? ')' ':' block
        if_stmt     ::= 'если' expression ':' block ('иначе если' expression ':' block)* 
                        ('иначе' ':' block)?
        ...
    """
    
    def __init__(self):
        self._tokens: List[IToken] = []
        self._pos = 0
        self._errors: List[str] = []
        
    def parse(self, tokens: Iterator[IToken]) -> ASTNode:
        """Парсит поток токенов."""
        self._tokens = list(tokens)
        self._pos = 0
        self._errors = []
        
        return self._parse_program()
    
    def parse_file(self, filepath: Path) -> ASTNode:
        """Парсит файл."""
        from frontend.tokenizer import create_tokenizer
        
        tokenizer = create_tokenizer()
        tokens = tokenizer.tokenize_file(filepath)
        errors = tokenizer.get_errors()
        
        if errors:
            self._errors.extend(errors)
            return ProgramNode()
        
        return self.parse(tokens)
    
    def get_errors(self) -> List[str]:
        return self._errors.copy()
    
    def _current_token(self) -> Optional[IToken]:
        """Возвращает текущий токен."""
        if self._pos >= len(self._tokens):
            return None
        return self._tokens[self._pos]
    
    def _peek_token(self, offset: int = 1) -> Optional[IToken]:
        """Заглядывает вперед."""
        pos = self._pos + offset
        if pos >= len(self._tokens):
            return None
        return self._tokens[pos]
    
    def _advance(self) -> Optional[IToken]:
        """Переходит к следующему токену."""
        token = self._current_token()
        self._pos += 1
        return token
    
    def _match(self, *types: str) -> bool:
        """Проверяет тип текущего токена."""
        token = self._current_token()
        if token is None:
            return False
        return token.type in types
    
    def _expect(self, type_: str, message: str = None) -> IToken:
        """Ожидает токен определенного типа."""
        token = self._current_token()
        if token is None or token.type != type_:
            msg = message or f"Ожидался токен {type_}"
            self._error(msg)
            return token
        return self._advance()
    
    def _error(self, message: str) -> None:
        """Добавляет ошибку."""
        token = self._current_token()
        if token:
            message = f"Строка {token.line}, колонка {token.column}: {message}"
        self._errors.append(message)
    
    def _parse_program(self) -> ProgramNode:
        """Парсит программу."""
        statements = []
        
        while not self._match("КОНЕЦ_ФАЙЛА"):
            stmt = self._parse_statement()
            if stmt:
                statements.append(stmt)
        
        return ProgramNode(statements=statements)
    
    def _parse_statement(self) -> Optional[ASTNode]:
        """Парсит оператор."""
        if self._match("ФУНКЦИЯ"):
            return self._parse_function_def()
        elif self._match("КЛАСС"):
            return self._parse_class_def()
        elif self._match("ЕСЛИ"):
            return self._parse_if_stmt()
        elif self._match("ПОКА"):
            return self._parse_while_stmt()
        elif self._match("ДЛЯ"):
            return self._parse_for_stmt()
        elif self._match("ВОЗВРАТ"):
            return self._parse_return_stmt()
        elif self._match("ИМПОРТ"):
            return self._parse_import()
        elif self._match("ПОПРОБУЙ"):
            return self._parse_try_stmt()
        elif self._match("С"):
            return self._parse_with_stmt()
        elif self._match("ИДЕНТИФИКАТОР"):
            # Может быть присваивание или выражение
            return self._parse_assignment_or_expr()
        else:
            return self._parse_expression_stmt()
    
    def _parse_function_def(self) -> FunctionDefNode:
        """Парсит объявление функции."""
        start_token = self._advance()  # Пропускаем 'функция'
        
        # Имя функции
        name_token = self._expect("ИДЕНТИФИКАТОР", "Ожидалось имя функции")
        name = name_token.value if name_token else ""
        
        # Параметры
        self._expect("ЛЕВАЯ_СКОБКА", "Ожидалась '('")
        parameters = self._parse_parameters()
        self._expect("ПРАВАЯ_СКОБКА", "Ожидалась ')'")
        
        # Тело функции
        self._expect("ДВОЕТОЧИЕ", "Ожидалось ':'")
        body = self._parse_block()
        
        return FunctionDefNode(
            name=name,
            parameters=parameters,
            body=body,
            line=start_token.line if start_token else 0,
            column=start_token.column if start_token else 0
        )
    
    def _parse_parameters(self) -> List[str]:
        """Парсит параметры функции."""
        parameters = []
        
        if self._match("ПРАВАЯ_СКОБКА"):
            return parameters
        
        while True:
            token = self._expect("ИДЕНТИФИКАТОР", "Ожидался параметр")
            if token:
                parameters.append(token.value)
            
            if self._match("ЗАПЯТАЯ"):
                self._advance()
            else:
                break
        
        return parameters
    
    def _parse_block(self) -> List[ASTNode]:
        """Парсит блок операторов."""
        statements = []
        
        # Пропускаем отступы и новые строки
        while self._match("ОТСТУП", "НОВЫЙ_СТРОКА"):
            self._advance()
        
        while not self._match("КОНЕЦ_ФАЙЛА"):
            # Проверяем конец блока
            if self._match("ПРАВАЯ_ФИГУРНАЯ"):
                break
            
            stmt = self._parse_statement()
            if stmt:
                statements.append(stmt)
            else:
                break
        
        return statements
    
    def _parse_if_stmt(self) -> IfStmtNode:
        """Парсит оператор if."""
        start_token = self._advance()  # Пропускаем 'если'
        
        condition = self._parse_expression()
        self._expect("ДВОЕТОЧИЕ", "Ожидалось ':'")
        then_body = self._parse_block()
        
        elif_clauses = []
        else_body = []
        
        # Проверяем 'иначе если'
        while self._match("ИНАЧЕ"):
            self._advance()
            if self._match("ЕСЛИ"):
                self._advance()
                elif_cond = self._parse_expression()
                self._expect("ДВОЕТОЧИЕ", "Ожидалось ':'")
                elif_body = self._parse_block()
                elif_clauses.append((elif_cond, elif_body))
            else:
                # Просто 'иначе'
                self._expect("ДВОЕТОЧИЕ", "Ожидалось ':'")
                else_body = self._parse_block()
                break
        
        return IfStmtNode(
            condition=condition,
            then_body=then_body,
            else_body=else_body,
            elif_clauses=elif_clauses,
            line=start_token.line if start_token else 0,
            column=start_token.column if start_token else 0
        )
    
    def _parse_while_stmt(self) -> WhileStmtNode:
        """Парсит оператор while."""
        start_token = self._advance()  # Пропускаем 'пока'
        
        condition = self._parse_expression()
        self._expect("ДВОЕТОЧИЕ", "Ожидалось ':'")
        body = self._parse_block()
        
        else_body = []
        if self._match("ИНАЧЕ"):
            self._advance()
            self._expect("ДВОЕТОЧИЕ", "Ожидалось ':'")
            else_body = self._parse_block()
        
        return WhileStmtNode(
            condition=condition,
            body=body,
            else_body=else_body,
            line=start_token.line if start_token else 0,
            column=start_token.column if start_token else 0
        )
    
    def _parse_for_stmt(self) -> ForStmtNode:
        """Парсит оператор for."""
        start_token = self._advance()  # Пропускаем 'для'
        
        target = self._parse_expression()
        self._expect("В", "Ожидалось 'в'")
        iterable = self._parse_expression()
        self._expect("ДВОЕТОЧИЕ", "Ожидалось ':'")
        body = self._parse_block()
        
        else_body = []
        if self._match("ИНАЧЕ"):
            self._advance()
            self._expect("ДВОЕТОЧИЕ", "Ожидалось ':'")
            else_body = self._parse_block()
        
        return ForStmtNode(
            target=target,
            iterable=iterable,
            body=body,
            else_body=else_body,
            line=start_token.line if start_token else 0,
            column=start_token.column if start_token else 0
        )
    
    def _parse_return_stmt(self) -> ASTNode:
        """Парсит оператор return."""
        start_token = self._advance()  # Пропускаем 'возврат'
        
        if self._match("ДВОЕТОЧИЕ", "НОВЫЙ_СТРОКА", "КОНЕЦ_ФАЙЛА"):
            value = None
        else:
            value = self._parse_expression()
        
        return ASTNode(
            node_type=NodeType.RETURN_STMT,
            children=[value] if value else [],
            line=start_token.line if start_token else 0,
            column=start_token.column if start_token else 0
        )
    
    def _parse_import(self) -> ASTNode:
        """Парсит оператор import."""
        start_token = self._advance()  # Пропускаем 'импорт'
        
        modules = []
        while True:
            token = self._expect("ИДЕНТИФИКАТОР", "Ожидалось имя модуля")
            if token:
                module_name = token.value
                
                # Проверяем 'как'
                alias = None
                if self._match("КАК"):
                    self._advance()
                    alias_token = self._expect("ИДЕНТИФИКАТОР", "Ожидался псевдоним")
                    if alias_token:
                        alias = alias_token.value
                
                modules.append((module_name, alias))
            
            if self._match("ЗАПЯТАЯ"):
                self._advance()
            else:
                break
        
        return ASTNode(
            node_type=NodeType.IMPORT,
            attributes={"modules": modules},
            line=start_token.line if start_token else 0,
            column=start_token.column if start_token else 0
        )
    
    def _parse_try_stmt(self) -> ASTNode:
        """Парсит оператор try."""
        start_token = self._advance()  # Пропускаем 'попробуй'
        
        self._expect("ДВОЕТОЧИЕ", "Ожидалось ':'")
        body = self._parse_block()
        
        except_clauses = []
        finally_body = []
        
        while self._match("КРОМЕ"):
            self._advance()
            
            # Тип исключения
            exc_type = None
            exc_name = None
            
            if self._match("ИДЕНТИФИКАТОР"):
                exc_type = self._advance().value
                
                if self._match("КАК"):
                    self._advance()
                    exc_name_token = self._expect("ИДЕНТИФИКАТОР")
                    if exc_name_token:
                        exc_name = exc_name_token.value
            
            self._expect("ДВОЕТОЧИЕ", "Ожидалось ':'")
            except_body = self._parse_block()
            except_clauses.append((exc_type, exc_name, except_body))
        
        if self._match("НАКОНЕЦ"):
            self._advance()
            self._expect("ДВОЕТОЧИЕ", "Ожидалось ':'")
            finally_body = self._parse_block()
        
        return ASTNode(
            node_type=NodeType.TRY_STMT,
            attributes={
                "body": body,
                "except_clauses": except_clauses,
                "finally_body": finally_body
            },
            line=start_token.line if start_token else 0,
            column=start_token.column if start_token else 0
        )
    
    def _parse_with_stmt(self) -> ASTNode:
        """Парсит оператор with."""
        start_token = self._advance()  # Пропускаем 'с'
        
        context_expr = self._parse_expression()
        
        alias = None
        if self._match("КАК"):
            self._advance()
            alias_token = self._expect("ИДЕНТИФИКАТОР")
            if alias_token:
                alias = alias_token.value
        
        self._expect("ДВОЕТОЧИЕ", "Ожидалось ':'")
        body = self._parse_block()
        
        return ASTNode(
            node_type=NodeType.WITH_STMT,
            attributes={
                "context_expr": context_expr,
                "alias": alias,
                "body": body
            },
            line=start_token.line if start_token else 0,
            column=start_token.column if start_token else 0
        )
    
    def _parse_assignment_or_expr(self) -> ASTNode:
        """Парсит присваивание или выражение."""
        left = self._parse_primary()
        
        if self._match("РАВНО"):
            self._advance()
            right = self._parse_expression()
            
            return ASTNode(
                node_type=NodeType.ASSIGNMENT,
                children=[left, right],
                line=left.line,
                column=left.column
            )
        elif self._match("ПЛЮС_РАВНО", "МИНУС_РАВНО", "ЗВЕЗДОЧКА_РАВНО", "СЛЕШ_РАВНО"):
            op_token = self._advance()
            right = self._parse_expression()
            
            return ASTNode(
                node_type=NodeType.AUGMENTED_ASSIGN,
                children=[left, right],
                attributes={"operator": op_token.type},
                line=left.line,
                column=left.column
            )
        else:
            # Это просто выражение как оператор
            return ASTNode(
                node_type=NodeType.EXPRESSION_STMT,
                children=[left],
                line=left.line,
                column=left.column
            )
    
    def _parse_expression_stmt(self) -> ASTNode:
        """Парсит выражение как оператор."""
        expr = self._parse_expression()
        
        return ASTNode(
            node_type=NodeType.EXPRESSION_STMT,
            children=[expr],
            line=expr.line if expr else 0,
            column=expr.column if expr else 0
        )
    
    def _parse_expression(self) -> Optional[ASTNode]:
        """Парсит выражение."""
        return self._parse_or_expr()
    
    def _parse_or_expr(self) -> Optional[ASTNode]:
        """Парсит OR выражение."""
        left = self._parse_and_expr()
        
        while self._match("ИЛИ"):
            op_token = self._advance()
            right = self._parse_and_expr()
            left = BinaryOpNode(operator="or", left=left, right=right)
        
        return left
    
    def _parse_and_expr(self) -> Optional[ASTNode]:
        """Парсит AND выражение."""
        left = self._parse_not_expr()
        
        while self._match("И"):
            op_token = self._advance()
            right = self._parse_not_expr()
            left = BinaryOpNode(operator="and", left=left, right=right)
        
        return left
    
    def _parse_not_expr(self) -> Optional[ASTNode]:
        """Парсит NOT выражение."""
        if self._match("НЕ"):
            op_token = self._advance()
            operand = self._parse_not_expr()
            return ASTNode(
                node_type=NodeType.UNARY_OP,
                children=[operand],
                attributes={"operator": "not"},
                line=op_token.line,
                column=op_token.column
            )
        
        return self._parse_comparison()
    
    def _parse_comparison(self) -> Optional[ASTNode]:
        """Парсит сравнение."""
        left = self._parse_additive()
        
        comparison_ops = {
            "РАВНО_РАВНО": "==",
            "НЕ_РАВНО": "!=",
            "МЕНЬШЕ": "<",
            "БОЛЬШЕ": ">",
            "МЕНЬШЕ_РАВНО": "<=",
            "БОЛЬШЕ_РАВНО": ">=",
        }
        
        while True:
            op_type = None
            for token_type, op_str in comparison_ops.items():
                if self._match(token_type):
                    op_type = (token_type, op_str)
                    break
            
            if not op_type:
                break
            
            self._advance()
            right = self._parse_additive()
            left = BinaryOpNode(operator=op_type[1], left=left, right=right)
        
        return left
    
    def _parse_additive(self) -> Optional[ASTNode]:
        """Парсит аддитивные операции."""
        left = self._parse_multiplicative()
        
        while self._match("ПЛЮС", "МИНУС"):
            op_token = self._advance()
            op = "+" if op_token.type == "ПЛЮС" else "-"
            right = self._parse_multiplicative()
            left = BinaryOpNode(operator=op, left=left, right=right)
        
        return left
    
    def _parse_multiplicative(self) -> Optional[ASTNode]:
        """Парсит мультипликативные операции."""
        left = self._parse_unary()
        
        while self._match("ЗВЕЗДОЧКА", "СЛЕШ", "ДВОЙНОЙ_СЛЕШ", "ПРОЦЕНТ"):
            op_token = self._advance()
            op_map = {
                "ЗВЕЗДОЧКА": "*",
                "СЛЕШ": "/",
                "ДВОЙНОЙ_СЛЕШ": "//",
                "ПРОЦЕНТ": "%"
            }
            op = op_map.get(op_token.type, op_token.type)
            right = self._parse_unary()
            left = BinaryOpNode(operator=op, left=left, right=right)
        
        return left
    
    def _parse_unary(self) -> Optional[ASTNode]:
        """Парсит унарные операции."""
        if self._match("МИНУС", "ПЛЮС", "НЕ"):
            op_token = self._advance()
            operand = self._parse_unary()
            op_map = {"МИНУС": "-", "ПЛЮС": "+", "НЕ": "not"}
            op = op_map.get(op_token.type, op_token.type)
            
            return ASTNode(
                node_type=NodeType.UNARY_OP,
                children=[operand],
                attributes={"operator": op},
                line=op_token.line,
                column=op_token.column
            )
        
        return self._parse_primary()
    
    def _parse_primary(self) -> Optional[ASTNode]:
        """Парсит первичные выражения."""
        token = self._current_token()
        
        if token is None:
            return None
        
        if token.type == "ЧИСЛО":
            self._advance()
            return NumberNode(value=token.value, line=token.line, column=token.column)
        
        elif token.type == "СТРОКА":
            self._advance()
            return StringNode(value=token.value, line=token.line, column=token.column)
        
        elif token.type == "ИСТИНА":
            self._advance()
            return ASTNode(
                node_type=NodeType.BOOLEAN,
                attributes={"value": True},
                line=token.line,
                column=token.column
            )
        
        elif token.type == "ЛОЖЬ":
            self._advance()
            return ASTNode(
                node_type=NodeType.BOOLEAN,
                attributes={"value": False},
                line=token.line,
                column=token.column
            )
        
        elif token.type == "НИЧТО":
            self._advance()
            return ASTNode(
                node_type=NodeType.NONE,
                line=token.line,
                column=token.column
            )
        
        elif token.type == "ИДЕНТИФИКАТОР":
            self._advance()
            identifier = IdentifierNode(name=token.value, line=token.line, column=token.column)
            
            # Проверяем вызов функции или доступ к атрибуту
            return self._parse_trailer(identifier)
        
        elif token.type == "ЛЕВАЯ_СКОБКА":
            self._advance()
            expr = self._parse_expression()
            self._expect("ПРАВАЯ_СКОБКА", "Ожидалась ')'")
            return self._parse_trailer(expr)
        
        elif token.type == "ЛЕВАЯ_КВАДРАТНАЯ":
            return self._parse_list_or_subscript()
        
        elif token.type == "ЛЕВАЯ_ФИГУРНАЯ":
            return self._parse_dict_or_set()
        
        else:
            self._error(f"Неожиданный токен: {token.type}")
            self._advance()
            return None
    
    def _parse_trailer(self, left: ASTNode) -> ASTNode:
        """Парсит трейлеры (вызов, индекс, атрибут)."""
        while True:
            if self._match("ЛЕВАЯ_СКОБКА"):
                # Вызов функции
                self._advance()
                args, kwargs = self._parse_arguments()
                self._expect("ПРАВАЯ_СКОБКА", "Ожидалась ')'")
                left = CallNode(func=left, args=args, kwargs=kwargs)
            
            elif self._match("ТОЧКА"):
                # Доступ к атрибуту
                self._advance()
                attr_token = self._expect("ИДЕНТИФИКАТОР", "Ожидалось имя атрибута")
                left = ASTNode(
                    node_type=NodeType.ATTRIBUTE,
                    children=[left],
                    attributes={"name": attr_token.value if attr_token else ""},
                    line=left.line,
                    column=left.column
                )
            
            elif self._match("ЛЕВАЯ_КВАДРАТНАЯ"):
                # Индексация
                self._advance()
                index = self._parse_expression()
                self._expect("ПРАВАЯ_КВАДРАТНАЯ", "Ожидалась ']'")
                left = ASTNode(
                    node_type=NodeType.SUBSCRIPT,
                    children=[left, index],
                    line=left.line,
                    column=left.column
                )
            
            else:
                break
        
        return left
    
    def _parse_arguments(self) -> tuple:
        """Парсит аргументы вызова функции."""
        args = []
        kwargs = {}
        
        if self._match("ПРАВАЯ_СКОБКА"):
            return args, kwargs
        
        while True:
            # Проверяем именованный аргумент
            if self._match("ИДЕНТИФИКАТОР") and self._peek_token() and self._peek_token().type == "РАВНО":
                name = self._advance().value
                self._advance()  # Пропускаем '='
                value = self._parse_expression()
                kwargs[name] = value
            else:
                arg = self._parse_expression()
                if arg:
                    args.append(arg)
            
            if self._match("ЗАПЯТАЯ"):
                self._advance()
            else:
                break
        
        return args, kwargs
    
    def _parse_list_or_subscript(self) -> ASTNode:
        """Парсит список или subscript."""
        start_token = self._advance()  # Пропускаем '['
        
        if self._match("ПРАВАЯ_КВАДРАТНАЯ"):
            self._advance()
            return ASTNode(
                node_type=NodeType.LIST,
                children=[],
                line=start_token.line,
                column=start_token.column
            )
        
        elements = []
        while True:
            elem = self._parse_expression()
            if elem:
                elements.append(elem)
            
            if self._match("ЗАПЯТАЯ"):
                self._advance()
            else:
                break
        
        self._expect("ПРАВАЯ_КВАДРАТНАЯ", "Ожидалась ']'")
        
        return ASTNode(
            node_type=NodeType.LIST,
            children=elements,
            line=start_token.line,
            column=start_token.column
        )
    
    def _parse_dict_or_set(self) -> ASTNode:
        """Парсит словарь или множество."""
        start_token = self._advance()  # Пропускаем '{'
        
        if self._match("ПРАВАЯ_ФИГУРНАЯ"):
            self._advance()
            return ASTNode(
                node_type=NodeType.DICT,
                children=[],
                line=start_token.line,
                column=start_token.column
            )
        
        # Проверяем первый элемент на наличие ':'
        first_elem = self._parse_expression()
        
        if self._match("ДВОЕТОЧИЕ"):
            # Это словарь
            self._advance()
            first_value = self._parse_expression()
            
            items = [(first_elem, first_value)]
            
            while self._match("ЗАПЯТАЯ"):
                self._advance()
                if self._match("ПРАВАЯ_ФИГУРНАЯ"):
                    break
                key = self._parse_expression()
                self._expect("ДВОЕТОЧИЕ", "Ожидалось ':'")
                value = self._parse_expression()
                items.append((key, value))
            
            self._expect("ПРАВАЯ_ФИГУРНАЯ", "Ожидалась '}'")
            
            return ASTNode(
                node_type=NodeType.DICT,
                children=[item for pair in items for item in pair],
                line=start_token.line,
                column=start_token.column
            )
        else:
            # Это множество
            elements = [first_elem]
            
            while self._match("ЗАПЯТАЯ"):
                self._advance()
                if self._match("ПРАВАЯ_ФИГУРНАЯ"):
                    break
                elem = self._parse_expression()
                if elem:
                    elements.append(elem)
            
            self._expect("ПРАВАЯ_ФИГУРНАЯ", "Ожидалась '}'")
            
            return ASTNode(
                node_type=NodeType.SET,
                children=elements,
                line=start_token.line,
                column=start_token.column
            )
    
    def _parse_class_def(self) -> ASTNode:
        """Парсит объявление класса."""
        start_token = self._advance()  # Пропускаем 'класс'
        
        name_token = self._expect("ИДЕНТИФИКАТОР", "Ожидалось имя класса")
        name = name_token.value if name_token else ""
        
        # Базовые классы
        bases = []
        if self._match("ЛЕВАЯ_СКОБКА"):
            self._advance()
            if not self._match("ПРАВАЯ_СКОБКА"):
                while True:
                    base_token = self._expect("ИДЕНТИФИКАТОР", "Ожидалось имя базового класса")
                    if base_token:
                        bases.append(base_token.value)
                    if self._match("ЗАПЯТАЯ"):
                        self._advance()
                    else:
                        break
            self._expect("ПРАВАЯ_СКОБКА", "Ожидалась ')'")
        
        self._expect("ДВОЕТОЧИЕ", "Ожидалось ':'")
        body = self._parse_block()
        
        return ASTNode(
            node_type=NodeType.CLASS_DEF,
            attributes={"name": name, "bases": bases, "body": body},
            line=start_token.line,
            column=start_token.column
        )


# =============================================================================
# ФАБРИКА ПАРСЕРОВ
# =============================================================================

def create_parser() -> Parser:
    """Создает экземпляр парсера."""
    return Parser()


# =============================================================================
# CLI ИНТЕРФЕЙС
# =============================================================================

if __name__ == "__main__":
    import sys
    
    print("Русский Питон Парсер v0.2.3")
    print("=" * 50)
    
    if len(sys.argv) > 1:
        filepath = Path(sys.argv[1])
        parser = create_parser()
        
        try:
            ast = parser.parse_file(filepath)
            errors = parser.get_errors()
            
            print(f"\nФайл: {filepath}")
            print(f"Ошибок: {len(errors)}")
            
            if errors:
                print("\nОшибки:")
                for error in errors:
                    print(f"  ❌ {error}")
            
            print(f"\nAST ({ast.to_dict()})")
                
        except Exception as e:
            print(f"Ошибка: {e}")
    else:
        # Демо режим
        demo_code = """
функция привет(имя):
    печать(f"Привет, {имя}!")

привет("Мир")
"""
        print("\nДемо код:")
        print(demo_code)
        
        from frontend.tokenizer import create_tokenizer
        
        tokenizer = create_tokenizer()
        tokens = list(tokenizer.tokenize(demo_code))
        
        parser = create_parser()
        ast = parser.parse(iter(tokens))
        
        print(f"\nAST: {ast.to_dict()}")
