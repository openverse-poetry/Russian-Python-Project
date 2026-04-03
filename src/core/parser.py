"""
Синтаксический анализатор (Парсер) для языка Русский Питон
Версия 0.1.0

Реализует рекурсивный спуск парсер для построения AST из потока токенов.
Поддерживает все конструкции языка:
- Объявления функций, классов, переменных
- Управляющие конструкции (если, пока, для)
- Выражения всех видов
- Операторы ввода/вывода
"""

from typing import List, Optional, Any, Dict, Tuple
from dataclasses import dataclass, field

from src.core.lexer import Token, TokenType, LexerError, tokenize_source
from src.ast.nodes import (
    ASTNode, Module, Program, FunctionDecl, Parameter, ClassDecl,
    VariableDecl, ImportDecl, FromImportDecl, ExpressionStmt, Assignment,
    AugmentedAssign, IfStmt, WhileStmt, ForStmt, ReturnStmt, BreakStmt,
    ContinueStmt, PassStmt, PrintStmt, InputStmt, BinaryOp, UnaryOp, Call,
    AttributeAccess, Subscript, Slice, NumberLiteral, StringLiteral,
    BooleanLiteral, NoneLiteral, ListLiteral, TupleLiteral, DictLiteral,
    SetLiteral, Identifier, Name, Lambda, TryStmt, ExceptClause, FinallyClause,
    RaiseStmt, AssertStmt, WithStmt, Decorator, print_ast
)


class ParseError(Exception):
    """Исключение парсера"""
    def __init__(self, message: str, token: Optional[Token] = None):
        self.message = message
        self.token = token
        self.line = token.line if token else 0
        self.column = token.column if token else 0
        super().__init__(self.format_message())
    
    def format_message(self) -> str:
        pos = f"строка {self.line}, столбец {self.column}" if self.line > 0 else "неизвестная позиция"
        token_info = f", токен: {self.token.value}" if self.token and self.token.value else ""
        return f"Синтаксическая ошибка в {pos}: {self.message}{token_info}"


@dataclass
class ParserConfig:
    """Конфигурация парсера"""
    debug_mode: bool = False
    error_recovery: bool = True
    max_errors: int = 100


class RussianParser:
    """
    Синтаксический анализатор для русского языка программирования
    
    Реализует рекурсивный спуск с поддержкой:
    - Приоритета операторов
    -Вложенных конструкций
    -Обработки ошибок с восстановлением
    """
    
    # Приоритеты операторов (от низшего к высшему)
    PRECEDENCE = {
        # Логические
        'или': 1,
        'и': 2,
        
        # Сравнения
        '<': 3, '>': 3, '<=': 3, '>=': 3, '==': 3, '!=': 3,
        
        # Сложение/вычитание
        '+': 4, '-': 4,
        
        # Умножение/деление
        '*': 5, '/': 5, '//': 5, '%': 5,
        
        # Унарные
        'не': 6, '-': 6, '+': 6,
        
        # Степень
        '**': 7,
    }
    
    # Правоассоциативные операторы
    RIGHT_ASSOCIATIVE = {'**', '='}
    
    def __init__(self, config: Optional[ParserConfig] = None):
        self.config = config or ParserConfig()
        self.tokens: List[Token] = []
        self.pos = 0
        self.errors: List[ParseError] = []
        self.current_module: Optional[Module] = None
    
    def parse(self, source: str) -> Module:
        """
        Парсинг исходного кода
        
        :param source: Исходный код на русском языке
        :return: Корневой узел AST (Module)
        :raises ParseError: При синтаксической ошибке
        """
        # Токенизация
        try:
            self.tokens = tokenize_source(source)
        except LexerError as e:
            raise ParseError(f"Лексическая ошибка: {e.message}", 
                           Token(TokenType.НЕИЗВЕСТНЫЙ, e.message, e.line, e.column))
        
        self.pos = 0
        self.errors = []
        self.current_module = Module(name="<main>")
        
        # Парсинг модуля
        module = self._parse_module()
        
        if self.errors and self.config.error_recovery:
            # Возвращаем первую ошибку
            raise self.errors[0]
        
        return module
    
    def _current_token(self) -> Optional[Token]:
        """Получение текущего токена"""
        if 0 <= self.pos < len(self.tokens):
            return self.tokens[self.pos]
        return None
    
    def _peek_token(self, offset: int = 0) -> Optional[Token]:
        """Просмотр токена со смещением"""
        idx = self.pos + offset
        if 0 <= idx < len(self.tokens):
            return self.tokens[idx]
        return None
    
    def _advance(self) -> Optional[Token]:
        """Переход к следующему токену"""
        token = self._current_token()
        if token:
            self.pos += 1
        return token
    
    def _match(self, *types: TokenType) -> bool:
        """Проверка текущего токена на совпадение с типами"""
        token = self._current_token()
        if token is None:
            return False
        return token.type in types
    
    def _expect(self, token_type: TokenType, message: str = "") -> Token:
        """Ожидание токена определенного типа"""
        token = self._current_token()
        
        if token is None:
            error_msg = message or f"Ожидался токен {token_type.name}, но достигнут конец файла"
            raise ParseError(error_msg, token)
        
        if token.type != token_type:
            error_msg = message or f"Ожидался токен {token_type.name}, но получен {token.type.name}"
            raise ParseError(error_msg, token)
        
        return self._advance()
    
    def _skip_newlines(self):
        """Пропуск переводов строк"""
        while self._match(TokenType.НОВАЯ_СТРОКА):
            self._advance()
    
    def _parse_module(self) -> Module:
        """Парсинг модуля"""
        module = self.current_module
        
        self._skip_newlines()
        
        while not self._match(TokenType.КОНЕЦ_ФАЙЛА):
            try:
                stmt = self._parse_statement()
                if stmt:
                    module.add_statement(stmt)
            except ParseError as e:
                self.errors.append(e)
                if len(self.errors) >= self.config.max_errors:
                    break
                
                # Восстановление после ошибки
                if self.config.error_recovery:
                    self._recover_from_error()
            
            self._skip_newlines()
        
        return module
    
    def _recover_from_error(self):
        """Восстановление после синтаксической ошибки"""
        # Пропускаем токены до безопасной точки
        while not self._match(TokenType.КОНЕЦ_ФАЙЛА, TokenType.ФУНКЦИЯ, 
                             TokenType.КЛАСС, TokenType.ЕСЛИ, TokenType.ПОКА,
                             TokenType.ДЛЯ, TokenType.ВЕРНУТЬ):
            self._advance()
    
    def _parse_statement(self) -> Optional[ASTNode]:
        """Парсинг оператора"""
        token = self._current_token()
        
        if token is None or token.type == TokenType.КОНЕЦ_ФАЙЛА:
            return None
        
        # Декораторы
        decorators = []
        while self._match(TokenType.ИДЕНТИФИКАТОР) and self._peek_token(1) and self._peek_token(1).type == TokenType.ТОЧКА:
            decorators.append(self._parse_decorator())
            self._skip_newlines()
        
        # Ключевые слова операторов
        if self._match(TokenType.ФУНКЦИЯ):
            return self._parse_function_def(decorators)
        
        elif self._match(TokenType.КЛАСС):
            return self._parse_class_def(decorators)
        
        elif self._match(TokenType.ЕСЛИ):
            return self._parse_if_stmt()
        
        elif self._match(TokenType.ПОКА):
            return self._parse_while_stmt()
        
        elif self._match(TokenType.ДЛЯ):
            return self._parse_for_stmt()
        
        elif self._match(TokenType.ВЕРНУТЬ):
            return self._parse_return_stmt()
        
        elif self._match(TokenType.ИМПОРТ):
            return self._parse_import_stmt()
        
        elif self._match(TokenType.ИЗ):
            return self._parse_from_import_stmt()
        
        elif self._match(TokenType.ИДЕНТИФИКАТОР):
            return self._parse_print_stmt()
        
        elif self._match(TokenType.ИДЕНТИФИКАТОР):
            return self._parse_input_stmt()
        
        elif self._match(TokenType.ИДЕНТИФИКАТОР):
            return self._parse_try_stmt()
        
        elif self._match(TokenType.ИДЕНТИФИКАТОР):
            return self._parse_raise_stmt()
        
        elif self._match(TokenType.ИДЕНТИФИКАТОР):
            return self._parse_assert_stmt()
        
        elif self._match(TokenType.С):
            return self._parse_with_stmt()
        
        elif self._match(TokenType.ПРЕРВАТЬ):
            self._advance()
            return BreakStmt(line=token.line, column=token.column)
        
        elif self._match(TokenType.ПРОДОЛЖИТЬ):
            self._advance()
            return ContinueStmt(line=token.line, column=token.column)
        
        elif self._match(TokenType.НИЧТО):
            self._advance()
            return PassStmt(line=token.line, column=token.column)
        
        # Присваивание или выражение
        elif self._match(TokenType.ИДЕНТИФИКАТОР, TokenType.ИДЕНТИФИКАТОР):
            return self._parse_assignment_or_expr()
        
        else:
            # Пытаемся распарсить как выражение
            expr = self._parse_expression()
            if expr:
                return ExpressionStmt(expression=expr, line=token.line, column=token.column)
        
        return None
    
    def _parse_function_def(self, decorators: List[Decorator]) -> FunctionDecl:
        """Парсинг объявления функции"""
        start_token = self._expect(TokenType.ФУНКЦИЯ)
        
        # Имя функции
        name_token = self._expect(TokenType.ИДЕНТИФИКАТОР, "Ожидалось имя функции")
        name = name_token.value
        
        func = FunctionDecl(
            name=name,
            decorators=decorators,
            line=start_token.line,
            column=start_token.column
        )
        
        # Параметры
        self._expect(TokenType.ЛЕВАЯ_СКОБКА, "Ожидалась '(' после имени функции")
        
        if not self._match(TokenType.ПРАВАЯ_СКОБКА):
            func.parameters = self._parse_parameters()
        
        self._expect(TokenType.ПРАВАЯ_СКОБКА, "Ожидалась ')' после параметров")
        
        # Тип возвращаемого значения (опционально)
        if self._match(TokenType.ДВОЕТОЧИЕ):
            self._advance()
            # Здесь можно добавить парсинг типа возврата
        
        # Тело функции
        self._expect(TokenType.ДВОЕТОЧИЕ, "Ожидалось ':' после сигнатуры функции")
        func.body = self._parse_block()
        
        return func
    
    def _parse_parameters(self) -> List[Parameter]:
        """Парсинг списка параметров"""
        parameters = []
        
        while True:
            param = self._parse_parameter()
            if param:
                parameters.append(param)
            
            if not self._match(TokenType.ЗАПЯТАЯ):
                break
            self._advance()
            
            if self._match(TokenType.ПРАВАЯ_СКОБКА):
                break
        
        return parameters
    
    def _parse_parameter(self) -> Optional[Parameter]:
        """Парсинг одного параметра"""
        token = self._current_token()
        
        if not self._match(TokenType.ИДЕНТИФИКАТОР, TokenType.ИДЕНТИФИКАТОР):
            return None
        
        name_token = self._advance()
        
        param = Parameter(
            name=name_token.value,
            line=token.line,
            column=token.column
        )
        
        # Тип параметра (опционально)
        if self._match(TokenType.ДВОЕТОЧИЕ):
            self._advance()
            # Парсинг типа
        
        # Значение по умолчанию (опционально)
        if self._match(TokenType.ПРИСВОИТЬ):
            self._advance()
            param.default_value = self._parse_expression()
        
        return param
    
    def _parse_class_def(self, decorators: List[Decorator]) -> ClassDecl:
        """Парсинг объявления класса"""
        start_token = self._expect(TokenType.КЛАСС)
        
        # Имя класса
        name_token = self._expect(TokenType.ИДЕНТИФИКАТОР, "Ожидалось имя класса")
        name = name_token.value
        
        cls = ClassDecl(
            name=name,
            decorators=decorators,
            line=start_token.line,
            column=start_token.column
        )
        
        # Базовые классы
        if self._match(TokenType.ЛЕВАЯ_СКОБКА):
            self._advance()
            
            if not self._match(TokenType.ПРАВАЯ_СКОБКА):
                cls.base_classes = self._parse_base_classes()
            
            self._expect(TokenType.ПРАВАЯ_СКОБКА)
        
        # Тело класса
        self._expect(TokenType.ДВОЕТОЧИЕ, "Ожидалось ':' после объявления класса")
        cls.body = self._parse_class_body()
        
        return cls
    
    def _parse_base_classes(self) -> List[ASTNode]:
        """Парсинг базовых классов"""
        bases = []
        
        while True:
            base = self._parse_expression()
            if base:
                bases.append(base)
            
            if not self._match(TokenType.ЗАПЯТАЯ):
                break
            self._advance()
        
        return bases
    
    def _parse_class_body(self) -> List[ASTNode]:
        """Парсинг тела класса"""
        body = []
        indent_level = 0
        
        self._skip_newlines()
        
        # Простая реализация - парсим пока не встретим dedent
        while not self._match(TokenType.КОНЕЦ_ФАЙЛА):
            # Проверка на отступ (упрощенно)
            if self._match(TokenType.ФУНКЦИЯ):
                method = self._parse_function_def([])
                body.append(method)
            elif self._match(TokenType.ИДЕНТИФИКАТОР):
                # Атрибут класса
                attr = self._parse_assignment_or_expr()
                if attr:
                    body.append(attr)
            else:
                break
            
            self._skip_newlines()
        
        return body
    
    def _parse_if_stmt(self) -> IfStmt:
        """Парсинг условного оператора"""
        start_token = self._expect(TokenType.ЕСЛИ)
        
        condition = self._parse_expression()
        
        self._expect(TokenType.ДВОЕТОЧИЕ, "Ожидалось ':' после условия если")
        then_branch = self._parse_block()
        
        if_stmt = IfStmt(
            condition=condition,
            then_branch=then_branch,
            line=start_token.line,
            column=start_token.column
        )
        
        # Ветки иначе-если и иначе
        while self._match(TokenType.ИНАЧЕ):
            self._advance()
            
            if self._match(TokenType.ЕСЛИ):
                # иначе-если
                self._advance()
                elif_condition = self._parse_expression()
                self._expect(TokenType.ДВОЕТОЧИЕ)
                elif_body = self._parse_block()
                if_stmt.elif_branches.append((elif_condition, elif_body))
            else:
                # иначе
                self._expect(TokenType.ДВОЕТОЧИЕ, "Ожидалось ':' после иначе")
                if_stmt.else_branch = self._parse_block()
                break
        
        return if_stmt
    
    def _parse_while_stmt(self) -> WhileStmt:
        """Парсинг цикла пока"""
        start_token = self._expect(TokenType.ПОКА)
        
        condition = self._parse_expression()
        
        self._expect(TokenType.ДВОЕТОЧИЕ, "Ожидалось ':' после условия пока")
        body = self._parse_block()
        
        while_stmt = WhileStmt(
            condition=condition,
            body=body,
            line=start_token.line,
            column=start_token.column
        )
        
        # Ветка иначе для цикла
        if self._match(TokenType.ИНАЧЕ):
            self._advance()
            self._expect(TokenType.ДВОЕТОЧИЕ)
            while_stmt.else_branch = self._parse_block()
        
        return while_stmt
    
    def _parse_for_stmt(self) -> ForStmt:
        """Парсинг цикла для"""
        start_token = self._expect(TokenType.ДЛЯ)
        
        # Переменная цикла
        target = self._parse_expression()
        
        self._expect(TokenType.ИЗ, "Ожидалось 'из' после переменной цикла")
        
        # Итерируемый объект
        iterable = self._parse_expression()
        
        self._expect(TokenType.ДВОЕТОЧИЕ, "Ожидалось ':' после выражения цикла")
        body = self._parse_block()
        
        for_stmt = ForStmt(
            target=target,
            iterable=iterable,
            body=body,
            line=start_token.line,
            column=start_token.column
        )
        
        # Ветка иначе для цикла
        if self._match(TokenType.ИНАЧЕ):
            self._advance()
            self._expect(TokenType.ДВОЕТОЧИЕ)
            for_stmt.else_branch = self._parse_block()
        
        return for_stmt
    
    def _parse_return_stmt(self) -> ReturnStmt:
        """Парсинг оператора вернуть"""
        start_token = self._expect(TokenType.ВЕРНУТЬ)
        
        value = None
        if not self._match(TokenType.ДВОЕТОЧИЕ, TokenType.НОВАЯ_СТРОКА):
            value = self._parse_expression()
        
        return ReturnStmt(
            value=value,
            line=start_token.line,
            column=start_token.column
        )
    
    def _parse_import_stmt(self) -> ImportDecl:
        """Парсинг оператора импорт"""
        start_token = self._expect(TokenType.ИМПОРТ)
        
        module_token = self._expect(TokenType.ИДЕНТИФИКАТОР, "Ожидалось имя модуля")
        
        imp = ImportDecl(
            module_name=module_token.value,
            line=start_token.line,
            column=start_token.column
        )
        
        # Псевдоним
        if self._match(TokenType.КАК):
            self._advance()
            alias_token = self._expect(TokenType.ИДЕНТИФИКАТОР)
            imp.alias = alias_token.value
        
        return imp
    
    def _parse_from_import_stmt(self) -> FromImportDecl:
        """Парсинг оператора из ... импорт"""
        start_token = self._expect(TokenType.ИЗ)
        
        module_token = self._expect(TokenType.ИДЕНТИФИКАТОР, "Ожидалось имя модуля")
        
        self._expect(TokenType.ИМПОРТ, "Ожидалось 'импорт' после имени модуля")
        
        imp = FromImportDecl(
            module_name=module_token.value,
            line=start_token.line,
            column=start_token.column
        )
        
        # Импортируемые имена
        if self._match(TokenType.УМНОЖИТЬ):
            self._advance()
            imp.is_star = True
        else:
            while True:
                name_token = self._expect(TokenType.ИДЕНТИФИКАТОР)
                alias = None
                
                if self._match(TokenType.КАК):
                    self._advance()
                    alias_token = self._expect(TokenType.ИДЕНТИФИКАТОР)
                    alias = alias_token.value
                
                imp.add_name(name_token.value, alias)
                
                if not self._match(TokenType.ЗАПЯТАЯ):
                    break
                self._advance()
        
        return imp
    
    def _parse_print_stmt(self) -> PrintStmt:
        """Парсинг оператора печать"""
        start_token = self._expect(TokenType.ИДЕНТИФИКАТОР)
        
        self._expect(TokenType.ЛЕВАЯ_СКОБКА, "Ожидалась '(' после печать")
        
        print_stmt = PrintStmt(line=start_token.line, column=start_token.column)
        
        if not self._match(TokenType.ПРАВАЯ_СКОБКА):
            while True:
                arg = self._parse_expression()
                if arg:
                    print_stmt.add_argument(arg)
                
                if not self._match(TokenType.ЗАПЯТАЯ):
                    break
                self._advance()
        
        self._expect(TokenType.ПРАВАЯ_СКОБКА, "Ожидалась ')' после аргументов печать")
        
        return print_stmt
    
    def _parse_input_stmt(self) -> InputStmt:
        """Парсинг оператора ввод"""
        start_token = self._expect(TokenType.ИДЕНТИФИКАТОР)
        
        prompt = None
        
        if self._match(TokenType.ЛЕВАЯ_СКОБКА):
            self._advance()
            
            if not self._match(TokenType.ПРАВАЯ_СКОБКА):
                prompt = self._parse_expression()
            
            self._expect(TokenType.ПРАВАЯ_СКОБКА)
        
        return InputStmt(
            prompt=prompt,
            line=start_token.line,
            column=start_token.column
        )
    
    def _parse_assignment_or_expr(self) -> Optional[ASTNode]:
        """Парсинг присваивания или выражения"""
        left = self._parse_expression()
        
        if self._match(TokenType.ПРИСВОИТЬ):
            self._advance()
            right = self._parse_expression()
            
            return Assignment(
                target=left,
                value=right,
                line=left.line,
                column=left.column
            )
        
        # Составное присваивание
        if self._match(TokenType.ПЛЮС_РАВНО, TokenType.МИНУС_РАВНО,
                      TokenType.УМНОЖИТЬ_РАВНО, TokenType.РАЗДЕЛИТЬ_РАВНО):
            op_token = self._advance()
            right = self._parse_expression()
            
            return AugmentedAssign(
                target=left,
                value=right,
                operator=op_token.value,
                line=left.line,
                column=left.column
            )
        
        # Просто выражение
        return ExpressionStmt(expression=left, line=left.line, column=left.column)
    
    def _parse_expression(self, precedence: int = 0) -> Optional[ASTNode]:
        """Парсинг выражения с учетом приоритета операторов"""
        left = self._parse_primary()
        
        if left is None:
            return None
        
        while True:
            token = self._current_token()
            
            if token is None or token.type == TokenType.КОНЕЦ_ФАЙЛА:
                break
            
            # Получаем оператор
            op = None
            if token.type in (TokenType.ПЛЮС, TokenType.МИНУС, TokenType.УМНОЖИТЬ,
                             TokenType.РАЗДЕЛИТЬ, TokenType.ОСТАТОК, TokenType.СТЕПЕНЬ,
                             TokenType.РАВНО, TokenType.НЕ_РАВНО, TokenType.МЕНЬШЕ,
                             TokenType.БОЛЬШЕ, TokenType.МЕНЬШЕ_ИЛИ_РАВНО,
                             TokenType.БОЛЬШЕ_ИЛИ_РАВНО, TokenType.И, TokenType.ИЛИ):
                op = token.value
            elif token.type == TokenType.НЕ:
                op = 'не'
            else:
                break
            
            # Проверяем приоритет
            op_prec = self.PRECEDENCE.get(op, 0)
            if op_prec < precedence:
                break
            
            self._advance()
            
            # Правоассоциативность
            next_prec = op_prec + 1 if op in self.RIGHT_ASSOCIATIVE else op_prec
            
            right = self._parse_expression(next_prec)
            
            left = BinaryOp(
                left=left,
                right=right,
                operator=op,
                line=left.line,
                column=left.column
            )
        
        return left
    
    def _parse_primary(self) -> Optional[ASTNode]:
        """Парсинг первичных выражений"""
        token = self._current_token()
        
        if token is None:
            return None
        
        # Число
        if self._match(TokenType.ЧИСЛО, TokenType.ДРОБНОЕ_ЧИСЛО):
            self._advance()
            return NumberLiteral(
                value=token.value,
                line=token.line,
                column=token.column
            )
        
        # Строка
        if self._match(TokenType.СТРОКА_ЛИТ):
            self._advance()
            return StringLiteral(
                value=token.value,
                line=token.line,
                column=token.column
            )
        
        # Булево значение
        if self._match(TokenType.ИСТИНА):
            self._advance()
            return BooleanLiteral(
                value=True,
                line=token.line,
                column=token.column
            )
        
        if self._match(TokenType.ЛОЖЬ):
            self._advance()
            return BooleanLiteral(
                value=False,
                line=token.line,
                column=token.column
            )
        
        # Ничто
        if self._match(TokenType.НИЧТО):
            self._advance()
            return NoneLiteral(line=token.line, column=token.column)
        
        # Идентификатор
        if self._match(TokenType.ИДЕНТИФИКАТОР, TokenType.ИДЕНТИФИКАТОР):
            self._advance()
            name = Identifier(
                name=token.value,
                line=token.line,
                column=token.column
            )
            
            # Проверка на вызов функции или доступ к атрибуту
            return self._parse_trailer(name)
        
        # Список
        if self._match(TokenType.ЛЕВАЯ_КВАДРАТНАЯ):
            return self._parse_list_literal()
        
        # Кортеж
        if self._match(TokenType.ЛЕВАЯ_СКОБКА):
            return self._parse_tuple_or_paren()
        
        # Словарь
        if self._match(TokenType.ЛЕВАЯ_ФИГУРНАЯ):
            return self._parse_dict_literal()
        
        # Унарный оператор
        if self._match(TokenType.МИНУС, TokenType.ПЛЮС, TokenType.НЕ):
            self._advance()
            operand = self._parse_primary()
            return UnaryOp(
                operand=operand,
                operator=token.value,
                line=token.line,
                column=token.column
            )
        
        return None
    
    def _parse_trailer(self, left: ASTNode) -> ASTNode:
        """Парсинг трейлеров (вызов функции, доступ к атрибуту, индексация)"""
        while True:
            if self._match(TokenType.ЛЕВАЯ_СКОБКА):
                # Вызов функции
                self._advance()
                args = []
                kwargs = {}
                
                if not self._match(TokenType.ПРАВАЯ_СКОБКА):
                    args, kwargs = self._parse_call_args()
                
                self._expect(TokenType.ПРАВАЯ_СКОБКА)
                
                left = Call(
                    function=left,
                    arguments=args,
                    keyword_args=kwargs,
                    line=left.line,
                    column=left.column
                )
            
            elif self._match(TokenType.ТОЧКА):
                # Доступ к атрибуту
                self._advance()
                attr_token = self._expect(TokenType.ИДЕНТИФИКАТОР, "Ожидалось имя атрибута")
                
                left = AttributeAccess(
                    object=left,
                    attribute=attr_token.value,
                    line=left.line,
                    column=left.column
                )
            
            elif self._match(TokenType.ЛЕВАЯ_КВАДРАТНАЯ):
                # Индексация
                self._advance()
                index = self._parse_expression()
                self._expect(TokenType.ПРАВАЯ_КВАДРАТНАЯ, "Ожидалась ']'")
                
                left = Subscript(
                    value=left,
                    index=index,
                    line=left.line,
                    column=left.column
                )
            
            else:
                break
        
        return left
    
    def _parse_call_args(self) -> Tuple[List[ASTNode], Dict[str, ASTNode]]:
        """Парсинг аргументов вызова функции"""
        args = []
        kwargs = {}
        
        while True:
            # Проверяем на именованный аргумент
            if (self._match(TokenType.ИДЕНТИФИКАТОР) and 
                self._peek_token(1) and 
                self._peek_token(1).type == TokenType.ПРИСВОИТЬ):
                
                name_token = self._advance()
                self._advance()  # пропускаем '='
                value = self._parse_expression()
                kwargs[name_token.value] = value
            else:
                arg = self._parse_expression()
                if arg:
                    args.append(arg)
            
            if not self._match(TokenType.ЗАПЯТАЯ):
                break
            self._advance()
            
            if self._match(TokenType.ПРАВАЯ_СКОБКА):
                break
        
        return args, kwargs
    
    def _parse_list_literal(self) -> ListLiteral:
        """Парсинг спискового литерала"""
        start_token = self._expect(TokenType.ЛЕВАЯ_КВАДРАТНАЯ)
        
        list_lit = ListLiteral(line=start_token.line, column=start_token.column)
        
        if not self._match(TokenType.ПРАВАЯ_КВАДРАТНАЯ):
            while True:
                elem = self._parse_expression()
                if elem:
                    list_lit.add_element(elem)
                
                if not self._match(TokenType.ЗАПЯТАЯ):
                    break
                self._advance()
        
        self._expect(TokenType.ПРАВАЯ_КВАДРАТНАЯ, "Ожидалась ']'")
        
        return list_lit
    
    def _parse_tuple_or_paren(self) -> ASTNode:
        """Парсинг кортежа или выражения в скобках"""
        start_token = self._expect(TokenType.ЛЕВАЯ_СКОБКА)
        
        # Пустые скобки
        if self._match(TokenType.ПРАВАЯ_СКОБКА):
            self._advance()
            return TupleLiteral(line=start_token.line, column=start_token.column)
        
        expr = self._parse_expression()
        
        # Одна запятая означает кортеж
        if self._match(TokenType.ЗАПЯТАЯ):
            self._advance()
            elements = [expr]
            
            while not self._match(TokenType.ПРАВАЯ_СКОБКА):
                elem = self._parse_expression()
                if elem:
                    elements.append(elem)
                
                if not self._match(TokenType.ЗАПЯТАЯ):
                    break
                self._advance()
            
            self._expect(TokenType.ПРАВАЯ_СКОБКА)
            
            return TupleLiteral(
                elements=elements,
                line=start_token.line,
                column=start_token.column
            )
        
        # Просто выражение в скобках
        self._expect(TokenType.ПРАВАЯ_СКОБКА)
        return expr
    
    def _parse_dict_literal(self) -> DictLiteral:
        """Парсинг словарного литерала"""
        start_token = self._expect(TokenType.ЛЕВАЯ_ФИГУРНАЯ)
        
        dict_lit = DictLiteral(line=start_token.line, column=start_token.column)
        
        if not self._match(TokenType.ПРАВАЯ_ФИГУРНАЯ):
            while True:
                key = self._parse_expression()
                self._expect(TokenType.ДВОЕТОЧИЕ, "Ожидалось ':' после ключа словаря")
                value = self._parse_expression()
                
                dict_lit.add_item(key, value)
                
                if not self._match(TokenType.ЗАПЯТАЯ):
                    break
                self._advance()
        
        self._expect(TokenType.ПРАВАЯ_ФИГУРНАЯ, "Ожидалась '}'")
        
        return dict_lit
    
    def _parse_block(self) -> List[ASTNode]:
        """Парсинг блока операторов"""
        block = []
        
        self._skip_newlines()
        
        # Парсим пока не встретим конец блока
        while not self._match(TokenType.КОНЕЦ_ФАЙЛА):
            # Проверка на конец блока (упрощенно)
            if self._match(TokenType.ИНАЧЕ, TokenType.ВЕРНУТЬ):
                break
            
            stmt = self._parse_statement()
            if stmt:
                block.append(stmt)
            else:
                break
            
            self._skip_newlines()
        
        return block
    
    def _parse_decorator(self) -> Decorator:
        """Парсинг декоратора"""
        start_token = self._current_token()
        
        # Имя декоратора
        name = self._parse_expression()
        
        decorator = Decorator(
            name=name,
            line=start_token.line,
            column=start_token.column
        )
        
        # Аргументы декоратора
        if self._match(TokenType.ЛЕВАЯ_СКОБКА):
            self._advance()
            
            if not self._match(TokenType.ПРАВАЯ_СКОБКА):
                args, kwargs = self._parse_call_args()
                decorator.arguments = args
                decorator.keyword_args = kwargs
            
            self._expect(TokenType.ПРАВАЯ_СКОБКА)
        
        return decorator
    
    def _parse_try_stmt(self) -> TryStmt:
        """Парсинг оператора попытка"""
        start_token = self._expect(TokenType.ИДЕНТИФИКАТОР)
        
        self._expect(TokenType.ДВОЕТОЧИЕ)
        body = self._parse_block()
        
        try_stmt = TryStmt(
            body=body,
            line=start_token.line,
            column=start_token.column
        )
        
        # Ветки кроме
        while self._match(TokenType.КРОМЕ):
            self._advance()
            except_clause = self._parse_except_clause()
            try_stmt.except_clauses.append(except_clause)
        
        # Ветка иначе
        if self._match(TokenType.ИНАЧЕ):
            self._advance()
            self._expect(TokenType.ДВОЕТОЧИЕ)
            try_stmt.else_branch = self._parse_block()
        
        # Ветка наконец
        if self._match(TokenType.НАКОНЕЦ):
            self._advance()
            self._expect(TokenType.ДВОЕТОЧИЕ)
            finally_body = self._parse_block()
            try_stmt.finally_clause = FinallyClause(body=finally_body)
        
        return try_stmt
    
    def _parse_except_clause(self) -> ExceptClause:
        """Парсинг ветки кроме"""
        exception_type = None
        exception_name = None
        
        if self._match(TokenType.ИДЕНТИФИКАТОР):
            exception_type = self._parse_expression()
            
            if self._match(TokenType.КАК):
                self._advance()
                name_token = self._expect(TokenType.ИДЕНТИФИКАТОР)
                exception_name = name_token.value
        
        self._expect(TokenType.ДВОЕТОЧИЕ)
        body = self._parse_block()
        
        return ExceptClause(
            exception_type=exception_type,
            exception_name=exception_name,
            body=body
        )
    
    def _parse_raise_stmt(self) -> RaiseStmt:
        """Парсинг оператора выбросить"""
        start_token = self._expect(TokenType.ИДЕНТИФИКАТОР)
        
        exception = None
        from_exception = None
        
        if not self._match(TokenType.ДВОЕТОЧИЕ, TokenType.НОВАЯ_СТРОКА):
            exception = self._parse_expression()
            
            if self._match(TokenType.ИЗ):
                self._advance()
                from_exception = self._parse_expression()
        
        return RaiseStmt(
            exception=exception,
            from_exception=from_exception,
            line=start_token.line,
            column=start_token.column
        )
    
    def _parse_assert_stmt(self) -> AssertStmt:
        """Парсинг оператора утверждение"""
        start_token = self._expect(TokenType.ИДЕНТИФИКАТОР)
        
        condition = self._parse_expression()
        message = None
        
        if self._match(TokenType.ЗАПЯТАЯ):
            self._advance()
            message = self._parse_expression()
        
        return AssertStmt(
            condition=condition,
            message=message,
            line=start_token.line,
            column=start_token.column
        )
    
    def _parse_with_stmt(self) -> WithStmt:
        """Парсинг оператора с"""
        start_token = self._expect(TokenType.С)
        
        items = []
        
        # Элемент контекстного менеджера
        expr = self._parse_expression()
        var_name = None
        
        if self._match(TokenType.КАК):
            self._advance()
            var_token = self._expect(TokenType.ИДЕНТИФИКАТОР)
            var_name = var_token.value
        
        items.append((expr, var_name))
        
        self._expect(TokenType.ДВОЕТОЧИЕ)
        body = self._parse_block()
        
        return WithStmt(
            items=items,
            body=body,
            line=start_token.line,
            column=start_token.column
        )
    
    def get_errors(self) -> List[ParseError]:
        """Получение списка ошибок"""
        return self.errors
    
    def has_errors(self) -> bool:
        """Проверка наличия ошибок"""
        return len(self.errors) > 0


def parse_source(source: str, config: Optional[ParserConfig] = None) -> Module:
    """
    Удобная функция для парсинга исходного кода
    
    :param source: Исходный код
    :param config: Конфигурация парсера
    :return: AST модуля
    """
    parser = RussianParser(config)
    return parser.parse(source)


if __name__ == "__main__":
    # Демо-пример использования парсера
    demo_code = '''
функция главная():
    печать("Привет, мир!")
    
    х = 10
    у = 20
    
    если х < у:
        печать("х меньше у")
    иначе:
        печать("х больше или равен у")
    
    вернуть х + у
'''
    
    print("Исходный код:")
    print(demo_code)
    print("\n")
    
    try:
        ast = parse_source(demo_code)
        print("AST:")
        print(print_ast(ast))
        print("\n✅ Успешный парсинг!")
    except ParseError as e:
        print(f"\n❌ Ошибка: {e}")
