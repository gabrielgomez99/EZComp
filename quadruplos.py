from cuboSemantico import cuboSemantico as Cubo
from cuboSemantico import Conversion

class quadruplo :
    def __init__(self,operator,op1,op2,res):
        self.operator = operator
        self.op1 = op1
        self.op2 = op2
        self.res = res

    def Imprimir(self,i):
        print(i,'(',(list(Conversion.keys())[list(Conversion.values()).index(self.operator)]),',',self.op1,',',self.op2,',',self.res,')')

class listQuads :
    def __init__(self):
        self.lista = [] #Se inicializa una lista para poder guardar un objeto quadruplo en cada indice
        self.types = [] #Stack que guarda el tipo
        self.operandos = [] #Stack que guarda los operandos
        self.operator = [] #Stack que guarda los operadores
        self.jumps = [] #Stack que guarda los saltos
        self.resTemp = 0 #Stack que guarda los resultados
        self.pointer = 0 #Nos apunta hacia adelante de la instruccion que hicimos
        self.tempVControl = [] #Sirve para poder controlar la variable de control de los For loops
        self.arrPointer = 10000

# Aqui se inserta todo a sus listas
    def pushOperando_Type(self,newOperando, newType):
        print("push operando", newOperando,"push type",newType)
        self.operandos.append(newOperando)
        self.types.append(newType)

    def pushOperator(self, newOperator):
        print("push operator", newOperator)
        self.operator.append(newOperator)

    def pushJump(self):
        print("push jump", (self.pointer))
        self.jumps.append((self.pointer))

    # Pop de Stacks
    def popOperator(self):
        operator = self.operator.pop()
        print("pop Operator",operator)
        return operator

    def popOperando(self):
        operando = self.operandos.pop()
        print("pop operando",operando)
        return operando

    def popType(self):
        return self.types.pop()

    def popJump(self):
        print("pop jump",self.getJump())
        return self.jumps.pop()

    def popParen(self):
        try:
            self.operator.pop(self.operator.index(Conversion['(']))
        except ValueError:
            print("Not Found")

    # Aparramos con la posision anterior
    def getOperator(self):
        try:
            return self.operator[-1]
        except IndexError:
            pass

    def getOperando(self):
        return self.operandos[-1]

    def getType(self):
        return self.types[-1]

    def getJump(self):
        return self.jumps[-1]

    def getPointer(self):
        return self.pointer

    # Se Valida tipos
    def checkTypeMismatch(self):
        operator = self.getOperator()
        rightType = self.popType()
        leftType = self.popType()
        try:
            if (Cubo[leftType][rightType][operator]):
                self.types.append(Cubo[leftType][rightType][operator])
        except:
            print(leftType,rightType,operator)
            print("ERROR: TypeMismatch")
            exit()

    def checkTypeMismatchP(self,leftType,rightType,operator):
        try:
            if (Cubo[leftType][rightType][operator]):
                self.types.append(Cubo[leftType][rightType][operator])
        except:
            print(leftType,rightType,operator)
            print("ERROR: TypeMismatch")
            exit()

    def dumpQuad(self,dirTemp):
        operator = self.popOperator()
        if not operator == Conversion['=']:
            rightOp = self.operandos.pop()
            leftOp = self.operandos.pop()
            self.lista.append(quadruplo(operator,leftOp,rightOp,dirTemp))
            self.pushOperando_Type(dirTemp,self.popType())
        else:
            self.lista.append(quadruplo(operator,dirTemp,None,self.popOperando()))
            #self.pushOperando_Type(self.popOperando(),self.popType())
        self.pointer += 1

    def genQuadVar1Dim(self):
        self.lista.append(quadruplo(Conversion['+'],dir,self.getOperando(),self.arrPointer))
        self.lista.append(quadruplo(Conversion['ARREGLO'],None,None,self.popOperando()))
        self.pushOperando_Type(self.arrPointer,Conversion['int'])
        self.pointer += 1
        self.arrPointer += 1
        self.pushOperando_Type(dir,Conversion['int'])

    def genQuadVar2Dim(self,dir):
        self.lista.append(quadruplo(Conversion['*'],self.popOperando(),self.popOperando(),dir))
        self.pointer += 1
        self.lista.append(quadruplo(Conversion['+'],dir,self.getOperando(),self.arrPointer))
        self.pointer += 1
        self.lista.append(quadruplo(Conversion['ARREGLO'],None,None,self.popOperando()))
        self.pushOperando_Type((self.arrPointer),Conversion['int'])
        self.arrPointer += 1
        

    def dumpQuadLL(self,dir):
        operator = self.popOperator()
        self.lista.append(quadruplo(operator,dir,None,self.popOperando()))
        #self.pushOperando_Type(self.popOperando(),self.popType())
        self.pointer += 1

    def pushGoToMain(self):
        self.lista.append(quadruplo(self.operator.pop(),None,None,'main'))
        self.pointer += 1
    
    def solveGoToMain(self):
        self.lista[0].res = f'${self.pointer}'

    def push_GoTo(self,):
        self.lista.append(quadruplo(self.operator.pop(),self.lista[len(self.lista)-1].res,None,None))
        self.pointer += 1

    def solveGoTo(self):
        self.lista[self.popJump()].res = f'${self.pointer}'

    def push_GoToF(self):
        resType = self.popType()
        if (resType == Conversion['bool']):
            operator = self.popOperator()
            prevRes = self.popOperando()
            self.lista.append(quadruplo(operator, prevRes, None, None))
            self.pointer += 1
        else:
            print(f"ERROR: Expression type must be of type bool, not {(list(Conversion.keys())[list(Conversion.values()).index(resType)])}.")
            exit()

    def solveGoToF(self):
        self.lista[self.popJump()].res = f'${self.pointer + 1}'

    def solveWhile(self):
        end = self.popJump()
        ret = self.popJump()
        self.lista.append(quadruplo(self.operator.pop(),None,None,f'${ret}'))
        self.pointer += 1
        self.lista[end-1].res = f'${self.pointer}'

    def solveExpFor(self):
        operator = self.popOperator()
        rightType = self.popType()
        vControl = self.popOperando()
        if(rightType == Conversion['int'] or rightType == Conversion['float']):
            exp = self.popOperando()
            controlType = self.getType()
            self.resTemp += 1
            typeFinal = self.checkTypeMismatchP(controlType,rightType,operator)
            self.tempVControl.append(vControl)
            self.lista.append(quadruplo(operator,exp,None,vControl))
            self.pushOperando_Type(vControl,typeFinal)
            self.pointer += 1
        else:
            print(f"ERROR: Expression type must be numeric, not {(list(Conversion.keys())[list(Conversion.values()).index(rightType)])}.")
            exit() 

    def solveCondicionFor(self):
        tx = self.popOperando()
        rightType = self.popType()
        if(rightType == Conversion['int'] or rightType == Conversion['float']):
            vFinal = self.popOperando()
            self.resTemp +=1
            #aqui se asigna la expresiona vFinal para seguir checando que se cumpla
            self.lista.append(quadruplo(Conversion['='],self.popOperando(),None,vFinal))
            self.pointer += 1
            self.resTemp +=1
            #Aqui se revisa se se paso de la variable final
            self.lista.append(quadruplo(Conversion['<'],self.popOperando(),vFinal,tx))
            self.pushJump()
            self.pointer += 1
            self.lista.append(quadruplo(Conversion['GoToF'],self.lista[self.pointer-1].res,None,None))
            self.pushJump()
            self.pointer += 1
        else:
            print(f"ERROR: Expression type must be numeric, not {(list(Conversion.keys())[list(Conversion.values()).index(rightType)])}.")
            exit() 

    def finalFor(self):
        self.resTemp += 1
        ty = self.popOperando()
        #Aqui se incrementa la var de control en ty
        self.lista.append(quadruplo(Conversion['+'],self.tempVControl[-1],self.popOperando(),ty))
        self.pointer += 1
        self.resTemp += 1
        #aqui se pone el valor de ty en vControl
        self.lista.append(quadruplo(Conversion['='],ty,None,self.tempVControl[-1]))
        self.pointer += 1
        #aqui se deja el ty con el id original
        self.lista.append(quadruplo(Conversion['='],ty,None,self.popOperando()))
        self.pointer += 1
        fin = self.popJump()
        ret = self.popJump()
        self.lista.append(quadruplo(Conversion['GoTo'],None,None,f'${ret}'))
        self.pointer += 1
        self.lista[fin].res = f'${self.pointer}'
        self.popType()
        self.tempVControl.pop()

    def solveRead(self):
        self.lista.append(quadruplo(Conversion['Read'],None,None,self.operandos.pop()))
        self.pointer += 1

    def solvePrint(self):
        self.lista.append(quadruplo(Conversion['Print'],None,None,self.operandos.pop()))
        self.pointer += 1

    def solveEndFunc(self):
        self.lista.append(quadruplo(self.popOperator(),None,None,None))
        self.pointer += 1

    def pushERA(self, id):
        self.lista.append(quadruplo(self.popOperator(),None,None,id))
        self.pointer += 1

    def solveParam(self):
        self.lista.append(quadruplo(self.popOperator(),None,None,self.popOperando()))
        self.pointer += 1

    def pushGoSub(self, dir):
        self.lista.append(quadruplo(Conversion['GoSub'],None,None,f'${dir}'))
        self.pointer += 1

    def pushParcheGuadalupano(self,dir,id):
        self.lista.append(quadruplo(Conversion['='],dir,None,id))
        self.pointer += 1

    def pushReturn(self,type):
        if(type==Conversion['void']):
            print(f"ERROR: Function is void type, return is not allowed")
            exit()
        else:
            self.checkTypeMismatchP(type,self.getType(),Conversion['='])
            self.lista.append(quadruplo(self.popOperator(),None,None,self.popOperando()))
            self.pointer += 1
    
    def pushReturnLL(self,type,id):
        if(type==Conversion['void']):
            print(f"ERROR: Function is void type, return is not allowed")
            exit()
        else:
            self.lista.append(quadruplo(self.popOperator(),None,None,id))
            self.pointer += 1

    def genQuadFEsp(self):
        self.lista.append(quadruplo(self.popOperator(),None,None,self.popOperando()))

    def genEnd(self):
        self.lista.append(quadruplo(Conversion['END'],None,None,None))
        self.pointer += 1


    def imprimirQuadruplos(self):
        for i in range(len(self.lista)):
            self.lista[i].Imprimir(i)

    def imprimirQuadStacks(self):
        print(self.lista)
        print(self.operandos)
        print(self.operator)
        print(self.jumps)
        print(self.resTemp)
        print(self.pointer)

