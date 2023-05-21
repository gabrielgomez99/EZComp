from cuboSemantico import cuboSemantico as Cubo
from cuboSemantico import Conversion

class quadruplo :
    def __init__(self,operator,op1,op2,res):
        self.operator = operator
        self.op1 = op1
        self.op2 = op2
        self.res = res

    def Imprimir(self):
        print('(',self.operator,',',self.op1,',',self.op2,',',self.res,')')

class listQuads :
    def __init__(self):
        self.lista = [] #Se inicializa una lista para poder guardar un objeto quadruplo en cada indice
        self.types = [] #Stack que guarda el tipo
        self.operandos = [] #Stack que guarda los operandos
        self.operator = [] #Stack que guarda los operadores
        self.jumps = [] #Stack que guarda los saltos
        self.resTemp = 0 #Stack que guarda los resultados
        self.pointer = 1 #Nos apunta hacia adelante de la instruccion que hicimos

# Aqui se inserta todo a sus listas
    def pushOperando_Type(self,newOperando, newType):
        print("push operando", newOperando,"push type",newType)
        self.operandos.append(newOperando)
        self.types.append(newType)

    def pushOperator(self, newOperator):
        print("push operator", newOperator)
        self.operator.append(newOperator)

    def pushJump(self):
        print("push jump", (self.pointer - 1))
        self.jumps.append((self.pointer - 1))

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
        return self.jumps.pop()

    def popParen(self):
        try:
            self.operator.pop(self.operator.index(Conversion['(']))
        except ValueError:
            print("Not Found")

    # Aparramos con la posision anterior
    def getOperator(self):
        return self.operator[-1]

    def getOperando(self):
        return self.operandos[-1]

    def getType(self):
        return self.operandos[-1]

    def getJump(self):
        return self.operandos[-1]

    def getPointer(self):
        return self.pointer

    # Se Valida tipos
    def checkTypeMismatch(self, leftType, rightType, operator):
        try:
            if (Cubo[leftType][rightType][operator]):
                return Cubo[leftType][rightType][operator]
        except:
            print(leftType,rightType,operator)
            print("ERROR: TypeMismatch")
            exit()

    def dumpQuad(self):
        operator = self.popOperator()
        rightType = self.popType()
        leftType = self.popType()
        typeFinal = self.checkTypeMismatch(leftType, rightType, operator)
        if not operator == Conversion['=']:
            self.resTemp += 1
            rightOp = self.operandos.pop()
            leftOp = self.operandos.pop()
            self.lista.append(quadruplo(operator,leftOp,rightOp,self.resTemp))
            self.pushOperando_Type(self.resTemp,typeFinal)
        else:
            self.resTemp += 1
            self.lista.append(quadruplo(operator,self.operandos.pop(),None,self.operandos.pop()))
            self.pushOperando_Type(self.resTemp,typeFinal)
        self.lista[self.pointer - 1].Imprimir()
        self.pointer += 1

    def pushGoToF(self):
        self.lista.append('GoToF',self.lista[len(self.lista)-2].res,None,None)

    def pushGoTo(self):
        self.lista.append('GoTo',self.lista[len(self.lista)-2].res,None,None)

    def solveGoTo(self):
        self.lista[self.popJump()].res = self.pointer

    def imprimirQuadruplos(self):
        for i in range(len(self.lista)):
            self.lista[i].Imprimir()

    def imprimirQuadStacks(self):
        print(self.lista)
        print(self.operandos)
        print(self.operator)
        print(self.jumps)
        print(self.resTemp)
        print(self.pointer)

