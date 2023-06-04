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
            #print('value',self.memory.globalVars[op])
            return self.memory.globalVars[op]
        elif(op < 6000):
            #print('value',self.memory.memory)
            return self.memory.memory[-1][op]
        else:
            #print('value',self.memory.constants[op])
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
        i = 0 #pointer de los quadruplos
        contParam = 0 #Se cuenta los parametros
        funcionIdTemp = '' #Sirve para luego buscar en tablaDeVariables y Param de funcDir
        jumpEndProc = []
        self.memory.printMem()
        while(True):
            operator = self.quads[i].operator
            #print(self.quads[i].operator,self.quads[i].op1,self.quads[i].op2,self.quads[i].res)
            if(type(self.quads[i].op1) == str):
                opLeft = self.quads[i].op1
            else:
                #print(self.memory.memory[-1])
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
                    if(type(self.quads[i].res) == str):
                        for j in range(len(self.funcDir)):
                            if(self.funcDir[j].id == opLeft):
                                #print(self.memory.popGlobal()[1])
                                temp = self.quads[i].op1
                                print('i',i,'asigna','a',temp,'aaaaaaaa')
                                #print(self.memory.popGlobal()[0],'dddddddddd')
                                print(self.memory.memory[-1],'afffffff') 
                                self.memory.memory[-1][temp] = self.memory.popGlobal()[1]
                                print(self.memory.memory,'ffaaaaaaaaa') 
                                break  
                    else:
                        #print(opLeft,'=',self.quads[i].res)
                        self.memory.memory[-1][self.quads[i].res] = opLeft
                except:
                    print(self.quads[i].operator,self.quads[i].op1,self.quads[i].op2,self.quads[i].res)
                    self.memory.globalVars[self.quads[i].res] = opLeft
            elif(operator == Conversion['+']):
                #print(self.getValue(self.quads[i].op1),'+',opRight,self.quads[i].res)
                value = self.getValue(self.quads[i].op1) + self.getValue(self.quads[i].op2)
                #print(value)
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
                    #print(opLeft,'<',opRight)
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
                i = int(result) - 1
            elif(operator == Conversion['GoToF']):
                if(opLeft == 0):
                    i = int(result) - 1

            #Print
            if(operator == Conversion['Print']):
                if(type(self.quads[i].res) == str):
                    print(self.quads[i].res)
                else:
                    print(self.getValue(self.quads[i].res))

            #ERA
            if(operator == Conversion['ERA']):
                size = len(self.funcDir)-1
                for j in range(size):
                    if(self.funcDir[j].id == result):
                        for key in ((self.funcDir[j].tablaDeVariables.keys())):
                            self.memory.addVar(self.funcDir[j].tablaDeVariables[key]['dir'])
                        funcionIdTemp = result
                        self.memory.memory.append(self.memory.localVars)
                        self.memory.localVars = {}
                        #print(self.memory.localVars)
                        #self.memory.addToMemoryEra()

            #Param
            if(operator == Conversion['Param']):
                size = len(self.funcDir)-1
                #print(self.memory.memory)
                for j in range(size):
                    if(self.funcDir[j].id == funcionIdTemp):
                        key = list(self.funcDir[j].param.keys())[contParam]
                        self.memory.addVar(self.funcDir[j].param[key]['dirV'])
                        self.memory.localVars[self.funcDir[j].param[key]['dirV']] = self.getValue(self.quads[i].res)
                        contParam += 1
                        self.memory.updateParams()
                                 
            #GoSub
            if(operator == Conversion['GoSub']):
                #print(self.memory.localVars,self.memory.TcounterInt)
                #print(self.memory.memory)
                #print(self.memory.localVars)
                contParam = 0
                jumpEndProc.append(i)
                i = int(result) -1

            #Return
            if(operator == Conversion['Return']):
                for j in range(len(self.funcDir)):
                    if(self.funcDir[j].id == funcionIdTemp):
                        self.memory.addVarGlobalType(self.funcDir[j].type)
                        print('lel',self.memory.globalVars)
                        key = list(self.memory.globalVars.keys())[-1]
                        self.memory.globalVars[key] = self.getValue(self.quads[i].res)
                        print('lel',self.memory.globalVars)
                        self.memory.memory.pop()
                i = int(jumpEndProc.pop())
            
            #EndFunc
            if(operator == Conversion['EndFunc']):
                i = int(jumpEndProc.pop())
                        
            
            if(operator == Conversion['END']):
                print('Se acabo ejecucion')
                
                #self.memory.eraseAll()
                self.memory.printMem()
                exit()
            i += 1