import json
from cuboSemantico import Conversion

class tablaVar :
    def __init__(self):
        self.id = 0
        self.CounterInt = 0
        self.CounterFloat = 0
        self.CounterChar = 0
        self.variables = {}#Se crea un diccionario vacio que se ira actualizando con las varibales

    #Aqui se anaden las variables a la tabla
    def addVar(self,id,scope,type,xAxis,yAxis,value):
        if type == 1:
            dirV = 1000 + self.CounterInt
            self.CounterInt += 1
        elif type == 2:
            dirV = 2000 + self.CounterFloat
            self.CounterFloat += 1
        else :
            dirV = 3000 + self.CounterChar
            self.CounterChar += 1
        self.variables.update({
                id : {
                'scope' : scope,
                'type' : type,
                'xAxis' : xAxis,
                'yAxis' : yAxis,
                'value' : value,
                'dirV' : dirV
            }
        })

    #Esto es para poder iterar
    def __iter__(self):
        return iter(self.variables.items())

class tablaFunc :
    def __init__(self,type,id):
        self.type = type
        self.id = id
        self.dir = None
        self.param = {}
        self.tablaDeVariables = {}

    def addParam(self,type,id,value,dirV):
        self.param.update({id : {'type' : type, 'value' : value, 'dirV' : dirV}})

    def addVars(self,tablaVars):
        self.tablaDeVariables.update(tablaVars)

    def imprimirFunc(self):
        #print({'Params' : self.param, 'Tabla de Variables' : self.tablaDeVariables})
        print(json.dumps(self.param,indent=4,sort_keys=False))
        print(json.dumps(self.tablaDeVariables,indent=4,sort_keys=False))

class dictFunc :
    def __init__(self):
        self.list = []

    def agregaFunc(self,func):
        self.list.append({'func' : func})
    
    def getVarType(self, varId):
        id = str(varId)
        try:
            return self.list[len(self.list)-1]['func'].tablaDeVariables[id]['type']
        except KeyError:
            print("ERROR: Variable does not exist")
            exit()
          
        
""" d = dictFunc()
t = tablaFunc('int','ejemplo')
v = tablaVar()
v.addVar('x','global','int',1,1,12,1001)
t.addVars(v)
d.agregaFunc(t.tablaDeVariables)

d.list[0]['func'].imprimirFunc() """
