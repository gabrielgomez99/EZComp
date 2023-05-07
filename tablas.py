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

    #Esto es para poder iterar
    def __iter__(self):
        return iter(self.variables.items())

class tablaFunc :
    def __init__(self,type,id):
        self.type = type
        self.id = id
        self.param = {}
        self.tablaDeVariables = {}

    def addParam(self,type,id,value,dirV):
        self.param.update({id : {'type' : type, 'value' : value, 'dirV' : dirV}})

    def addVars(self,tablaVars):
        self.tablaDeVariables.update(tablaVars)

    def imprimirFunc(self):
        print({'Params' : self.param, 'Tabla de Variables' : self.tablaDeVariables})

class dictFunc :
    def __init__(self):
        self.list = []

    def agregaFunc(self,func):
        self.list.append({'func' : func})
          
        
""" d = dictFunc()
t = tablaFunc('int','ejemplo')
v = tablaVar()
v.addVar('x','global','int',1,1,12,1001)
t.addVars(v)
d.addParam('cont','int',4,2501)
d.agregaFunc(t.tablaDeVariables,'cont','int',4,2501)

print(d.dict) """
