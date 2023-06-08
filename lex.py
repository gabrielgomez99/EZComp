# Aqui va las instrucciones de analizador lexico
import ply.lex as lex

# Definimos los tokens
tokens = (
    'ID',
    'COMMENT',
    'IF',
    'ELSE',
    'MAIN',
    'VOID',
    'INT',
    'FLOAT',
    'CHAR',
    'PRINT',
    'VAR',
    'NE',
    'EQ',
    'GTEQ',
    'LTEQ',
    'READ',
    'WHILE',
    'FOR',
    'ARR',
    'FILE',
    'DATAFRAME',
    'OR',
    'MEAN',
    'MEDIAN',
    'MODE',
    'VARIANCE',
    'STDDEV',
    'HISTOGRAM',
    'FUNC',
    'RETURN',
    'CTECHAR',
    'CTEINT',
    'CTEFLOAT'
)

# Son palabras reservadas del leguaje entonces se tratan diferente
reserved = {
   'if' : 'IF',
   'else' : 'ELSE',
   'while' : 'WHILE',
   'for' : 'FOR',
   'int' : 'INT',
   'float' : 'FLOAT',
   'char' : 'CHAR',
   'var' : 'VAR',
   'print' : 'PRINT',
   'mean' : 'MEAN',
   'median' : 'MEDIAN',
   'mode' : 'MODE',
   'variance' : 'VARIANCE',
   'stdDev' : 'STDDEV',
   'histogram' : 'HISTOGRAM',
   'file' : 'FILE',
   'read' : 'READ',
   'arr' : 'ARR',
   'func' : 'FUNC',
   'return' : 'RETURN',
   'void' : 'VOID',
   'main' : 'MAIN'
}

# Tokens que son de un valor y son literales
literals = [ '+','-','*','/','=','(',')',';',':','[',']','{','}','>','<','.',',','"','&']

def t_DATAFRAME(t):
    r'\"[\w\d]*\.csv\"'
    return t

def t_COMMENT(t):
    r'\#.*'
    pass
    # Es para dejar pasar comentarios
    
def t_CTEFLOAT(t):
    r'[-+]?[\d]+\.[\d+]?'
    t.value = float(t.value)    
    return t
    #identifica numeros

# Definimos el token de numeros
def t_CTEINT(t):
    r'\d+'
    t.value = int(t.value)    
    return t
    #identifica numeros

def t_NE(t):
    r'!='
    t.value = (t.value)    
    return t
    # identifica <>

def t_OR(t):
    r'\|\|'
    t.value = (t.value)    
    return t
    # identifica ||

def t_GTEQ(t):
    r'>='
    t.value = (t.value)    
    return t
    # identifica >=

def t_LTEQ(t):
    r'<='
    t.value = (t.value)    
    return t
    # identifica <=

def t_EQ(t):
    r'=='
    t.value = (t.value)    
    return t
    # identifica ==

def t_CHAR(t):
    r'\"[a-zA-Z_0-9_!@#$%^&*()\-+=~`[\]{}|:;"\',.<>/?\\ ]*?\"'
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
#data = '''
#<=
#'''

#lex.input(data)

# Tokenize
#while True:
#    tok = lex.token()
#    if not tok: 
#        break      # Ya no mas input
#    print(tok)