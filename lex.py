# Aqui va las instrucciones de analizador lexico
import ply.lex as lex
import re

# Definimos los tokens
tokens = (
    'PLUS',
    'MINUS',
    'TIMES',
    'DIVIDE',
    'LPAREN',
    'RPAREN',
    'EQUALS',
    'ID',
    'COMMENT',
    'IF',
    'THEN',
    'ELSE',
    'WHILE',
    'MORELESS',
    'CTESTRING',
    'PROGRAM',
    'INT',
    'FLOAT',
    'PRINT',
    'VAR',
    
)

# Son palabras reservadas del leguaje entonces se tratan diferente
reserved = {
   'if' : 'IF',
   'then' : 'THEN',
   'else' : 'ELSE',
   'while' : 'WHILE',
   'program' : 'PROGRAM',
   'int' : 'INT',
   'float' : 'FLOAT',
   'var' : 'VAR',

}

# Tokens que son de un valor y son literales
literals = [ '+','-','*','/','=','(',')',';',':','[',']','{','}','>','<','.',',','"']

def t_COMMENT(t):
    r'\#.*'
    pass
    # Es para dejar pasar comentarios
    
def t_FLOAT(t):
    r'[-+]?[\d]+\.[\d+]?'
    t.value = float(t.value)    
    return t
    #identifica numeros

# Definimos el token de numeros
def t_INT(t):
    r'\d+'
    t.value = int(t.value)    
    return t
    #identifica numeros

def t_MORELESS(t):
    r'<>'
    t.value = (t.value)    
    return t
    # identifica <>

def t_CTESTRING(t):
    r'\"[a-zA-Z_0-9_ ]*?\"'
    t.value = t.value[1:-1]
    return t
    # identifica si es un string

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
lex = lex.lex()

# Probarlo
data = '''
3 + 20.1 
'''

lex.input(data)

# Tokenize
while True:
    tok = lex.token()
    if not tok: 
        break      # No more input
    print(tok)