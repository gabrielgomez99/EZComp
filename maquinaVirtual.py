import pickle
from cuboSemantico import Conversion
from tablas import tablaVar
from tablas import tablaFunc
from tablas import dictFunc

class maquinaVirtual:
    
    def __init__(self):
        with open ('data.obj', 'rb') as file:
            data = pickle.load(file)

        self.funcDir = data['funcDir']
        self.memory = data['memory']
        self.quads = data['quadruplos']

    def getValue(self,op):
        if(op == None):
            return
        if(op < 2000):
            return self.memory.globalVars[op]
        elif(op < 6000):
            return self.memory.memory[-1][op]
        else:
            return self.memory.constants[op]
        
    def setValue(self,dir,value):
        #print(dir,value)
        if(dir < 2000):
            self.memory.globalVars[dir] = value
        elif(dir < 6000):
            #print(value)
            self.memory.memory[-1][dir] = value
        else:
            self.memory.constants = value

    def startMaquinaVirtual(self):
        i = 0
        self.memory.printMem()
        while(True):
            operator = self.quads[i].operator
            opLeft = self.getValue(self.quads[i].op1)
            opRight = self.getValue(self.quads[i].op2)
            if(self.quads[i].res == None):
                pass
            elif(type(self.quads[i].res) == str):
                if(self.quads[i].res[0] == '$'):
                    result = self.quads[i].res[1:]
                else:
                    result = self.quads[i].res

            #Arithmetics
            if(operator == Conversion['=']):
                try:
                    print(opLeft,'=',self.quads[i].res)
                    self.memory.memory[-1][self.quads[i].res] = opLeft
                except:
                    self.memory.globalVars[self.quads[i].res] = opLeft
            elif(operator == Conversion['+']):
                print(opLeft,'+',opRight,self.quads[i].res)
                value = opLeft + opRight
                self.setValue(self.quads[i].res,value)
            elif(operator == Conversion['-']):
                value = opLeft - opRight
                self.setValue(self.quads[i].res,value)
            elif(operator == Conversion['*']):
                value = opLeft * opRight
                self.setValue(self.quads[i].res,value)
            elif(operator == Conversion['/']):
                value = opLeft / opRight
                self.setValue(self.quads[i].res,value)
            
            #Relational
            if(operator == Conversion['<']):
                if(opLeft < opRight):
                    print(opLeft,'<',opRight)
                    self.setValue(self.quads[i].res,1)
                else:
                    self.setValue(self.quads[i].res,0)
            elif(operator == Conversion['>']):
                if(opLeft > opRight):
                    self.setValue(self.quads[i].res,1)
                else:
                    self.setValue(self.quads[i].res,0)
            elif(operator == Conversion['<=']):
                if(opLeft <= opRight):
                    self.setValue(self.quads[i].res,1)
                else:
                    self.setValue(self.quads[i].res,0)
            elif(operator == Conversion['>=']):
                if(opLeft >= opRight):
                    self.setValue(self.quads[i].res,1)
                else:
                    self.setValue(self.quads[i].res,0)
            elif(operator == Conversion['!=']):
                if(not(opLeft == opRight)):
                    self.setValue(self.quads[i].res,1)
                else:
                    self.setValue(self.quads[i].res,0)
            elif(operator == Conversion['==']):
                if(opLeft == opRight):
                    self.setValue(self.quads[i].res,1)
                else:
                    self.setValue(self.quads[i].res,0)

            #GoTo
            if(operator == Conversion['GoTo']):
                #print('regreso',result)
                i = int(result) - 1
            elif(operator == Conversion['GoToF']):
                if(opLeft == 0):
                    #print('sali',result)
                    i = int(result) - 1

            #Print
            """ if(operator == Conversion['Print']):
                print('hola',self.getValue(self.quads[i].res)) """
            
            if(operator == Conversion['END']):
                print('Se acabo ejecucion')
                self.memory.printMem()
                exit()

            i += 1