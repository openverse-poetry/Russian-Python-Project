"""
Lexer for Russian Python language using PLY.
Implements tokens: если (if), печать (print), функция (function), 
пока (while), вернуть (return), ввод (input).
"""

from ply import lex

# List of token names - must be ASCII for PLY
tokens = (
    'IF',
    'PRINT',
    'FUNCTION',
    'WHILE',
    'RETURN',
    'INPUT',
    'NAME',
    'NUMBER',
    'STRING',
    'COLON',
    'COMMA',
    'LPAREN',
    'RPAREN',
    'LBRACE',
    'RBRACE',
    'ASSIGN',
    'PLUS',
    'MINUS',
    'TIMES',
    'DIVIDE',
    'GT',
    'LT',
    'EQ',
    'NE',
    'GE',
    'LE',
)

# Reserved keywords mapping
reserved = {
    'если': 'IF',
    'печать': 'PRINT',
    'функция': 'FUNCTION',
    'пока': 'WHILE',
    'вернуть': 'RETURN',
    'ввод': 'INPUT',
}

# Token regex rules
t_COLON = r':'
t_COMMA = r','
t_LPAREN = r'\('
t_RPAREN = r'\)'
t_LBRACE = r'\{'
t_RBRACE = r'\}'
t_ASSIGN = r'='
t_PLUS = r'\+'
t_MINUS = r'-'
t_TIMES = r'\*'
t_DIVIDE = r'/'
t_GT = r'>'
t_LT = r'<'
t_EQ = r'=='
t_NE = r'!='
t_GE = r'>='
t_LE = r'<='


def t_NUMBER(t):
    r'\d+'
    t.value = int(t.value)
    return t


def t_STRING(t):
    r'"[^"]*"|\'[^\']*\''
    t.value = t.value[1:-1]  # Remove quotes
    return t


def t_NAME(t):
    r'[а-яА-ЯёЁa-zA-Z_][а-яА-ЯёЁa-zA-Z0-9_]*'
    t.type = reserved.get(t.value.lower(), 'NAME')
    return t


# Ignored characters
t_ignore = ' \t\n\r'


def t_error(t):
    print(f"Недопустимый символ: '{t.value[0]}'")
    t.lexer.skip(1)


# Build the lexer
lexer = lex.lex()


if __name__ == '__main__':
    # Test the lexer with a sample Russian code
    test_code = """
    функция привет():
        печать("Привет, мир!")
    
    если 1 > 0:
        печать("Работает!")
    
    пока 1:
        вернуть ввод()
    """
    
    lexer.input(test_code)
    while True:
        tok = lexer.token()
        if not tok:
            break
        print(tok)
