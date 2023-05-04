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
    def imprimir(self):
        print(self.variables)

    #Esto es para poder iterar
    def __iter__(self):
        return iter(self.variables.items())

class tablaFunc :
    def __init__(self,type,id):
        self.type = type
        self.id = id
        self.param = {}
        self.tablaDeVariables = {}

    def addVars(self,tablaVars):
        self.tablaDeVariables.update(tablaVars)

    """ def imprimirTablaVar(self,id):
        print(self.tablaDeVariables[id])

    def imprimirAllParam(self):
        for key, value in self.param.items():
            print(key, ":", value)
    
    def imprimirAll(self):
        print('Type: \n',self.type)
        print('Id: \n',self.id)
        print('Parameters: ')
        for key, value in self.param.items():
            print(key, ":", value)
        print('Table of variables: ')
        for key, value in self.tablaDeVariables.items():
            print(key, ":", value) """

class dictFunc :
    def __init__(self):
        self.cont = 0
        self.param = {}
        self.dictionary = {}
        
    def addParam(self,id,type,value,dirV):
        self.param.update({id : {'type' : type, 'value' : value, 'dirV' : dirV}})

    def agregaFunc(self,func):
        self.dictionary.update({(self.cont) : {'func' : func}})
        self.cont = self.cont + 1
          
        
""" d = dictFunc()
t = tablaFunc('int','ejemplo')
v = tablaVar()
v.addVar('x','global','int',1,1,12,1001)
t.addVars(v)
d.addParam('cont','int',4,2501)
d.agregaFunc(t.tablaDeVariables,'cont','int',4,2501)

print(d.dict) """
