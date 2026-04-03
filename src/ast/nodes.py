"""
Абстрактное синтаксическое дерево (AST) для языка Русский Питон
Версия 0.1.0

Определяет все узлы AST для представления программ на русском языке:
- Модули и объявления
- Функции и классы
- Выражения и операторы
- Управляющие конструкции
- Литералы и переменные
"""

from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from typing import List, Optional, Any, Dict, Union, Tuple
from enum import Enum, auto


class ASTNodeType(Enum):
    """Типы узлов AST"""
    # Программные единицы
    MODULE = auto()
    PROGRAM = auto()
    
    # Объявления
    FUNCTION_DECL = auto()
    CLASS_DECL = auto()
    VARIABLE_DECL = auto()
    IMPORT_DECL = auto()
    FROM_IMPORT_DECL = auto()
    
    # Операторы
    EXPRESSION_STMT = auto()
    ASSIGNMENT = auto()
    AUGMENTED_ASSIGN = auto()
    IF_STMT = auto()
    WHILE_STMT = auto()
    FOR_STMT = auto()
    RETURN_STMT = auto()
    BREAK_STMT = auto()
    CONTINUE_STMT = auto()
    PASS_STMT = auto()
    PRINT_STMT = auto()
    INPUT_STMT = auto()
    
    # Выражения
    BINARY_OP = auto()
    UNARY_OP = auto()
    CALL = auto()
    ATTRIBUTE_ACCESS = auto()
    SUBSCRIPT = auto()
    SLICE = auto()
    
    # Литералы
    NUMBER_LITERAL = auto()
    STRING_LITERAL = auto()
    BOOLEAN_LITERAL = auto()
    NONE_LITERAL = auto()
    LIST_LITERAL = auto()
    TUPLE_LITERAL = auto()
    DICT_LITERAL = auto()
    SET_LITERAL = auto()
    
    # Идентификаторы
    IDENTIFIER = auto()
    NAME = auto()
    
    # Лямбда и комприхеншены
    LAMBDA = auto()
    LIST_COMPREHENSION = auto()
    DICT_COMPREHENSION = auto()
    SET_COMPREHENSION = auto()
    
    # Классы и ООП
    METHOD_DECL = auto()
    CONSTRUCTOR = auto()
    SUPER_CALL = auto()
    INSTANCE_CREATE = auto()
    
    # Исключения
    TRY_STMT = auto()
    EXCEPT_CLAUSE = auto()
    FINALLY_CLAUSE = auto()
    RAISE_STMT = auto()
    ASSERT_STMT = auto()
    
    # Контекстные менеджеры
    WITH_STMT = auto()
    
    # Декораторы
    DECORATOR = auto()
    DECORATED = auto()


@dataclass
class ASTNode(ABC):
    """Базовый класс для всех узлов AST"""
    node_type: ASTNodeType
    line: int = 0
    column: int = 0
    source_file: str = ""
    children: List['ASTNode'] = field(default_factory=list)
    
    @abstractmethod
    def accept(self, visitor: 'ASTVisitor') -> Any:
        """Принятие посетителя для обхода дерева"""
        pass
    
    def add_child(self, child: 'ASTNode'):
        """Добавление дочернего узла"""
        self.children.append(child)
    
    def get_children(self) -> List['ASTNode']:
        """Получение дочерних узлов"""
        return self.children
    
    def traverse(self, callback):
        """Рекурсивный обход дерева"""
        callback(self)
        for child in self.children:
            child.traverse(callback)
    
    def __str__(self) -> str:
        return f"{self.node_type.name}(line={self.line})"


# ============================================================================
# ПРОГРАММНЫЕ ЕДИНИЦЫ
# ============================================================================

@dataclass
class Module(ASTNode):
    """Корневой узел модуля"""
    node_type: ASTNodeType = field(init=False, default=ASTNodeType.MODULE)
    name: str = ""
    docstring: Optional[str] = None
    body: List[ASTNode] = field(default_factory=list)
    imports: List['ImportDecl'] = field(default_factory=list)
    functions: List['FunctionDecl'] = field(default_factory=list)
    classes: List['ClassDecl'] = field(default_factory=list)
    variables: List['VariableDecl'] = field(default_factory=list)
    
    def accept(self, visitor: 'ASTVisitor') -> Any:
        return visitor.visit_module(self)
    
    def add_statement(self, stmt: ASTNode):
        """Добавление оператора в тело модуля"""
        self.body.append(stmt)
        if isinstance(stmt, FunctionDecl):
            self.functions.append(stmt)
        elif isinstance(stmt, ClassDecl):
            self.classes.append(stmt)
        elif isinstance(stmt, VariableDecl):
            self.variables.append(stmt)
        elif isinstance(stmt, (ImportDecl, FromImportDecl)):
            self.imports.append(stmt)


@dataclass
class Program(ASTNode):
    """Узел программы (может содержать несколько модулей)"""
    modules: List[Module] = field(default_factory=list)
    main_module: Optional[Module] = None
    
    node_type: ASTNodeType = field(init=False, default=ASTNodeType.FUNCTION_DECL)
    
    def __post_init__(self):
        pass  # node_type уже установлен через field
        self.node_type = ASTNodeType.PROGRAM
    
    def accept(self, visitor: 'ASTVisitor') -> Any:
        return visitor.visit_program(self)
    
    def add_module(self, module: Module):
        """Добавление модуля в программу"""
        self.modules.append(module)
        if self.main_module is None:
            self.main_module = module


# ============================================================================
# ОБЪЯВЛЕНИЯ
# ============================================================================

@dataclass
class FunctionDecl(ASTNode):
    """Объявление функции"""
    name: str = ""
    parameters: List['Parameter'] = field(default_factory=list)
    return_type: Optional[str] = None
    body: List[ASTNode] = field(default_factory=list)
    decorators: List['Decorator'] = field(default_factory=list)
    is_async: bool = False
    docstring: Optional[str] = None
    
    node_type: ASTNodeType = field(init=False, default=ASTNodeType.FUNCTION_DECL)
    
    def __post_init__(self):
        pass  # node_type уже установлен через field
        self.node_type = ASTNodeType.FUNCTION_DECL
    
    def accept(self, visitor: 'ASTVisitor') -> Any:
        return visitor.visit_function_decl(self)
    
    def add_parameter(self, param: 'Parameter'):
        """Добавление параметра"""
        self.parameters.append(param)
    
    def add_statement(self, stmt: ASTNode):
        """Добавление оператора в тело функции"""
        self.body.append(stmt)


@dataclass
class Parameter(ASTNode):
    """Параметр функции"""
    name: str = ""
    param_type: Optional[str] = None
    default_value: Optional[ASTNode] = None
    is_vararg: bool = False  # *args
    is_kwarg: bool = False   # **kwargs
    
    node_type: ASTNodeType = field(init=False, default=ASTNodeType.FUNCTION_DECL)
    
    def __post_init__(self):
        pass  # node_type уже установлен через field
        self.node_type = ASTNodeType.NAME
    
    def accept(self, visitor: 'ASTVisitor') -> Any:
        return visitor.visit_parameter(self)


@dataclass
class ClassDecl(ASTNode):
    """Объявление класса"""
    name: str = ""
    base_classes: List[ASTNode] = field(default_factory=list)
    body: List[ASTNode] = field(default_factory=list)
    decorators: List['Decorator'] = field(default_factory=list)
    docstring: Optional[str] = None
    
    node_type: ASTNodeType = field(init=False, default=ASTNodeType.FUNCTION_DECL)
    
    def __post_init__(self):
        pass  # node_type уже установлен через field
        self.node_type = ASTNodeType.CLASS_DECL
    
    def accept(self, visitor: 'ASTVisitor') -> Any:
        return visitor.visit_class_decl(self)
    
    def add_base_class(self, base: ASTNode):
        """Добавление базового класса"""
        self.base_classes.append(base)
    
    def add_member(self, member: ASTNode):
        """Добавление члена класса (метод или атрибут)"""
        self.body.append(member)


@dataclass
class VariableDecl(ASTNode):
    """Объявление переменной"""
    name: str = ""
    var_type: Optional[str] = None
    initial_value: Optional[ASTNode] = None
    is_constant: bool = False
    is_global: bool = False
    is_nonlocal: bool = False
    
    node_type: ASTNodeType = field(init=False, default=ASTNodeType.FUNCTION_DECL)
    
    def __post_init__(self):
        pass  # node_type уже установлен через field
        self.node_type = ASTNodeType.VARIABLE_DECL
    
    def accept(self, visitor: 'ASTVisitor') -> Any:
        return visitor.visit_variable_decl(self)


@dataclass
class ImportDecl(ASTNode):
    """Оператор импорта: импорт модуль"""
    module_name: str = ""
    alias: Optional[str] = None
    
    node_type: ASTNodeType = field(init=False, default=ASTNodeType.FUNCTION_DECL)
    
    def __post_init__(self):
        pass  # node_type уже установлен через field
        self.node_type = ASTNodeType.IMPORT_DECL
    
    def accept(self, visitor: 'ASTVisitor') -> Any:
        return visitor.visit_import_decl(self)


@dataclass
class FromImportDecl(ASTNode):
    """Оператор импорта: из модуль импорт имя"""
    module_name: str = ""
    names: List[Tuple[str, Optional[str]]] = field(default_factory=list)  # (имя, псевдоним)
    is_star: bool = False
    
    node_type: ASTNodeType = field(init=False, default=ASTNodeType.FUNCTION_DECL)
    
    def __post_init__(self):
        pass  # node_type уже установлен через field
        self.node_type = ASTNodeType.FROM_IMPORT_DECL
    
    def accept(self, visitor: 'ASTVisitor') -> Any:
        return visitor.visit_from_import_decl(self)
    
    def add_name(self, name: str, alias: Optional[str] = None):
        """Добавление импортируемого имени"""
        self.names.append((name, alias))


# ============================================================================
# ОПЕРАТОРЫ
# ============================================================================

@dataclass
class ExpressionStmt(ASTNode):
    """Оператор-выражение"""
    expression: ASTNode = None
    
    node_type: ASTNodeType = field(init=False, default=ASTNodeType.FUNCTION_DECL)
    
    def __post_init__(self):
        pass  # node_type уже установлен через field
        self.node_type = ASTNodeType.EXPRESSION_STMT
    
    def accept(self, visitor: 'ASTVisitor') -> Any:
        return visitor.visit_expression_stmt(self)


@dataclass
class Assignment(ASTNode):
    """Оператор присваивания"""
    target: ASTNode = None
    value: ASTNode = None
    annotation: Optional[str] = None
    
    node_type: ASTNodeType = field(init=False, default=ASTNodeType.FUNCTION_DECL)
    
    def __post_init__(self):
        pass  # node_type уже установлен через field
        self.node_type = ASTNodeType.ASSIGNMENT
    
    def accept(self, visitor: 'ASTVisitor') -> Any:
        return visitor.visit_assignment(self)


@dataclass
class AugmentedAssign(ASTNode):
    """Составное присваивание (+=, -=, *=, и т.д.)"""
    target: ASTNode = None
    value: ASTNode = None
    operator: str = "+="
    
    node_type: ASTNodeType = field(init=False, default=ASTNodeType.FUNCTION_DECL)
    
    def __post_init__(self):
        pass  # node_type уже установлен через field
        self.node_type = ASTNodeType.AUGMENTED_ASSIGN
    
    def accept(self, visitor: 'ASTVisitor') -> Any:
        return visitor.visit_augmented_assign(self)


@dataclass
class IfStmt(ASTNode):
    """Условный оператор если/иначе"""
    condition: ASTNode = None
    then_branch: List[ASTNode] = field(default_factory=list)
    else_branch: List[ASTNode] = field(default_factory=list)
    elif_branches: List[Tuple[ASTNode, List[ASTNode]]] = field(default_factory=list)
    
    node_type: ASTNodeType = field(init=False, default=ASTNodeType.FUNCTION_DECL)
    
    def __post_init__(self):
        pass  # node_type уже установлен через field
        self.node_type = ASTNodeType.IF_STMT
    
    def accept(self, visitor: 'ASTVisitor') -> Any:
        return visitor.visit_if_stmt(self)
    
    def add_elif(self, condition: ASTNode, body: List[ASTNode]):
        """Добавление ветви иначе-если"""
        self.elif_branches.append((condition, body))


@dataclass
class WhileStmt(ASTNode):
    """Цикл пока"""
    condition: ASTNode = None
    body: List[ASTNode] = field(default_factory=list)
    else_branch: List[ASTNode] = field(default_factory=list)
    
    node_type: ASTNodeType = field(init=False, default=ASTNodeType.FUNCTION_DECL)
    
    def __post_init__(self):
        pass  # node_type уже установлен через field
        self.node_type = ASTNodeType.WHILE_STMT
    
    def accept(self, visitor: 'ASTVisitor') -> Any:
        return visitor.visit_while_stmt(self)


@dataclass
class ForStmt(ASTNode):
    """Цикл для"""
    target: ASTNode = None
    iterable: ASTNode = None
    body: List[ASTNode] = field(default_factory=list)
    else_branch: List[ASTNode] = field(default_factory=list)
    is_async: bool = False
    
    node_type: ASTNodeType = field(init=False, default=ASTNodeType.FUNCTION_DECL)
    
    def __post_init__(self):
        pass  # node_type уже установлен через field
        self.node_type = ASTNodeType.FOR_STMT
    
    def accept(self, visitor: 'ASTVisitor') -> Any:
        return visitor.visit_for_stmt(self)


@dataclass
class ReturnStmt(ASTNode):
    """Оператор вернуть"""
    value: Optional[ASTNode] = None
    
    node_type: ASTNodeType = field(init=False, default=ASTNodeType.FUNCTION_DECL)
    
    def __post_init__(self):
        pass  # node_type уже установлен через field
        self.node_type = ASTNodeType.RETURN_STMT
    
    def accept(self, visitor: 'ASTVisitor') -> Any:
        return visitor.visit_return_stmt(self)


@dataclass
class BreakStmt(ASTNode):
    """Оператор прервать"""
    
    node_type: ASTNodeType = field(init=False, default=ASTNodeType.FUNCTION_DECL)
    
    def __post_init__(self):
        pass  # node_type уже установлен через field
        self.node_type = ASTNodeType.BREAK_STMT
    
    def accept(self, visitor: 'ASTVisitor') -> Any:
        return visitor.visit_break_stmt(self)


@dataclass
class ContinueStmt(ASTNode):
    """Оператор продолжить"""
    
    node_type: ASTNodeType = field(init=False, default=ASTNodeType.FUNCTION_DECL)
    
    def __post_init__(self):
        pass  # node_type уже установлен через field
        self.node_type = ASTNodeType.CONTINUE_STMT
    
    def accept(self, visitor: 'ASTVisitor') -> Any:
        return visitor.visit_continue_stmt(self)


@dataclass
class PassStmt(ASTNode):
    """Оператор ничего (pass)"""
    
    node_type: ASTNodeType = field(init=False, default=ASTNodeType.FUNCTION_DECL)
    
    def __post_init__(self):
        pass  # node_type уже установлен через field
        self.node_type = ASTNodeType.PASS_STMT
    
    def accept(self, visitor: 'ASTVisitor') -> Any:
        return visitor.visit_pass_stmt(self)


@dataclass
class PrintStmt(ASTNode):
    """Оператор печать"""
    arguments: List[ASTNode] = field(default_factory=list)
    separator: str = " "
    end: str = "\n"
    file: Optional[ASTNode] = None
    
    node_type: ASTNodeType = field(init=False, default=ASTNodeType.FUNCTION_DECL)
    
    def __post_init__(self):
        pass  # node_type уже установлен через field
        self.node_type = ASTNodeType.PRINT_STMT
    
    def accept(self, visitor: 'ASTVisitor') -> Any:
        return visitor.visit_print_stmt(self)
    
    def add_argument(self, arg: ASTNode):
        """Добавление аргумента печати"""
        self.arguments.append(arg)


@dataclass
class InputStmt(ASTNode):
    """Оператор ввод"""
    prompt: Optional[ASTNode] = None
    target: Optional[str] = None
    
    node_type: ASTNodeType = field(init=False, default=ASTNodeType.FUNCTION_DECL)
    
    def __post_init__(self):
        pass  # node_type уже установлен через field
        self.node_type = ASTNodeType.INPUT_STMT
    
    def accept(self, visitor: 'ASTVisitor') -> Any:
        return visitor.visit_input_stmt(self)


# ============================================================================
# ВЫРАЖЕНИЯ
# ============================================================================

@dataclass
class BinaryOp(ASTNode):
    """Бинарная операция"""
    left: ASTNode = None
    right: ASTNode = None
    operator: str = "+"
    
    node_type: ASTNodeType = field(init=False, default=ASTNodeType.FUNCTION_DECL)
    
    def __post_init__(self):
        pass  # node_type уже установлен через field
        self.node_type = ASTNodeType.BINARY_OP
    
    def accept(self, visitor: 'ASTVisitor') -> Any:
        return visitor.visit_binary_op(self)


@dataclass
class UnaryOp(ASTNode):
    """Унарная операция"""
    operand: ASTNode = None
    operator: str = "-"
    
    node_type: ASTNodeType = field(init=False, default=ASTNodeType.FUNCTION_DECL)
    
    def __post_init__(self):
        pass  # node_type уже установлен через field
        self.node_type = ASTNodeType.UNARY_OP
    
    def accept(self, visitor: 'ASTVisitor') -> Any:
        return visitor.visit_unary_op(self)


@dataclass
class Call(ASTNode):
    """Вызов функции"""
    function: ASTNode = None
    arguments: List[ASTNode] = field(default_factory=list)
    keyword_args: Dict[str, ASTNode] = field(default_factory=dict)
    
    node_type: ASTNodeType = field(init=False, default=ASTNodeType.FUNCTION_DECL)
    
    def __post_init__(self):
        pass  # node_type уже установлен через field
        self.node_type = ASTNodeType.CALL
    
    def accept(self, visitor: 'ASTVisitor') -> Any:
        return visitor.visit_call(self)
    
    def add_argument(self, arg: ASTNode):
        """Добавление позиционного аргумента"""
        self.arguments.append(arg)
    
    def add_keyword_argument(self, name: str, value: ASTNode):
        """Добавление именованного аргумента"""
        self.keyword_args[name] = value


@dataclass
class AttributeAccess(ASTNode):
    """Доступ к атрибуту объекта"""
    object: ASTNode = None
    attribute: str = ""
    
    node_type: ASTNodeType = field(init=False, default=ASTNodeType.FUNCTION_DECL)
    
    def __post_init__(self):
        pass  # node_type уже установлен через field
        self.node_type = ASTNodeType.ATTRIBUTE_ACCESS
    
    def accept(self, visitor: 'ASTVisitor') -> Any:
        return visitor.visit_attribute_access(self)


@dataclass
class Subscript(ASTNode):
    """Индексация (доступ по индексу)"""
    value: ASTNode = None
    index: ASTNode = None
    
    node_type: ASTNodeType = field(init=False, default=ASTNodeType.FUNCTION_DECL)
    
    def __post_init__(self):
        pass  # node_type уже установлен через field
        self.node_type = ASTNodeType.SUBSCRIPT
    
    def accept(self, visitor: 'ASTVisitor') -> Any:
        return visitor.visit_subscript(self)


@dataclass
class Slice(ASTNode):
    """Срез"""
    start: Optional[ASTNode] = None
    stop: Optional[ASTNode] = None
    step: Optional[ASTNode] = None
    
    node_type: ASTNodeType = field(init=False, default=ASTNodeType.FUNCTION_DECL)
    
    def __post_init__(self):
        pass  # node_type уже установлен через field
        self.node_type = ASTNodeType.SLICE
    
    def accept(self, visitor: 'ASTVisitor') -> Any:
        return visitor.visit_slice(self)


# ============================================================================
# ЛИТЕРАЛЫ
# ============================================================================

@dataclass
class NumberLiteral(ASTNode):
    """Числовой литерал"""
    value: Union[int, float] = 0
    
    node_type: ASTNodeType = field(init=False, default=ASTNodeType.FUNCTION_DECL)
    
    def __post_init__(self):
        pass  # node_type уже установлен через field
        self.node_type = ASTNodeType.NUMBER_LITERAL
    
    def accept(self, visitor: 'ASTVisitor') -> Any:
        return visitor.visit_number_literal(self)


@dataclass
class StringLiteral(ASTNode):
    """Строковый литерал"""
    value: str = ""
    prefix: str = ""  # r, f, b и т.д.
    
    node_type: ASTNodeType = field(init=False, default=ASTNodeType.FUNCTION_DECL)
    
    def __post_init__(self):
        pass  # node_type уже установлен через field
        self.node_type = ASTNodeType.STRING_LITERAL
    
    def accept(self, visitor: 'ASTVisitor') -> Any:
        return visitor.visit_string_literal(self)


@dataclass
class BooleanLiteral(ASTNode):
    """Булев литерал"""
    value: bool = False
    
    node_type: ASTNodeType = field(init=False, default=ASTNodeType.FUNCTION_DECL)
    
    def __post_init__(self):
        pass  # node_type уже установлен через field
        self.node_type = ASTNodeType.BOOLEAN_LITERAL
    
    def accept(self, visitor: 'ASTVisitor') -> Any:
        return visitor.visit_boolean_literal(self)


@dataclass
class NoneLiteral(ASTNode):
    """Литерал Ничто"""
    
    node_type: ASTNodeType = field(init=False, default=ASTNodeType.FUNCTION_DECL)
    
    def __post_init__(self):
        pass  # node_type уже установлен через field
        self.node_type = ASTNodeType.NONE_LITERAL
    
    def accept(self, visitor: 'ASTVisitor') -> Any:
        return visitor.visit_none_literal(self)


@dataclass
class ListLiteral(ASTNode):
    """Списковый литерал"""
    elements: List[ASTNode] = field(default_factory=list)
    
    node_type: ASTNodeType = field(init=False, default=ASTNodeType.FUNCTION_DECL)
    
    def __post_init__(self):
        pass  # node_type уже установлен через field
        self.node_type = ASTNodeType.LIST_LITERAL
    
    def accept(self, visitor: 'ASTVisitor') -> Any:
        return visitor.visit_list_literal(self)
    
    def add_element(self, element: ASTNode):
        """Добавление элемента списка"""
        self.elements.append(element)


@dataclass
class TupleLiteral(ASTNode):
    """Кортежный литерал"""
    elements: List[ASTNode] = field(default_factory=list)
    
    node_type: ASTNodeType = field(init=False, default=ASTNodeType.FUNCTION_DECL)
    
    def __post_init__(self):
        pass  # node_type уже установлен через field
        self.node_type = ASTNodeType.TUPLE_LITERAL
    
    def accept(self, visitor: 'ASTVisitor') -> Any:
        return visitor.visit_tuple_literal(self)
    
    def add_element(self, element: ASTNode):
        """Добавление элемента кортежа"""
        self.elements.append(element)


@dataclass
class DictLiteral(ASTNode):
    """Словарный литерал"""
    items: List[Tuple[ASTNode, ASTNode]] = field(default_factory=list)
    
    node_type: ASTNodeType = field(init=False, default=ASTNodeType.FUNCTION_DECL)
    
    def __post_init__(self):
        pass  # node_type уже установлен через field
        self.node_type = ASTNodeType.DICT_LITERAL
    
    def accept(self, visitor: 'ASTVisitor') -> Any:
        return visitor.visit_dict_literal(self)
    
    def add_item(self, key: ASTNode, value: ASTNode):
        """Добавление пары ключ-значение"""
        self.items.append((key, value))


@dataclass
class SetLiteral(ASTNode):
    """Множественный литерал"""
    elements: List[ASTNode] = field(default_factory=list)
    
    node_type: ASTNodeType = field(init=False, default=ASTNodeType.FUNCTION_DECL)
    
    def __post_init__(self):
        pass  # node_type уже установлен через field
        self.node_type = ASTNodeType.SET_LITERAL
    
    def accept(self, visitor: 'ASTVisitor') -> Any:
        return visitor.visit_set_literal(self)
    
    def add_element(self, element: ASTNode):
        """Добавление элемента множества"""
        self.elements.append(element)


# ============================================================================
# ИДЕНТИФИКАТОРЫ
# ============================================================================

@dataclass
class Identifier(ASTNode):
    """Идентификатор (переменная, функция, класс)"""
    name: str = ""
    
    node_type: ASTNodeType = field(init=False, default=ASTNodeType.FUNCTION_DECL)
    
    def __post_init__(self):
        pass  # node_type уже установлен через field
        self.node_type = ASTNodeType.IDENTIFIER
    
    def accept(self, visitor: 'ASTVisitor') -> Any:
        return visitor.visit_identifier(self)


@dataclass
class Name(ASTNode):
    """Имя (простой идентификатор)"""
    name: str = ""
    
    node_type: ASTNodeType = field(init=False, default=ASTNodeType.FUNCTION_DECL)
    
    def __post_init__(self):
        pass  # node_type уже установлен через field
        self.node_type = ASTNodeType.NAME
    
    def accept(self, visitor: 'ASTVisitor') -> Any:
        return visitor.visit_name(self)


# ============================================================================
# ЛЯМБДА И КОМПРИХЕНШЕНЫ
# ============================================================================

@dataclass
class Lambda(ASTNode):
    """Лямбда-функция"""
    parameters: List[Parameter] = field(default_factory=list)
    body: ASTNode = None
    
    node_type: ASTNodeType = field(init=False, default=ASTNodeType.FUNCTION_DECL)
    
    def __post_init__(self):
        pass  # node_type уже установлен через field
        self.node_type = ASTNodeType.LAMBDA
    
    def accept(self, visitor: 'ASTVisitor') -> Any:
        return visitor.visit_lambda(self)


@dataclass
class ListComprehension(ASTNode):
    """Списковое включение"""
    element: ASTNode = None
    generators: List[Tuple[ASTNode, ASTNode]] = field(default_factory=list)
    conditions: List[ASTNode] = field(default_factory=list)
    
    node_type: ASTNodeType = field(init=False, default=ASTNodeType.FUNCTION_DECL)
    
    def __post_init__(self):
        pass  # node_type уже установлен через field
        self.node_type = ASTNodeType.LIST_COMPREHENSION
    
    def accept(self, visitor: 'ASTVisitor') -> Any:
        return visitor.visit_list_comprehension(self)


@dataclass
class DictComprehension(ASTNode):
    """Словарное включение"""
    key: ASTNode = None
    value: ASTNode = None
    generators: List[Tuple[ASTNode, ASTNode]] = field(default_factory=list)
    conditions: List[ASTNode] = field(default_factory=list)
    
    node_type: ASTNodeType = field(init=False, default=ASTNodeType.FUNCTION_DECL)
    
    def __post_init__(self):
        pass  # node_type уже установлен через field
        self.node_type = ASTNodeType.DICT_COMPREHENSION
    
    def accept(self, visitor: 'ASTVisitor') -> Any:
        return visitor.visit_dict_comprehension(self)


# ============================================================================
# КЛАССЫ И ООП
# ============================================================================

@dataclass
class MethodDecl(FunctionDecl):
    """Объявление метода класса"""
    is_static: bool = False
    is_class_method: bool = False
    is_abstract: bool = False
    
    node_type: ASTNodeType = field(init=False, default=ASTNodeType.FUNCTION_DECL)
    
    def __post_init__(self):
        pass  # node_type уже установлен через field
        self.node_type = ASTNodeType.METHOD_DECL


@dataclass
class Constructor(MethodDecl):
    """Конструктор класса (__init__)"""
    
    node_type: ASTNodeType = field(init=False, default=ASTNodeType.FUNCTION_DECL)
    
    def __post_init__(self):
        pass  # node_type уже установлен через field
        self.node_type = ASTNodeType.CONSTRUCTOR


@dataclass
class SuperCall(ASTNode):
    """Вызов super()"""
    arguments: List[ASTNode] = field(default_factory=list)
    
    node_type: ASTNodeType = field(init=False, default=ASTNodeType.FUNCTION_DECL)
    
    def __post_init__(self):
        pass  # node_type уже установлен через field
        self.node_type = ASTNodeType.SUPER_CALL
    
    def accept(self, visitor: 'ASTVisitor') -> Any:
        return visitor.visit_super_call(self)


@dataclass
class InstanceCreate(ASTNode):
    """Создание экземпляра класса"""
    class_name: ASTNode = None
    arguments: List[ASTNode] = field(default_factory=list)
    keyword_args: Dict[str, ASTNode] = field(default_factory=dict)
    
    node_type: ASTNodeType = field(init=False, default=ASTNodeType.FUNCTION_DECL)
    
    def __post_init__(self):
        pass  # node_type уже установлен через field
        self.node_type = ASTNodeType.INSTANCE_CREATE
    
    def accept(self, visitor: 'ASTVisitor') -> Any:
        return visitor.visit_instance_create(self)


# ============================================================================
# ИСКЛЮЧЕНИЯ
# ============================================================================

@dataclass
class TryStmt(ASTNode):
    """Оператор попытка"""
    body: List[ASTNode] = field(default_factory=list)
    except_clauses: List['ExceptClause'] = field(default_factory=list)
    finally_clause: Optional['FinallyClause'] = None
    else_branch: List[ASTNode] = field(default_factory=list)
    
    node_type: ASTNodeType = field(init=False, default=ASTNodeType.FUNCTION_DECL)
    
    def __post_init__(self):
        pass  # node_type уже установлен через field
        self.node_type = ASTNodeType.TRY_STMT
    
    def accept(self, visitor: 'ASTVisitor') -> Any:
        return visitor.visit_try_stmt(self)


@dataclass
class ExceptClause(ASTNode):
    """Ветка обработка исключений"""
    exception_type: Optional[ASTNode] = None
    exception_name: Optional[str] = None
    body: List[ASTNode] = field(default_factory=list)
    
    node_type: ASTNodeType = field(init=False, default=ASTNodeType.FUNCTION_DECL)
    
    def __post_init__(self):
        pass  # node_type уже установлен через field
        self.node_type = ASTNodeType.EXCEPT_CLAUSE
    
    def accept(self, visitor: 'ASTVisitor') -> Any:
        return visitor.visit_except_clause(self)


@dataclass
class FinallyClause(ASTNode):
    """Ветка наконец"""
    body: List[ASTNode] = field(default_factory=list)
    
    node_type: ASTNodeType = field(init=False, default=ASTNodeType.FUNCTION_DECL)
    
    def __post_init__(self):
        pass  # node_type уже установлен через field
        self.node_type = ASTNodeType.FINALLY_CLAUSE
    
    def accept(self, visitor: 'ASTVisitor') -> Any:
        return visitor.visit_finally_clause(self)


@dataclass
class RaiseStmt(ASTNode):
    """Оператор выбросить (исключение)"""
    exception: Optional[ASTNode] = None
    from_exception: Optional[ASTNode] = None
    
    node_type: ASTNodeType = field(init=False, default=ASTNodeType.FUNCTION_DECL)
    
    def __post_init__(self):
        pass  # node_type уже установлен через field
        self.node_type = ASTNodeType.RAISE_STMT
    
    def accept(self, visitor: 'ASTVisitor') -> Any:
        return visitor.visit_raise_stmt(self)


@dataclass
class AssertStmt(ASTNode):
    """Оператор утверждение"""
    condition: ASTNode = None
    message: Optional[ASTNode] = None
    
    node_type: ASTNodeType = field(init=False, default=ASTNodeType.FUNCTION_DECL)
    
    def __post_init__(self):
        pass  # node_type уже установлен через field
        self.node_type = ASTNodeType.ASSERT_STMT
    
    def accept(self, visitor: 'ASTVisitor') -> Any:
        return visitor.visit_assert_stmt(self)


# ============================================================================
# КОНТЕКСТНЫЕ МЕНЕДЖЕРЫ
# ============================================================================

@dataclass
class WithStmt(ASTNode):
    """Оператор с (контекстный менеджер)"""
    items: List[Tuple[ASTNode, Optional[str]]] = field(default_factory=list)  # (expr, var)
    body: List[ASTNode] = field(default_factory=list)
    is_async: bool = False
    
    node_type: ASTNodeType = field(init=False, default=ASTNodeType.FUNCTION_DECL)
    
    def __post_init__(self):
        pass  # node_type уже установлен через field
        self.node_type = ASTNodeType.WITH_STMT
    
    def accept(self, visitor: 'ASTVisitor') -> Any:
        return visitor.visit_with_stmt(self)


# ============================================================================
# ДЕКОРАТОРЫ
# ============================================================================

@dataclass
class Decorator(ASTNode):
    """Декоратор"""
    name: ASTNode = None
    arguments: List[ASTNode] = field(default_factory=list)
    keyword_args: Dict[str, ASTNode] = field(default_factory=dict)
    
    node_type: ASTNodeType = field(init=False, default=ASTNodeType.FUNCTION_DECL)
    
    def __post_init__(self):
        pass  # node_type уже установлен через field
        self.node_type = ASTNodeType.DECORATOR
    
    def accept(self, visitor: 'ASTVisitor') -> Any:
        return visitor.visit_decorator(self)


@dataclass
class Decorated(ASTNode):
    """Декорированный элемент"""
    decorators: List[Decorator] = field(default_factory=list)
    definition: ASTNode = None
    
    node_type: ASTNodeType = field(init=False, default=ASTNodeType.FUNCTION_DECL)
    
    def __post_init__(self):
        pass  # node_type уже установлен через field
        self.node_type = ASTNodeType.DECORATED
    
    def accept(self, visitor: 'ASTVisitor') -> Any:
        return visitor.visit_decorated(self)


# ============================================================================
# ПОСЕТИТЕЛЬ (VISITOR PATTERN)
# ============================================================================

class ASTVisitor(ABC):
    """Базовый класс посетителя AST"""
    
    @abstractmethod
    def visit_module(self, node: Module) -> Any:
        pass
    
    @abstractmethod
    def visit_program(self, node: Program) -> Any:
        pass
    
    @abstractmethod
    def visit_function_decl(self, node: FunctionDecl) -> Any:
        pass
    
    @abstractmethod
    def visit_parameter(self, node: Parameter) -> Any:
        pass
    
    @abstractmethod
    def visit_class_decl(self, node: ClassDecl) -> Any:
        pass
    
    @abstractmethod
    def visit_variable_decl(self, node: VariableDecl) -> Any:
        pass
    
    @abstractmethod
    def visit_import_decl(self, node: ImportDecl) -> Any:
        pass
    
    @abstractmethod
    def visit_from_import_decl(self, node: FromImportDecl) -> Any:
        pass
    
    @abstractmethod
    def visit_expression_stmt(self, node: ExpressionStmt) -> Any:
        pass
    
    @abstractmethod
    def visit_assignment(self, node: Assignment) -> Any:
        pass
    
    @abstractmethod
    def visit_augmented_assign(self, node: AugmentedAssign) -> Any:
        pass
    
    @abstractmethod
    def visit_if_stmt(self, node: IfStmt) -> Any:
        pass
    
    @abstractmethod
    def visit_while_stmt(self, node: WhileStmt) -> Any:
        pass
    
    @abstractmethod
    def visit_for_stmt(self, node: ForStmt) -> Any:
        pass
    
    @abstractmethod
    def visit_return_stmt(self, node: ReturnStmt) -> Any:
        pass
    
    @abstractmethod
    def visit_break_stmt(self, node: BreakStmt) -> Any:
        pass
    
    @abstractmethod
    def visit_continue_stmt(self, node: ContinueStmt) -> Any:
        pass
    
    @abstractmethod
    def visit_pass_stmt(self, node: PassStmt) -> Any:
        pass
    
    @abstractmethod
    def visit_print_stmt(self, node: PrintStmt) -> Any:
        pass
    
    @abstractmethod
    def visit_input_stmt(self, node: InputStmt) -> Any:
        pass
    
    @abstractmethod
    def visit_binary_op(self, node: BinaryOp) -> Any:
        pass
    
    @abstractmethod
    def visit_unary_op(self, node: UnaryOp) -> Any:
        pass
    
    @abstractmethod
    def visit_call(self, node: Call) -> Any:
        pass
    
    @abstractmethod
    def visit_attribute_access(self, node: AttributeAccess) -> Any:
        pass
    
    @abstractmethod
    def visit_subscript(self, node: Subscript) -> Any:
        pass
    
    @abstractmethod
    def visit_slice(self, node: Slice) -> Any:
        pass
    
    @abstractmethod
    def visit_number_literal(self, node: NumberLiteral) -> Any:
        pass
    
    @abstractmethod
    def visit_string_literal(self, node: StringLiteral) -> Any:
        pass
    
    @abstractmethod
    def visit_boolean_literal(self, node: BooleanLiteral) -> Any:
        pass
    
    @abstractmethod
    def visit_none_literal(self, node: NoneLiteral) -> Any:
        pass
    
    @abstractmethod
    def visit_list_literal(self, node: ListLiteral) -> Any:
        pass
    
    @abstractmethod
    def visit_tuple_literal(self, node: TupleLiteral) -> Any:
        pass
    
    @abstractmethod
    def visit_dict_literal(self, node: DictLiteral) -> Any:
        pass
    
    @abstractmethod
    def visit_set_literal(self, node: SetLiteral) -> Any:
        pass
    
    @abstractmethod
    def visit_identifier(self, node: Identifier) -> Any:
        pass
    
    @abstractmethod
    def visit_name(self, node: Name) -> Any:
        pass
    
    @abstractmethod
    def visit_lambda(self, node: Lambda) -> Any:
        pass
    
    @abstractmethod
    def visit_list_comprehension(self, node: ListComprehension) -> Any:
        pass
    
    @abstractmethod
    def visit_dict_comprehension(self, node: DictComprehension) -> Any:
        pass
    
    @abstractmethod
    def visit_super_call(self, node: SuperCall) -> Any:
        pass
    
    @abstractmethod
    def visit_instance_create(self, node: InstanceCreate) -> Any:
        pass
    
    @abstractmethod
    def visit_try_stmt(self, node: TryStmt) -> Any:
        pass
    
    @abstractmethod
    def visit_except_clause(self, node: ExceptClause) -> Any:
        pass
    
    @abstractmethod
    def visit_finally_clause(self, node: FinallyClause) -> Any:
        pass
    
    @abstractmethod
    def visit_raise_stmt(self, node: RaiseStmt) -> Any:
        pass
    
    @abstractmethod
    def visit_assert_stmt(self, node: AssertStmt) -> Any:
        pass
    
    @abstractmethod
    def visit_with_stmt(self, node: WithStmt) -> Any:
        pass
    
    @abstractmethod
    def visit_decorator(self, node: Decorator) -> Any:
        pass
    
    @abstractmethod
    def visit_decorated(self, node: Decorated) -> Any:
        pass


class ASTPrinter(ASTVisitor):
    """Посетитель для печати AST"""
    
    def __init__(self, indent: int = 2):
        self.indent_size = indent
        self.current_indent = 0
    
    def _indent(self) -> str:
        return " " * self.current_indent
    
    def _print_node(self, node_type: str, value: Any = None) -> str:
        result = f"{self._indent()}{node_type}"
        if value is not None:
            result += f": {repr(value)}"
        return result
    
    def visit_module(self, node: Module) -> str:
        lines = [self._print_node("Module", node.name)]
        self.current_indent += self.indent_size
        
        if node.docstring:
            lines.append(f"{self._indent()}Docstring: {repr(node.docstring)}")
        
        for stmt in node.body:
            lines.append(stmt.accept(self))
        
        self.current_indent -= self.indent_size
        return "\n".join(lines)
    
    def visit_program(self, node: Program) -> str:
        lines = [self._print_node("Program")]
        self.current_indent += self.indent_size
        
        for module in node.modules:
            lines.append(module.accept(self))
        
        self.current_indent -= self.indent_size
        return "\n".join(lines)
    
    def visit_function_decl(self, node: FunctionDecl) -> str:
        params = ", ".join(p.name for p in node.parameters)
        lines = [self._print_node("Function", f"{node.name}({params})")]
        self.current_indent += self.indent_size
        
        for param in node.parameters:
            lines.append(param.accept(self))
        
        for stmt in node.body:
            lines.append(stmt.accept(self))
        
        self.current_indent -= self.indent_size
        return "\n".join(lines)
    
    def visit_parameter(self, node: Parameter) -> str:
        return self._print_node("Parameter", node.name)
    
    def visit_class_decl(self, node: ClassDecl) -> str:
        bases = ", ".join(str(b) for b in node.base_classes) if node.base_classes else ""
        lines = [self._print_node("Class", f"{node.name}" + (f"({bases})" if bases else ""))]
        self.current_indent += self.indent_size
        
        for member in node.body:
            lines.append(member.accept(self))
        
        self.current_indent -= self.indent_size
        return "\n".join(lines)
    
    def visit_variable_decl(self, node: VariableDecl) -> str:
        return self._print_node("Variable", f"{node.name}: {node.var_type}")
    
    def visit_import_decl(self, node: ImportDecl) -> str:
        return self._print_node("Import", node.module_name)
    
    def visit_from_import_decl(self, node: FromImportDecl) -> str:
        names = ", ".join(n[0] for n in node.names)
        return self._print_node("FromImport", f"{node.module_name} import {names}")
    
    def visit_expression_stmt(self, node: ExpressionStmt) -> str:
        lines = [self._print_node("ExpressionStmt")]
        self.current_indent += self.indent_size
        lines.append(node.expression.accept(self))
        self.current_indent -= self.indent_size
        return "\n".join(lines)
    
    def visit_assignment(self, node: Assignment) -> str:
        return self._print_node("Assignment", node.target)
    
    def visit_augmented_assign(self, node: AugmentedAssign) -> str:
        return self._print_node("AugmentedAssign", f"{node.target} {node.operator}")
    
    def visit_if_stmt(self, node: IfStmt) -> str:
        lines = [self._print_node("If")]
        self.current_indent += self.indent_size
        
        lines.append(f"{self._indent()}Condition:")
        self.current_indent += self.indent_size
        lines.append(node.condition.accept(self))
        self.current_indent -= self.indent_size
        
        lines.append(f"{self._indent()}Then:")
        self.current_indent += self.indent_size
        for stmt in node.then_branch:
            lines.append(stmt.accept(self))
        self.current_indent -= self.indent_size
        
        self.current_indent -= self.indent_size
        return "\n".join(lines)
    
    def visit_while_stmt(self, node: WhileStmt) -> str:
        lines = [self._print_node("While")]
        self.current_indent += self.indent_size
        
        lines.append(f"{self._indent()}Condition:")
        self.current_indent += self.indent_size
        lines.append(node.condition.accept(self))
        self.current_indent -= self.indent_size
        
        lines.append(f"{self._indent()}Body:")
        self.current_indent += self.indent_size
        for stmt in node.body:
            lines.append(stmt.accept(self))
        self.current_indent -= self.indent_size
        
        self.current_indent -= self.indent_size
        return "\n".join(lines)
    
    def visit_for_stmt(self, node: ForStmt) -> str:
        lines = [self._print_node("For")]
        self.current_indent += self.indent_size
        lines.append(f"{self._indent()}Target: {node.target}")
        lines.append(f"{self._indent()}Iterable: {node.iterable}")
        self.current_indent -= self.indent_size
        return "\n".join(lines)
    
    def visit_return_stmt(self, node: ReturnStmt) -> str:
        return self._print_node("Return")
    
    def visit_break_stmt(self, node: BreakStmt) -> str:
        return self._print_node("Break")
    
    def visit_continue_stmt(self, node: ContinueStmt) -> str:
        return self._print_node("Continue")
    
    def visit_pass_stmt(self, node: PassStmt) -> str:
        return self._print_node("Pass")
    
    def visit_print_stmt(self, node: PrintStmt) -> str:
        return self._print_node("Print", f"{len(node.arguments)} args")
    
    def visit_input_stmt(self, node: InputStmt) -> str:
        return self._print_node("Input", node.target)
    
    def visit_binary_op(self, node: BinaryOp) -> str:
        return self._print_node("BinaryOp", node.operator)
    
    def visit_unary_op(self, node: UnaryOp) -> str:
        return self._print_node("UnaryOp", node.operator)
    
    def visit_call(self, node: Call) -> str:
        return self._print_node("Call", f"{len(node.arguments)} args")
    
    def visit_attribute_access(self, node: AttributeAccess) -> str:
        return self._print_node("Attribute", node.attribute)
    
    def visit_subscript(self, node: Subscript) -> str:
        return self._print_node("Subscript")
    
    def visit_slice(self, node: Slice) -> str:
        return self._print_node("Slice")
    
    def visit_number_literal(self, node: NumberLiteral) -> str:
        return self._print_node("Number", node.value)
    
    def visit_string_literal(self, node: StringLiteral) -> str:
        return self._print_node("String", node.value[:50] + "..." if len(node.value) > 50 else node.value)
    
    def visit_boolean_literal(self, node: BooleanLiteral) -> str:
        return self._print_node("Boolean", node.value)
    
    def visit_none_literal(self, node: NoneLiteral) -> str:
        return self._print_node("None")
    
    def visit_list_literal(self, node: ListLiteral) -> str:
        return self._print_node("List", f"{len(node.elements)} elements")
    
    def visit_tuple_literal(self, node: TupleLiteral) -> str:
        return self._print_node("Tuple", f"{len(node.elements)} elements")
    
    def visit_dict_literal(self, node: DictLiteral) -> str:
        return self._print_node("Dict", f"{len(node.items)} items")
    
    def visit_set_literal(self, node: SetLiteral) -> str:
        return self._print_node("Set", f"{len(node.elements)} elements")
    
    def visit_identifier(self, node: Identifier) -> str:
        return self._print_node("Identifier", node.name)
    
    def visit_name(self, node: Name) -> str:
        return self._print_node("Name", node.name)
    
    def visit_lambda(self, node: Lambda) -> str:
        return self._print_node("Lambda")
    
    def visit_list_comprehension(self, node: ListComprehension) -> str:
        return self._print_node("ListComprehension")
    
    def visit_dict_comprehension(self, node: DictComprehension) -> str:
        return self._print_node("DictComprehension")
    
    def visit_super_call(self, node: SuperCall) -> str:
        return self._print_node("Super")
    
    def visit_instance_create(self, node: InstanceCreate) -> str:
        return self._print_node("InstanceCreate")
    
    def visit_try_stmt(self, node: TryStmt) -> str:
        return self._print_node("Try")
    
    def visit_except_clause(self, node: ExceptClause) -> str:
        return self._print_node("Except")
    
    def visit_finally_clause(self, node: FinallyClause) -> str:
        return self._print_node("Finally")
    
    def visit_raise_stmt(self, node: RaiseStmt) -> str:
        return self._print_node("Raise")
    
    def visit_assert_stmt(self, node: AssertStmt) -> str:
        return self._print_node("Assert")
    
    def visit_with_stmt(self, node: WithStmt) -> str:
        return self._print_node("With")
    
    def visit_decorator(self, node: Decorator) -> str:
        return self._print_node("Decorator")
    
    def visit_decorated(self, node: Decorated) -> str:
        return self._print_node("Decorated")


def print_ast(node: ASTNode, indent: int = 2) -> str:
    """Удобная функция для печати AST"""
    printer = ASTPrinter(indent)
    return node.accept(printer)


if __name__ == "__main__":
    # Демо-пример создания AST
    print("=== Демонстрация AST ===\n")
    
    # Создаем простую функцию
    func = FunctionDecl(
        name="главная",
        parameters=[Parameter(name="x", param_type="целый")],
        return_type="ничто"
    )
    
    # Добавляем оператор печати
    print_stmt = PrintStmt(
        arguments=[StringLiteral(value="Привет, мир!")]
    )
    func.add_statement(print_stmt)
    
    # Создаем модуль
    module = Module(name="пример")
    module.add_statement(func)
    
    # Печатаем AST
    print(print_ast(module))
    
    print("\n✅ AST успешно создано!")
