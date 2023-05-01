class tablaVar :
    def __init__(self):
        self.variables = {}#Se crea un diccionario vacio que se ira actualizando con las varibales

    #Aqui se anaden las variables a la tabla
    def addVar(self,id,scope,type,xAxis,yAxis,value,dirV):
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

    #Imprime dado un id un los atributos de una variable
    def imprimir(self,id):
        print(self.variables[id])

    #Esto es para poder iterar
    def __iter__(self):
        return iter(self.variables.items())

class tablaFunc :
    def __init__(self,type):
        self.type = type
        self.param = {}
        self.tablaDeVariables = {}

    def addParam(self,id,type,value,dirV):
        self.param.update({id : {'type' : type, 'value' : value, 'dirV' : dirV}})

    def addVars(self,id,scope,type,xAxis,yAxis,value,dirV):
        temp = tablaVar()
        temp.addVar(id,scope,type,xAxis,yAxis,value,dirV)
        self.tablaDeVariables.update(temp)

    def imprimirTablaVar(self,id):
        print(self.tablaDeVariables[id])

    def imprimirAllParam(self):
        for key, value in self.param.items():
            print(key, ":", value)
    
    def imprimirAll(self):
        print('Type: \n',self.type)
        print('Parameters: ')
        for key, value in self.param.items():
            print(key, ":", value)
        print('Table of variables: ')
        for key, value in self.tablaDeVariables.items():
            print(key, ":", value)
    

t = tablaFunc('int')
t.addVars('x','global','int',1,1,12,1001)
t.addVars('y','global','int',1,1,13,1003)

t.addParam('cont','int',4,2501)
t.addParam('a','float',14.5,2502)

t.imprimirAll()
