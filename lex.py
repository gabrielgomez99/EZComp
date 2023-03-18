# Aqui va las instrucciones de analizador lexico
import ply.lex as lex

# Definimos los tokens
tokens = (
    'NUMBER',
    'PLUS',
    'MINUS',
    'TIMES',
    'DIVIDE',
    'LPAREN',
    'RPAREN',
    'ID',
    'COMMENT',
)

# Son palabras reservadas del leguaje entonces se tratan diferente
reserved = {
   'if' : 'IF',
   'then' : 'THEN',
   'else' : 'ELSE',
   'while' : 'WHILE',
}

# Reglas para expresiones regulares
t_PLUS = r'\+'
t_MINUS = r'-'
t_TIMES = r'\*'
t_DIVIDE = r'/'
t_EQUALS = r'='
t_LPAREN = r'\('
t_RPAREN = r'\)'

def t_COMMENT(t):
    r'\#.*'
    pass
    # Es para dejar pasar comentarios
    
# Definimos el token de numeros
def t_NUMBER(t):
    r'\d+'
    t.value = int(t.value)    
    return t

def t_ID(t):
    r'[a-zA-Z_][a-zA-Z_0-9]*'
    t.type = reserved.get(t.value,'ID')    # Checamos por palabras reservadas
    return t

# Esta regla sirve para contar el numero de linea
def t_newline(t):
    r'\n+'
    t.lexer.lineno += len(t.value)

# Sirve para ignorar espacios y tabs
t_ignore  = ' \t'

# Regla error handling
def t_error(t):
    print("Illegal character '%s'" % t.value[0])
    t.lexer.skip(1)

# Construye el Lexer
lexer = lex.lex()