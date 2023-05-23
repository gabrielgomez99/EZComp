import ply.yacc as yacc
import queue
from cuboSemantico import Conversion
from quadruplos import listQuads
from lex import tokens
from lex import literals
from cuboSemantico import cuboSemantico
from tablas import tablaVar
from tablas import tablaFunc
from tablas import dictFunc

tempQDecVar = queue.Queue()
tempTipo = ''
tempYAxis = 0
tempScope = 0
tempVars = tablaVar()
tempTipoFunc = 0
tempFuncion = tablaFunc(0,0)
dictFunciones = dictFunc()
quads = listQuads()


# Empieza el programa
def p_PROGRAMA_START(p):
	'''
	PROGRAMA_START	: meter_GoToMain DEC_VAR meter_DecVar_a_func quitar_Global PROGRAMA_START_1 MAIN solve_GoToMain '{' DEC_VAR meter_DecVar_a_func BLOQUE '}'
	'''
def p_PROGRAMA_START_1(p):
	'''
	PROGRAMA_START_1	: FUNCION PROGRAMA_START_1 
		| empty
	'''	

def p_FUNCION(p):
	'''
	FUNCION	: FUNC FUNCION_1 ID seen_IdFunc '(' PARAM ')' '{' DEC_VAR meter_DecVar_a_func BLOQUE '}'
	'''
	
def p_FUNCION_1(p):
	'''
	FUNCION_1	: VOID seen_void
		| TIPO_SIMPLE
	'''

def p_PARAM(p):
	'''
	PARAM	: TIPO_SIMPLE ID seen_IdParam seen_Param PARAM_1
		| empty
	'''

def p_PARAM_1(p):
	'''
	PARAM_1	: ',' TIPO_SIMPLE ID seen_IdParam seen_Param PARAM_1 
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
		| RETURN_F
	'''

def p_ASIGNACION(p):
	'''
	ASIGNACION	: VARIABLE '=' push_Op EXP solve_Asig ';'
	'''	

def p_CONDICION(p):
	'''
	CONDICION	: IF '(' EXP meter_jump meter_GoToF ')' '{' BLOQUE '}' solve_GoToF CONDICION_1
	'''	
def p_CONDICION_1(p):
	'''
	CONDICION_1	: ELSE '{' meter_jump meter_GoTo BLOQUE '}' solve_GoTo
    	| empty
	'''	

def p_ESCRITURA(p):
	'''
	ESCRITURA	: PRINT '(' ESCRITURA_1 ')' ';'
	'''	
def p_ESCRITURA_1(p):
	'''
	ESCRITURA_1	: EXP solve_Print ESCRITURA_2
        | CHAR solve_Print_Char ESCRITURA_2
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
	LLAMADA	: ID '(' LLAMADA_1 meter_jump meter_GoSub ')' ';'
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
	VARS	: VAR VARS_1 ID seen_Id dec_axis meter_Dec_Var VARS_2 ';'
	'''	

def p_VARS_1(p):
	'''
	VARS_1	:  TIPO_COMPUESTO
		| TIPO_SIMPLE
	'''

def p_VARS_2(p):
	'''
	VARS_2	:  ',' ID seen_Id dec_axis meter_Dec_Var VARS_2
		| empty
	'''

def p_ARREGLO(p):
	'''
	ARREGLO	: ARR TIPO_SIMPLE ID seen_Id '[' CTEINT seen_xAxis ']' ARREGLO_1 dec_yAxis ';'
	'''	

def p_ARREGLO_1(p):
	'''
	ARREGLO_1	: '[' CTEINT seen_yAxis ']' 
		| empty
	'''	

def p_TIPO_SIMPLE(p):
	'''
	TIPO_SIMPLE	: FLOAT
    		| INT
	    | CHAR
	'''
	global tempTipo, tempTipoFunc
	tempTipoFunc = Conversion[p[1]]
	tempTipo = Conversion[p[1]]

def p_TIPO_COMPUESTO(p):
	'''
	TIPO_COMPUESTO	: FILE
    	| DATAFRAME
	'''
	global tempTipo
	tempTipo = Conversion[p[1]]

def p_VARIABLE(p):
	'''
	VARIABLE	: ID VARIABLE_1
	'''
	quads.pushOperando_Type(p[1],dictFunciones.getVarType(p[1]))
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
	EXP	: T_EXP EXP_1 solve_EXP
	'''	
def p_EXP_1(p):
	'''
	EXP_1	: OR push_Op EXP
        | empty
	'''	

def p_T_EXP(p):
	'''
	T_EXP	: G_EXP T_EXP_1 solve_T_EXP
	'''
def p_T_EXP_1(p):
	'''
	T_EXP_1	: '&' push_Op G_EXP
        | empty
	'''	

def p_G_EXP(p):
	'''
	G_EXP	: M_EXP G_EXP_1 solve_G_EXP
	'''	

def p_G_EXP_1(p):
	'''
	G_EXP_1	: '<' push_Op M_EXP
        	| '>' push_Op M_EXP
		| EQ push_Op M_EXP
		| NE push_Op M_EXP
		| LTEQ push_Op M_EXP
		| GTEQ push_Op M_EXP
		| empty 
	'''		

def p_M_EXP(p):
	'''
	M_EXP	: T solve_M_EXP M_EXP_1 
	'''	
def p_M_EXP_1(p):
	'''
	M_EXP_1	: '+' push_Op M_EXP
		| '-' push_Op M_EXP
        	| empty
	'''

def p_T(p):
	'''
	T	: F solve_T T_1 
	'''			
def p_T_1(p):
	'''
	T_1	: '*' push_Op T
        	| '/' push_Op T
		| empty
	'''

def p_F(p):
	'''
	F	: '(' insert_Paren EXP pop_Paren ')'
        	| CTEFLOAT push_operando_F
		| CTEINT push_operando_I
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

#Puntos Semanticos
#DECVAR
def p_quitar_Global(p):
	'''
	quitar_Global	: 
	'''
	global tempScope
	tempScope = 1

def p_meter_DecVar_a_func(p):
	'''
	meter_DecVar_a_func	: 
	'''
	global dictFunciones, tempFuncion, tempVars
	tempFuncion.addVars(tempVars)
	dictFunciones.agregaFunc(tempFuncion)
	tempFuncion = tablaFunc(0,0)
	tempVars = tablaVar()

def p_seen_void(p):
	'''
	seen_void	:
	'''
	global tempTipoFunc
	tempTipoFunc = Conversion[p[-1]]

def p_seen_IdFunc(p):
	'''
	seen_IdFunc	:
	'''
	global tempFuncion
	tempFuncion = tablaFunc(tempTipoFunc,p[-1])
	tempFuncion.dir = quads.pointer #se usa para cuando se cree la funcion le asignamos la direccion donde inicia

def p_seen_Param(p):
	'''
	seen_Param	: 
	'''
	global tempFuncion
	tempFuncion.addParam(tempTipo,tempId,10,0)

def p_seenId(p):
	'''
	seen_Id	: 
	'''
	global tempQDecVar
	tempQDecVar.put(p[-1]) #Mete el Id
	tempQDecVar.put(tempScope) #Mete si es global o no
	tempQDecVar.put(tempTipo) #Mete el tipo

def p_seenIdParam(p):
	'''
	seen_IdParam	: 
	'''
	global tempId
	tempId = p[-1] #Sirve para guardar id de param

def p_dec_axis(p):
	'''
	dec_axis	: 
	'''
	global tempQDecVar
	#Como no es un tipo arr (no es arreglo) se llena las dimensiones con nada
	tempQDecVar.put(None)
	tempQDecVar.put(None)

def p_meter_Dec_Var(p):
	'''
	meter_Dec_Var	: 
	'''
	global tempQDecVar
	tempQDecVar.put(0) #Temporalmente valor 0
	tempVars.addVar(tempQDecVar.get(),tempQDecVar.get(),tempQDecVar.get(),tempQDecVar.get(),tempQDecVar.get(),tempQDecVar.get())

def p_seen_xAxis(p):
	'''
	seen_xAxis	: 
	'''	
	global tempQDecVar
	tempQDecVar.put(p[-1])

def p_dec_yAxis(p):
	'''
	dec_yAxis	: 
	'''	
	global tempYAxis
	tempQDecVar.put(tempYAxis)
	tempYAxis = 0

def p_seen_yAxis(p):
	'''
	seen_yAxis	: 
	'''	
	global tempYAxis
	tempYAxis = p[-1]

#Estatutos
def p_meter_GoToMain(p):
	'''
	meter_GoToMain	: 
	'''	
	quads.pushOperator(Conversion['GoTo'])
	quads.pushGoToMain()

def p_solve_GoToMain(p):
	'''
	solve_GoToMain	: 
	'''	
	quads.solveGoToMain()

def p_solve_Asig(p):
	'''
	solve_Asig	: 
	'''	
	quads.dumpQuad()

def p_meter_jump(p):
	'''
	meter_jump	: 
	'''	
	quads.pushJump()

def p_meter_GoToF(p):
	'''
	meter_GoToF	: 
	'''	
	quads.pushOperator(Conversion['GoToF'])
	quads.push_GoTo()

def p_meter_GoTo(p):
	'''
	meter_GoTo	: 
	'''	
	quads.pushOperator(Conversion['GoTo'])
	quads.push_GoTo()

def p_solve_GoToF(p):
	'''
	solve_GoToF	: 
	'''	
	quads.solveGoToF()

def p_solve_GoTo(p):
	'''
	solve_GoTo	: 
	'''	
	quads.solveGoTo()

def p_solve_Print(p):
	'''
	solve_Print	: 
	'''	
	quads.solvePrint()

def p_solve_Print_Char(p):
	'''
	solve_Print_Char	: 
	'''	
	quads.pushOperando_Type(p[-1],Conversion['char'])
	quads.solvePrint_Char()

def p_meter_GoSub(p):
	'''
	meter_GoSub	: 
	'''	
	flag = False
	for i in range(len(dictFunciones.list)-1):
		if(dictFunciones.list[i]['func'].id == p[-4]):
			quads.pushGoSub(dictFunciones.list[i]['func'].dir)
			flag = True
	if(flag):
		pass
	else:
		print("Error funcion no declarada")	

#Expresions
def p_push_Op(p):
	'''
	push_Op	: 
	'''	
	quads.pushOperator(Conversion[p[-1]])
	
def p_push_operando_I(p):
	'''
	push_operando_I	: 
	'''	
	quads.pushOperando_Type(p[-1],Conversion['int'])

def p_push_operando_F(p):
	'''
	push_operando_F	: 
	'''	
	quads.pushOperando_Type(p[-1],Conversion['float'])

def p_solve_EXP(p):
	'''
	solve_EXP	: 
	'''	
	global quads
	if (quads.getOperator() == Conversion['||']):
		quads.dumpQuad()

def p_solve_T_EXP(p):
	'''
	solve_T_EXP	: 
	'''	
	global quads
	if (quads.getOperator() == Conversion['&']):
		quads.dumpQuad()

	
def p_solve_G_EXP(p):
	'''
	solve_G_EXP	: 
	'''	
	global quads
	if (quads.getOperator() == Conversion['<'] or quads.getOperator() == Conversion['>'] or quads.getOperator() == Conversion['=='] or quads.getOperator() == Conversion['!='] or quads.getOperator() == Conversion['<='] or quads.getOperator() == Conversion['>=']):
		quads.dumpQuad()

def p_solve_M_EXP(p):
	'''
	solve_M_EXP	: 
	'''	
	if (quads.getOperator() == Conversion['+'] or quads.getOperator() == Conversion['-']):
		quads.dumpQuad()

def p_solve_T(p):
	'''
	solve_T	: 
	'''	
	global quads
	if (quads.getOperator() == Conversion['*'] or quads.getOperator() == Conversion['/']):
		quads.dumpQuad()

def p_insert_Paren(p):
	'''
	insert_Paren	: 
	'''	
	global quads
	quads.pushOperator(Conversion['('])

def p_pop_Paren(p):
	'''
	pop_Paren	: 
	'''	
	global quads
	quads.popParen()

errorFlag = False

# Empty symbol = ε
def p_empty(p):
	'''
	empty	: 
	'''
	pass

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
with open('texto copy.txt', 'r') as f:
    input_data = f.read()

# Parsea el input
result = parser.parse(input_data)

# Imprime el resultado de parseo
if errorFlag == False:
    print("Se compilo correctamente")
    quads.imprimirQuadruplos()
    """ for i in range(len(dictFunciones.list)):
    	dictFunciones.list[i]['func'].imprimirFunc() """
else:
	print("No se compilo correctamente")

