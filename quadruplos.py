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
        self.index = 1 #Nos dice en que indice vamos

class quadruplo :
    def __init__(self,operator,op1,op2,res):
        self.operator = operator
        self.op1 = op1
        self.op2 = op2
        self.res = res

    def Imprimir(self):
        print('(',self.operator,',',self.op1,',',self.op2,',',self.res,')')


q1 = []
q1.append(quadruplo(1,2,3,4))
q1.append(quadruplo(5,6,7,8))
q1[1].Imprimir()
