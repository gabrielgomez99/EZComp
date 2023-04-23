import ply.yacc as yacc
from lex import tokens
from lex import literals

# Empieza el programa
def p_PROGRAMA_START(p):
	'''
	PROGRAMA_START	: DEC_VAR PROGRAMA_START_1 MAIN '{' DEC_VAR BLOQUE '}'
	'''
def p_PROGRAMA_START_1(p):
	'''
	PROGRAMA_START_1	: FUNCION PROGRAMA_START_1 
		| empty
	'''

def p_FUNCION(p):
	'''
	FUNCION	: FUNC FUNCION_1 ID '(' PARAM ')' '{' DEC_VAR BLOQUE '}'
	'''
	
def p_FUNCION_1(p):
	'''
	FUNCION_1	: VOID 
		| TIPO_SIMPLE
	'''

def p_PARAM(p):
	'''
	PARAM	: TIPO_SIMPLE ID PARAM_1 
		| empty
	'''

def p_PARAM_1(p):
	'''
	PARAM_1	: ',' TIPO_SIMPLE ID PARAM_1 
		| empty
	'''

def p_BLOQUE(p):
	'''
	BLOQUE	:  ESTATUTO BLOQUE
		| empty
	'''

def p_ESTATUTO(p):
	'''
	ESTATUTO	: ASIGNACION
        	| CONDICION
		| ESCRITURA
		| LECTURA
		| WHILE_C
		| FOR_C
		| LLAMADA
		| FUNC_ESPECIALES
		| COMM
		| RETURN_F
	'''

def p_ASIGNACION(p):
	'''
	ASIGNACION	: VARIABLE '=' EXP ';'
	'''	

def p_CONDICION(p):
	'''
	CONDICION	: IF '(' EXP ')' '{' BLOQUE '}' CONDICION_1
	'''	
def p_CONDICION_1(p):
	'''
	CONDICION_1	: ELSE '{' BLOQUE '}'
    	| empty
	'''	

def p_ESCRITURA(p):
	'''
	ESCRITURA	: PRINT '(' ESCRITURA_1 ')' ';'
	'''	
def p_ESCRITURA_1(p):
	'''
	ESCRITURA_1	: EXP ESCRITURA_2
        | CTESTRING ESCRITURA_2
	'''	
def p_ESCRITURA_2(p):
	'''
	ESCRITURA_2	: ',' ESCRITURA_1
    	| empty
	'''	

def p_LECTURA(p):
	'''
	LECTURA	: READ '(' VARIABLE ')' ';'
	'''	

def p_LLAMADA(p):
	'''
	LLAMADA	: ID '(' LLAMADA_1 ')' ';'
	'''	
def p_LLAMADA_1(p):
	'''
	LLAMADA_1	:  EXP LLAMADA_2
		| empty
	'''
def p_LLAMADA_2(p):
	'''
	LLAMADA_2	: ',' EXP LLAMADA_2
		| empty
	'''

def p_WHILE_C(p):
	'''
	WHILE_C	: WHILE '(' EXP ')' '{' BLOQUE '}'
	'''

def p_FOR_C(p):
	'''
	FOR_C	: FOR '(' ID '=' EXP ';' EXP ';' ASIGNACION ')' '{' BLOQUE '}'
	'''

def p_DEC_VAR(p):
	'''
	DEC_VAR	: VARS DEC_VAR
		| ARREGLO DEC_VAR
		| empty
	'''

def p_VARS(p):
	'''
	VARS	: VAR VARS_1 ID VARS_2 ';'
	'''	

def p_VARS_1(p):
	'''
	VARS_1	:  TIPO_COMPUESTO
		| TIPO_SIMPLE
	'''

def p_VARS_2(p):
	'''
	VARS_2	:  ',' ID VARS_2
		| empty
	'''

def p_ARREGLO(p):
	'''
	ARREGLO	: ARR TIPO_SIMPLE ID '[' CTEINT ']' ARREGLO_1 ';'
	'''	

def p_ARREGLO_1(p):
	'''
	ARREGLO_1	: '[' CTEINT ']' ARREGLO_1
		| empty
	'''	

def p_TIPO_SIMPLE(p):
	'''
	TIPO_SIMPLE	: FLOAT
    		| INT
	    | CTESTRING
	'''

def p_TIPO_COMPUESTO(p):
	'''
	TIPO_COMPUESTO	: FILE
    	| DATAFRAME
	'''

def p_VARIABLE(p):
	'''
	VARIABLE	: ID VARIABLE_1
	'''	
def p_VARIABLE_1(p):
	'''
	VARIABLE_1	: '[' EXP ']' VARIABLE_2
    	| empty
	'''	
def p_VARIABLE_2(p):
	'''
	VARIABLE_2	: '[' EXP ']'
    	| empty
	'''			
	
def p_EXP(p):
	'''
	EXP	: T_EXP EXP_1
	'''	
def p_EXP_1(p):
	'''
	EXP_1	: OR EXP
        | empty
	'''	

def p_T_EXP(p):
	'''
	T_EXP	: G_EXP T_EXP_1
	'''
def p_T_EXP_1(p):
	'''
	T_EXP_1	: '&' G_EXP
        | empty
	'''	

def p_G_EXP(p):
	'''
	G_EXP	: M_EXP G_EXP_1
	'''	

def p_G_EXP_1(p):
	'''
	G_EXP_1	: '<' M_EXP
        	| '>' M_EXP
		| EQUALS M_EXP
		| NE M_EXP
		| LESSEQ M_EXP
		| MOREEQ M_EXP
		| empty 
	'''		

def p_M_EXP(p):
	'''
	M_EXP	: T M_EXP_1
	'''	
def p_M_EXP_1(p):
	'''
	M_EXP_1	: '+' M_EXP
		| '-' M_EXP
        	| empty
	'''

def p_T(p):
	'''
	T	: F T_1
	'''			
def p_T_1(p):
	'''
	T_1	: '*' T
        	| '/' T
		| empty
	'''

def p_F(p):
	'''
	F	: '(' EXP ')'
        	| CTEFLOAT
		| CTEINT
		| VARIABLE
		| LLAMADA
	'''

def p_FUNC_ESPECIALES(p):
	'''
	FUNC_ESPECIALES	: MEAN_F
        	| MEDIAN_F
		| MODE_F
		| VARIANCE_F
		| STANDARD_DEV
		| HISTOGRAMA
	'''

def p_MEAN_F(p):
	'''
	MEAN_F	: MEAN '(' VARIABLE ')' ';'
	'''	

def p_MEDIAN_F(p):
	'''
	MEDIAN_F	: MEDIAN '(' VARIABLE ')' ';'
	'''	

def p_MODE_F(p):
	'''
	MODE_F	: MODE '(' VARIABLE ')' ';'
	'''	

def p_VARIANCE_F(p):
	'''
	VARIANCE_F	: VARIANCE '(' VARIABLE ')' ';'
	'''	

def p_STANDARD_DEV(p):
	'''
	STANDARD_DEV	: STDDEV '(' VARIABLE ')' ';'
	'''		

def p_HISTOGRAMA(p):
	'''
	HISTOGRAMA	: HISTOGRAM '(' VARIABLE ')' ';'
	'''	

def p_RETURN_F(p):
	'''
	RETURN_F	: RETURN EXP ';' 
	'''	

# Empty symbol = ε
def p_COMM(p):
	'''
	COMM	: COMMENT
	'''

# Empty symbol = ε
def p_empty(p):
	'''
	empty	: 
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

