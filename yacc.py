import ply.yacc as yacc
import queue
import pickle
from cuboSemantico import Conversion
from quadruplos import listQuads
from lex import tokens
from lex import literals
from cuboSemantico import cuboSemantico
from memoriaVirtual import memoria
from tablas import tablaVar
from tablas import tablaFunc
from tablas import dictFunc
from maquinaVirtual import maquinaVirtual

tempQDecVar = queue.Queue()
tempTipo = ''
tempYAxis = 0
dim = 1
tempId = ''
seenAxis = False
tempScope = 0
tempVars = tablaVar()
tempTipoFunc = 0
tempIdFunc = 'Global'
tempFuncion = tablaFunc(0,0)
dictFunciones = dictFunc()
quads = listQuads()
elseFlag = True
mem = memoria()
esLlamada = False
stackLlamadaId = []


# Empieza el programa
def p_PROGRAMA_START(p):
	'''
	PROGRAMA_START	: meter_GoToMain DEC_VAR meter_DecVar_a_func meter_a_MemGlobal quitar_Global PROGRAMA_START_1 MAIN solve_GoToMain '{' DEC_VAR meter_DecVar_a_func meter_a_MemV BLOQUE endProg '}'
	'''
def p_PROGRAMA_START_1(p):
	'''
	PROGRAMA_START_1	: FUNCION PROGRAMA_START_1 
		| empty
	'''	

def p_FUNCION(p):
	'''
	FUNCION	: FUNC FUNCION_1 ID seen_IdFunc '(' PARAM ')' '{' DEC_VAR meter_DecVar_a_func BLOQUE meter_endfunc '}'
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
	ASIGNACION	: VARIABLE '=' push_Op ASIGNACION_1 solve_Asig ';'
	'''	
def p_ASIGNACION_1(p):
	'''
	ASIGNACION_1	: EXP 
	'''	

def p_CONDICION(p):
	'''
	CONDICION	: IF '(' EXP meter_jump meter_GoToF ')' '{' BLOQUE '}' CONDICION_1 solve_GoToF
	'''	
def p_CONDICION_1(p):
	'''
	CONDICION_1	: ELSE '{' solve_GoToFElse meter_jump meter_GoTo BLOQUE '}' solve_GoTo
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
	LECTURA	: READ '(' VARIABLE solve_read ')' ';'
	'''	

def p_LLAMADA(p):
	'''
	LLAMADA	: ID meter_ERA '(' LLAMADA_1 meter_GoSub ')' es_llamada
	'''		
def p_LLAMADA_1(p):
	'''
	LLAMADA_1	:  EXP meter_param LLAMADA_2
		| empty
	'''
def p_LLAMADA_2(p):
	'''
	LLAMADA_2	: ',' EXP meter_param LLAMADA_2
		| empty
	'''

def p_WHILE_C(p):
	'''
	WHILE_C	: WHILE '(' meter_jump EXP meter_GoToF  meter_jump ')' '{' BLOQUE solve_While '}'
	'''

def p_FOR_C(p):
	'''
	FOR_C	: FOR '(' ID push_Id '=' push_Op EXP meter_expFor ';' EXP checar_condicionFor ')' '{' BLOQUE final_for '}'
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
	ARREGLO	: ARR TIPO_SIMPLE ID seen_Id '[' CTEINT seen_xAxis ']' ARREGLO_1 dec_yAxis meter_Dec_Arr ';'
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
	VARIABLE	: ID pushID VARIABLE_1 solveVar
	'''
def p_VARIABLE_1(p):
	'''
	VARIABLE_1	: '[' insert_Paren checarDim EXP ']' pop_Paren VARIABLE_2
    	| empty
	'''	
def p_VARIABLE_2(p):
	'''
	VARIABLE_2	: '[' insert_Paren checarDimY EXP ']' pop_Paren
    	| empty
	'''			
def p_pushID(p):
	'''
	pushID	: 
	'''	
	global tempId
	tempId = p[-1]
	quads.pushOperando_Type(dictFunciones.getVarDir(tempId),dictFunciones.getVarType(tempId))

def p_checarDim(p):
	'''
	checarDim	: 
	'''	
	global dim
	if(dictFunciones.list[-1].tablaDeVariables[tempId]['xAxis'] > 1):
		pass
	else:
		print('ERROR: Variable solo tiene una dimension')
		exit()
	dim += 1
		
def p_checarDimY(p):
	'''
	checarDimY	: 
	'''	
	global dim
	if(dictFunciones.list[-1].tablaDeVariables[tempId]['yAxis'] > 1):
		pass
	else:
		print('ERROR: Variable solo tiene dos dimension')
		exit()
	dim += 1

def p_solveVar(p):
	'''
	solveVar	: 
	'''	
	global dim
	if(dim == 2):
		quads.genQuadVar1Dim()
		mem.addVarGlobal(quads.arrPointer-1)
		dim = 0
	elif(dim == 3):
		quads.genQuadVar2Dim(dictFunciones.list[-1].addTemp(Conversion['int']))
		mem.addVarGlobal(quads.arrPointer-1)
		dim = 0

def p_EXP(p):
	'''
	EXP	: T_EXP EXP_1 solve_EXP update_memVmain
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
	RETURN_F	: RETURN EXP meter_Return ';' 
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
	global tempFuncion, tempIdFunc
	tempIdFunc = p[-1]
	tempFuncion = tablaFunc(tempTipoFunc,tempIdFunc)
	tempFuncion.dir = quads.pointer #se usa para cuando se cree la funcion le asignamos la direccion donde inicia

def p_seen_Param(p):
	'''
	seen_Param	: 
	'''
	global tempFuncion
	tempFuncion.addParam(tempTipo,tempId,0)

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
	tempQDecVar.put(1)
	tempQDecVar.put(1)

def p_meter_Dec_Var(p):
	'''
	meter_Dec_Var	: 
	'''
	global tempQDecVar
	tempVars.addVar(tempQDecVar.get(),tempQDecVar.get(),tempQDecVar.get(),tempQDecVar.get(),tempQDecVar.get(),tempFuncion.ints,tempFuncion.floats,tempFuncion.chars)

def p_meter_Dec_Arr(p):
	'''
	meter_Dec_Arr	: 
	'''
	global tempQDecVar
	tempVars.addMat(tempQDecVar.get(),tempQDecVar.get(),tempQDecVar.get(),tempQDecVar.get(),tempQDecVar.get())

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
	if(seenAxis):
		tempQDecVar.put(tempYAxis)
	else:
		tempYAxis = 1
		tempQDecVar.put(tempYAxis)

def p_seen_yAxis(p):
	'''
	seen_yAxis	: 
	'''	
	global tempYAxis, seenAxis
	seenAxis = True
	tempYAxis = p[-1]

def p_meter_a_MemV(p):
	'''
	meter_a_MemV	: 
	'''	
	for key in (dictFunciones.list[len(dictFunciones.list)-1].tablaDeVariables.keys()):
		mem.addVar(dictFunciones.list[len(dictFunciones.list)-1].tablaDeVariables[key]['dir'])
	mem.addToMemory()

def p_meter_a_MemGlobal(p):
	'''
	meter_a_MemGlobal	: 
	'''	
	for key in (dictFunciones.list[0].tablaDeVariables.keys()):
		mem.addVarGlobal(dictFunciones.list[len(dictFunciones.list)-1].tablaDeVariables[key]['dir'])
	
def p_update_memVmain(p):
	'''
	update_memVmain	: 
	'''	
	if(len(mem.memory)>0):
		mem.updateMain()

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
	global esLlamada
	if(esLlamada):
		temp = stackLlamadaId.pop()
		for i in range (len(dictFunciones.list)):
			if(temp == dictFunciones.list[i].id):
				#mem.addVarGlobalType(dictFunciones.list[i].type)
				dirTemp = quads.lista[quads.pointer-1].op1
		quads.dumpQuadLL(dirTemp)
		esLlamada = False
	else:
		mem.addVar(quads.getOperando())
		quads.dumpQuad(quads.popOperando())

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
	quads.push_GoToF()

def p_meter_GoTo(p):
	'''
	meter_GoTo	: 
	'''	
	quads.pushOperator(Conversion['GoTo'])
	quads.push_GoTo()

def p_solve_GoTo(p):
	'''
	solve_GoTo	: 
	'''	
	quads.solveGoTo()

def p_solve_GoToF(p):
	'''
	solve_GoToF : 
	'''
	#Se hace cuando no hay else en el estatuto Condicion
	global elseFlag
	#Se revisa si ya se visito el else y alfinal se cambia la flag para el siguiente gotoF
	if(elseFlag):
		quads.solveGoTo()
		elseFlag = False
	else:
		elseFlag = True

def p_solve_GoToFElse(p):
	'''
	solve_GoToFElse	: 
	'''	
	#Se hace si hay else en el estatuto Condicion para meter el pointer + 1 para saltar el Goto de else
	global elseFlag
	#Se revisa si ya se visito el else y alfinal se cambia la flag para el siguiente gotoF
	if(elseFlag):
		quads.solveGoToF()
		elseFlag = False
	else:
		elseFlag = True

def p_solve_While(p):
	'''
	solve_While	: 
	'''	
	quads.pushOperator(Conversion['GoTo'])
	quads.solveWhile()

def p_push_Id(p):
	'''
	push_Id	: 
	'''	
	temp = dictFunciones.getVarDir(p[-1])
	if(dictFunciones.getVarType(p[-1]) == Conversion['int'] or dictFunciones.getVarType(p[-1]) == Conversion['float']):
		quads.pushOperando_Type(temp,dictFunciones.getVarType(p[-1]))

def p_meter_expFor(p):
	'''
	meter_expFor	: 
	'''	
	#se crea una variable entera para variable de control para el GoToF
	dirTemp = dictFunciones.list[-1].addTemp(Conversion['int'])
	quads.operandos.append(dirTemp)
	quads.solveExpFor()

def p_checar_condicionFor(p):
	'''
	checar_condicionFor	: 
	'''	
	#se crea una variable entera para variable de tx para el GoToF
	dirTemp = dictFunciones.list[-1].addTemp(Conversion['int'])
	quads.operandos.append(dirTemp)
	dirTemp = dictFunciones.list[-1].addTemp(Conversion['bool'])#se crea una variable booleana para el GoToF
	quads.operandos.append(dirTemp)
	quads.solveCondicionFor()

def p_final_for(p):
	'''
	final_for	: 
	'''	
	dirTemp = dictFunciones.list[-1].addTemp(Conversion['int'])
	if(not mem.searchDirConstantes(1)):
		mem.addConst(1,Conversion['int'])
	quads.operandos.append(mem.searchDirConstantes(1))
	quads.operandos.append(dirTemp)
	quads.finalFor()

def p_solve_read(p):
	'''
	solve_read	: 
	'''	
	quads.solveRead()

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
	quads.solvePrint()

def p_meter_endfunc(p):
	'''
	meter_endfunc	: 
	'''	
	quads.pushOperator(Conversion['EndFunc'])
	dictFunciones.list[-1].fin = quads.pointer
	quads.solveEndFunc()

def p_meter_ERA(p):
	'''
	meter_ERA	:
	'''	
	global stackLlamadaId
	flag = False
	idTemp = 0
	quads.pushOperator(Conversion['ERA'])
	for i in range(len(dictFunciones.list)):
		if(dictFunciones.list[i].id == p[-1]):
			idTemp = dictFunciones.list[i].id
			stackLlamadaId.append(idTemp)
			quads.pushERA(idTemp)
			flag = True
			break
	if(flag):
		pass
	else:
		print("Error funcion no declarada")	
		exit()

def p_meter_param(p):
	'''
	meter_param	: 
	'''	
	quads.pushOperator(Conversion['Param'])
	quads.solveParam()

def p_meter_GoSub(p):
	'''
	meter_GoSub	: 
	'''	
	global indiceGoSub
	flag = False
	for i in range(len(dictFunciones.list)):
		if(dictFunciones.list[i].id == p[-4]):
			quads.pushGoSub(dictFunciones.list[i].dir)
			if(not dictFunciones.list[i].type == Conversion['void']):
				id = dictFunciones.list[i].id
				if(dictFunciones.list[i].type == Conversion['int']):
					quads.pushParcheGuadalupano((dictFunciones.list[i].addTemp(Conversion['int'])),id)
				if(dictFunciones.list[i].type == Conversion['float']):
					quads.pushParcheGuadalupano((dictFunciones.list[i].floats+3000),id)
				if(dictFunciones.list[i].type == Conversion['char']):
					quads.pushParcheGuadalupano((dictFunciones.list[i].char+4000),id)
			flag = True
	if(flag):
		pass
	else:
		print("Error funcion no declarada")	

def p_meter_Return(p):
	'''
	meter_Return	: 
	'''
	global esLlamada
	quads.pushOperator(Conversion['Return'])
	if(not dictFunciones.list[-1].type == Conversion['void']):
		if(esLlamada):
			quads.pushReturnLL(dictFunciones.list[len(dictFunciones.list)-1].type,dictFunciones.list[len(dictFunciones.list)-1].id)
			esLlamada = False
		else:
			quads.pushReturn(dictFunciones.list[len(dictFunciones.list)-1].type,dictFunciones.list[len(dictFunciones.list)-1].id)
	else:
		print('ERROR: No se puede hacer return en funcion VOID')
		exit()
		
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
	constFlag = True
	for value in mem.constants.values():
		if value == p[-1]:
			constFlag = False
	if constFlag:
		mem.addConst(Conversion['int'],p[-1])
	quads.pushOperando_Type(mem.searchDirConstantes(p[-1]),Conversion['int'])

def p_push_operando_F(p):
	'''
	push_operando_F	: 
	'''	
	constFlag = True
	for value in mem.constants.values():
		if value == p[-1]:
			constFlag = False
	if constFlag:
		mem.addConst(Conversion['float'],p[-1])
	quads.pushOperando_Type(mem.searchDirConstantes(p[-1]),Conversion['float'])

def p_es_llamada(p):
	'''
	es_llamada	: 
	'''	
	global esLlamada 
	esLlamada = True

def p_solve_EXP(p):
	'''
	solve_EXP	: 
	'''	
	global quads
	if (quads.getOperator() == Conversion['||']):
		quads.checkTypeMismatch()
		#Se toma el type que se pusheo en CheckTypeMismatch yluego se suma a los contadores de su tipo y se asigna direccion
		dirTemp = dictFunciones.list[len(dictFunciones.list)-1].addTemp(quads.getType())
		mem.addVar(dirTemp)
		quads.dumpQuad(dirTemp)

def p_solve_T_EXP(p):
	'''
	solve_T_EXP	: 
	'''	
	global quads
	if (quads.getOperator() == Conversion['&']):
		quads.checkTypeMismatch()
		#Se toma el type que se pusheo en CheckTypeMismatch yluego se suma a los contadores de su tipo y se asigna direccion
		dirTemp = dictFunciones.list[len(dictFunciones.list)-1].addTemp(quads.getType())
		mem.addVar(dirTemp)
		quads.dumpQuad(dirTemp)

	
def p_solve_G_EXP(p):
	'''
	solve_G_EXP	: 
	'''	
	global quads
	if (quads.getOperator() == Conversion['<'] or quads.getOperator() == Conversion['>'] or quads.getOperator() == Conversion['=='] or quads.getOperator() == Conversion['!='] or quads.getOperator() == Conversion['<='] or quads.getOperator() == Conversion['>=']):
		quads.checkTypeMismatch()
		#Se toma el type que se pusheo en CheckTypeMismatch yluego se suma a los contadores de su tipo y se asigna direccion
		dirTemp = dictFunciones.list[len(dictFunciones.list)-1].addTemp(quads.getType())
		mem.addVar(dirTemp)
		quads.dumpQuad(dirTemp)

def p_solve_M_EXP(p):
	'''
	solve_M_EXP	: 
	'''	
	if (quads.getOperator() == Conversion['+'] or quads.getOperator() == Conversion['-']):
		quads.checkTypeMismatch()
		#Se toma el type que se pusheo en CheckTypeMismatch yluego se suma a los contadores de su tipo y se asigna direccion
		dirTemp = dictFunciones.list[len(dictFunciones.list)-1].addTemp(quads.getType())
		mem.addVar(dirTemp)
		quads.dumpQuad(dirTemp)

def p_solve_T(p):
	'''
	solve_T	: 
	'''	
	global quads
	if (quads.getOperator() == Conversion['*'] or quads.getOperator() == Conversion['/']):

		quads.checkTypeMismatch()
		#Se toma el type que se pusheo en CheckTypeMismatch yluego se suma a los contadores de su tipo y se asigna direccion
		dirTemp = dictFunciones.list[len(dictFunciones.list)-1].addTemp(quads.getType())
		mem.addVar(dirTemp)
		quads.dumpQuad(dirTemp)

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

def p_endProg(p):
	'''
	endProg	: 
	'''	
	for key in ((dictFunciones.list[-1].tablaDeVariables.keys())):
		xAxis = dictFunciones.list[-1].tablaDeVariables[key]['xAxis']
		yAxis = dictFunciones.list[-1].tablaDeVariables[key]['yAxis']
		for k in range(xAxis*yAxis):
			mem.addVar(dictFunciones.list[-1].tablaDeVariables[key]['dir']+k)
	for key in ((dictFunciones.list[-1].temps.keys())):
		mem.addVar(key)
	mem.updateMain()
	quads.genEnd()

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

text = input("Ingresa archivo con extension .txt para leer: ")

# Lee de un archivo de entrada
with open(text, 'r') as f:
    input_data = f.read()

# Parsea el input
result = parser.parse(input_data)

with open('data.obj','wb') as file:
	pickle.dump({'quadruplos': quads.lista,'funcDir':dictFunciones.list,'memory':mem},file)
maquina = maquinaVirtual()

# Imprime el resultado de parseo
if errorFlag == False:
    print("Se compilo correctamente")
    quads.imprimirQuadruplos()
    #quads.imprimirQuadStacks()
    #mem.printMem()
    """ for i in range(len(dictFunciones.list)):
    	dictFunciones.list[i].imprimirFunc() """
    maquina.startMaquinaVirtual()
else:
	print("No se compilo correctamente")

