import json
from cuboSemantico import Conversion

class tablaVar :
    def __init__(self):
        self.id = 0
        self.counterInt = 0
        self.counterFloat = 0
        self.counterChar = 0
        self.variables = {}#Se crea un diccionario vacio que se ira actualizando con las varibales

    #Aqui se anaden las variables a la tabla
    def addVar(self,id,scope,type,xAxis,yAxis,value):
        if type == Conversion['int']:
            self.counterInt += 1
        elif type == Conversion['float']:
            self.counterFloat += 1
        else:
            self.counterChar += 1
        self.variables.update({
                id : {
                'scope' : scope,
                'type' : type,
                'xAxis' : xAxis,
                'yAxis' : yAxis,
                'value' : value,
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
        self.ints = 0
        self.floats = 0
        self.chars = 0

    def addParam(self,type,id,value,dirV):
        if type == Conversion['int']:
            self.ints += 1
        elif type == Conversion['float']:
            self.floats += 1
        else:
            self.chars += 1
        self.param.update({id : {'type' : type, 'value' : value, 'dirV' : dirV}})

    def addVars(self,tablaVars):
        self.ints += tablaVars.counterInt
        self.floats += tablaVars.counterFloat
        self.chars += tablaVars.counterChar
        self.tablaDeVariables.update(tablaVars)

    def imprimirFunc(self):
        print(json.dumps("Ints: " + str(self.ints),indent=4,sort_keys=False))
        print(json.dumps("Floats: " + str(self.floats),indent=4,sort_keys=False))
        print(json.dumps("Chars: " + str(self.chars),indent=4,sort_keys=False))
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
            try:
                return self.list[len(self.list)-1]['func'].param[id]['type']
            except KeyError:
                try:
                    return self.list[0]['func'].tablaDeVariables[id]['type']
                except KeyError:
                    print(f"ERROR: Variable does not exist, {varId}")
                    exit()
    
    def getVariD(self, varId):
        id = str(varId)
        try:
             return self.list[len(self.list)-1]['func'].tablaDeVariables[id]
        except KeyError:
            try:
                return self.list[len(self.list)-1]['func'].param[id]
            except KeyError:
                try:
                    return self.list[0]['func'].tablaDeVariables[id]
                except KeyError:
                    print(f"ERROR: Variable does not exist, {varId}")
                    exit()
        
""" d = dictFunc()
t = tablaFunc('int','ejemplo')
v = tablaVar()
v.addVar('x','global','int',1,1,12,1001)
t.addVars(v)
d.agregaFunc(t.tablaDeVariables)

d.list[0]['func'].imprimirFunc() """
