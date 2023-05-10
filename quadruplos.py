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
    #Se inicializa una lista para poder guardar un objeto quadruplo en cada indice
    lista = []
    def __init__(self,operator,op1,op2,res):
        self.lista.append(quadruplo(operator,op1,op2,res))
        self.types = [] #Stack que guarda el tipo
        self.operandos = [] #Stack que guarda los operandos
        self.operator = [] #Stack que guarda los operadores
        self.jumps = [] #Stack que guarda los saltos
        self.resTemp = 0 #Stack que guarda los resultados
        self.pointer = 1 #Nos apunta hacia adelante de la instruccion que hicimos

# Aqui se inserta todo a sus listas
    def insertOperando_Type(self,newOperando, newType):
        self.types.append(newType)
        self.operandos.append(newOperando)

    def insertOperator(self, newOperator):
        self.operator.append(newOperator)

    # <POP POPS>
    def popOperator(self):
        return self.operator.pop()

    def popOperando(self):
        return self.operandos.pop()

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
            print("ERROR: TypeMismatch")
            exit()

q1 = []
q1.append(quadruplo(1,2,3,4))
q1.append(quadruplo(5,6,7,8))
q1[1].Imprimir()
