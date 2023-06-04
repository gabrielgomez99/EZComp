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
    def addVar(self,id,scope,type,xAxis,yAxis):
        temp = 0
        if type == Conversion['int']:
            if scope == 0:
                if self.counterInt >= 500:
                    print(f"ERROR: ran out of memory for global Ints.")
                    exit()
                temp = self.counterInt
            else:
                if self.counterInt >= 1000:
                    print(f"ERROR: ran out of memory for Local Ints.")
                    exit()
                temp = self.counterInt + 2000
            self.counterInt += 1
        elif type == Conversion['float']:
            if scope == 0:
                if self.counterFloat >= 500:
                    print(f"ERROR: ran out of memory for global Floats.")
                    exit()
                temp = self.counterFloat
            else:
                if self.counterFloat >= 1000:
                    print(f"ERROR: ran out of memory for Local Floats.")
                    exit()
                temp = self.counterFloat + 3000
            self.counterFloat += 1
        else:
            if scope == 0:
                if self.counterChar >= 500:
                    print(f"ERROR: ran out of memory for global Chars.")
                    exit()
                temp = self.counterChar
            else:
                if self.counterChar >= 1000:
                    print(f"ERROR: ran out of memory for Local Chars.")
                    exit()
                temp = self.counterChar + 4000
            self.counterChar += 1
        self.variables.update({
                id : {
                'scope' : scope,
                'type' : type,
                'xAxis' : xAxis,
                'yAxis' : yAxis,
                'dir' : temp,
            }
        })

    def addMat(self,id,scope,type,xAxis,yAxis):
        temp = 0
        if(yAxis == 1):
            if type == Conversion['int']:
                if scope == 0:
                    if self.counterInt >= 500:
                        print(f"ERROR: ran out of memory for global Ints.")
                        exit()
                    temp = self.counterInt
                    self.counterInt
                else:
                    if self.counterInt >= 1000:
                        print(f"ERROR: ran out of memory for Local Ints.")
                        exit()
                    temp = self.counterInt + 2000
                self.counterInt += 1 + xAxis
            elif type == Conversion['float']:
                if scope == 0:
                    if self.counterFloat >= 500:
                        print(f"ERROR: ran out of memory for global Floats.")
                        exit()
                    temp = self.counterFloat
                else:
                    if self.counterFloat >= 1000:
                        print(f"ERROR: ran out of memory for Local Floats.")
                        exit()
                    temp = self.counterFloat + 3000
                self.counterFloat += 1 + xAxis
            else:
                if scope == 0:
                    if self.counterChar >= 500:
                        print(f"ERROR: ran out of memory for global Chars.")
                        exit()
                    temp = self.counterChar
                else:
                    if self.counterChar >= 1000:
                        print(f"ERROR: ran out of memory for Local Chars.")
                        exit()
                    temp = self.counterChar + 4000
                self.counterChar += 1 + xAxis
        else:
            if type == Conversion['int']:
                if scope == 0:
                    if self.counterInt >= 500:
                        print(f"ERROR: ran out of memory for global Ints.")
                        exit()
                    temp = self.counterInt
                else:
                    if self.counterInt >= 1000:
                        print(f"ERROR: ran out of memory for Local Ints.")
                        exit()
                    temp = self.counterInt + 2000
                self.counterInt += xAxis*yAxis
            elif type == Conversion['float']:
                if scope == 0:
                    if self.counterFloat >= 500:
                        print(f"ERROR: ran out of memory for global Floats.")
                        exit()
                    temp = self.counterFloat
                else:
                    if self.counterFloat >= 1000:
                        print(f"ERROR: ran out of memory for Local Floats.")
                        exit()
                    temp = self.counterFloat + 3000
                self.counterFloat += xAxis*yAxis
            else:
                if scope == 0:
                    if self.counterChar >= 500:
                        print(f"ERROR: ran out of memory for global Chars.")
                        exit()
                    temp = self.counterChar 
                else:
                    if self.counterChar >= 1000:
                        print(f"ERROR: ran out of memory for Local Chars.")
                        exit()
                    temp = self.counterChar + 4000
                self.counterChar += xAxis*yAxis
        self.variables.update({
                id : {
                'scope' : scope,
                'type' : type,
                'xAxis' : xAxis,
                'yAxis' : yAxis,
                'dir' : temp,
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
        self.fin = None
        self.param = {}
        self.tablaDeVariables = {}
        self.temps = {}
        self.ints = 0
        self.floats = 0
        self.chars = 0
        self.bools = 0

    def addToCounterType(self,type):
        temp = 0
        if type == Conversion['int']:
            temp = self.ints + 2000
            self.ints += 1
            return temp
        elif type == Conversion['float']:
            temp = self.floats + 3000
            self.floats += 1
            return temp
        elif type == Conversion['char']:
            temp = self.chars + 4000
            self.chars += 1
            return temp
        else:
            temp = self.bools + 5000
            self.bools += 1
            return temp

    def addTemp(self,type):
        dirV = 0
        if type == Conversion['int']:
            dirV = self.ints + 2000
            self.ints += 1
        elif type == Conversion['float']:
            dirV = self.floats + 3000
            self.floats += 1
        elif type == Conversion['char']:
            dirV = self.chars + 4000
            self.chars += 1
        elif type == Conversion['bool']:
            dirV = self.bools + 5000
            self.bools += 1
        self.temps.update({dirV : {'value' : 0}})
        return dirV

    def addParam(self,type,id,dirV):
        if type == Conversion['int']:
            dirV = self.ints + 2000
            self.ints += 1
        elif type == Conversion['float']:
            dirV = self.floats + 3000
            self.floats += 1
        else:
            dirV = self.chars + 4000
            self.chars += 1
        self.param.update({id : {'type' : type, 'dirV' : dirV}})

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
        print(json.dumps(self.temps,indent=4,sort_keys=False))

class dictFunc :
    def __init__(self):
        self.list = []

    def agregaFunc(self,func):
        self.list.append(func)
    
    def getVarType(self, varId):
        id = str(varId)
        try:
            return self.list[len(self.list)-1].tablaDeVariables[id]['type']
        except KeyError:
            try:
                return self.list[len(self.list)-1].param[id]['type']
            except KeyError:
                try:
                    return self.list[0].tablaDeVariables[id]['type']
                except KeyError:
                    print(f"ERROR: Variable does not exist, {varId}")
                    exit()
    
    def getVarDir(self, varId):
        id = str(varId)
        try:
             return self.list[len(self.list)-1].tablaDeVariables[id]['dir']
        except KeyError:
            try:
                return self.list[len(self.list)-1].param[id]['dirV']
            except KeyError:
                try:
                    return self.list[0].tablaDeVariables[id]['dir']
                except KeyError:
                    print(f"ERROR: Variable does not exist, {varId}")
                    exit()
       
""" d = dictFunc()
t = tablaFunc('int','ejemplo')
v = tablaVar()
v.addVar('x','global','int',1,1,12,1001)
t.addVars(v)
d.agregaFunc(t.tablaDeVariables)

d.list[0].imprimirFunc() """
