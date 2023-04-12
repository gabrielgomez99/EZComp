import ply.yacc as yacc
from lex import tokens
from lex import literals

# Empieza el programa
def p_programa_start(p):
	'''
	programa_start		: PROGRAM ID ';' programa_start_1 BLOQUE
	'''
def p_programa_start_1(p):
	'''
	programa_start_1	: VARS 
		| empty
	'''
	
def p_VARS(p):
	'''
	VARS		        : VAR ID VARS_1 ':' TIPO ';' VARS_2 
	'''
def p_VARS_1(p):
	'''
	VARS_1		        : ',' ID VARS_1 
                        | empty
	'''
def p_VARS_2(p):
	'''
	VARS_2		        : ID VARS_1 ':' TIPO ';' VARS_2
                        | empty
	'''
	
def p_TIPO(p):
	'''
	TIPO		        : FLOAT
                        | INT
	'''

def p_BLOQUE(p):
	'''
	BLOQUE		        : '{' BLOQUE_1 '}'
	'''
def p_BLOQUE_1(p):
	'''
	BLOQUE_1		    : ESTATUTO BLOQUE_1
                        | empty
	'''

def p_ESTATUTO(p):
	'''
	ESTATUTO		    : ASIGNACION
                        | CONDICION
			            | ESCRITURA
	'''

def p_ASIGNACION(p):
	'''
	ASIGNACION		    : ID '=' EXPRESION ';'
	'''	

def p_EXPRESION(p):
	'''
	EXPRESION		    : EXP EXPRESION_1
	'''		
def p_EXP(p):
	'''
	EXP     		    : TERMINO EXP_1
	'''	
def p_EXP_1(p):
	'''
	EXP_1     		    : '+' EXP
                        | '-' EXP
                        | empty
	'''	
def p_EXPRESION_1(p):
	'''
	EXPRESION_1		    : '>' EXPRESION
                        | '<' EXPRESION
                        | MORELESS EXPRESION
                        | empty
	'''	
	
def p_ESCRITURA(p):
	'''
	ESCRITURA		    : PRINT '(' ESCRITURA_1 ')' ';'
	'''	
def p_ESCRITURA_1(p):
	'''
	ESCRITURA_1		    : CTESTRING ESCRITURA_2
                        | EXPRESION ESCRITURA_2
	'''	
def p_ESCRITURA_2(p):
	'''
	ESCRITURA_2		    : ',' ESCRITURA_1
                        | empty
	'''	
	
def p_CONDICION(p):
	'''
	CONDICION		    : IF '(' EXPRESION ')' BLOQUE CONDICION_1 ';'
	'''	
def p_CONDICION_1(p):
	'''
	CONDICION_1		    : ELSE BLOQUE
                        | empty
	'''	

def p_TERMINO(p):
	'''
	TERMINO 		    : FACTOR TERMINO_1
	'''	
def p_TERMINO_1(p):
	'''
	TERMINO_1 		    : '*' TERMINO
                        | '/' TERMINO
                        | empty
	'''	

def p_FACTOR(p):
	'''
	FACTOR   		    : '(' EXPRESION ')' FACTOR_1
                        | FACTOR_1 VAR_CTE
	'''	
def p_FACTOR_1(p):
	'''
	FACTOR_1  		    : '+'
                        | '-'
                        | empty
	'''	

def p_VAR_CTE(p):
	'''
	VAR_CTE 		    : ID
                        | FLOAT
                        | INT
	'''	

# Empty symbol = ε
def p_empty(p):
	'''
	empty				: 
	'''
	pass

errorFlag = False

def p_error(p):
    if p:
         print(f"Syntax error at token {p.type} ({p.value}) in line {p.lineno}")
         # Se descarta el token y dice que siga avanzando reportantodo el error
         errorFlag = True
         parser.errok()
    else:
         errorFlag = True
         print("Syntax error at EOF")

    	
# Crea el objeto parser
parser = yacc.yacc()

# Lee de un archivo de entrada
with open('texto.txt', 'r') as f:
    input_data = f.read()

# Parsea el input
result = parser.parse(input_data)

# Imprime el resultado de parseo
if errorFlag == False:
    print("Se compilo correctamente")
else:
	print("No se compilo correctamente")

