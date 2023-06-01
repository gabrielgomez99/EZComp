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
        print(dir,value)
        if(dir < 2000):
            self.memory.globalVars[dir] = value
        elif(dir < 6000):
            self.memory.memory[-1][dir] = value
        else:
            self.memory.constants = value

    def startMaquinaVirtual(self):
        for i in range (len(self.quads)-1):
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
                    self.memory.memory[-1][self.quads[i].res] = opLeft
                except:
                    self.memory.globalVars[self.quads[i].res] = opLeft
            elif(operator == Conversion['+']):
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
                    print('True')
                    self.setValue(self.quads[i].res,1)
                else:
                    print('False')
                    self.setValue(self.quads[i].res,0)
            elif(operator == Conversion['==']):
                if(opLeft == opRight):
                    print('True')
                    self.setValue(self.quads[i].res,1)
                else:
                    print('False')
                    self.setValue(self.quads[i].res,0)
            
