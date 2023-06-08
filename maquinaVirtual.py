import pickle
import pandas as pd
import matplotlib.pyplot as plt
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
        elif(op < 9999):
            return self.memory.constants[op]
        else:
            return self.memory.globalVars[op]
        
    def setValue(self,dir,value):
        if(dir < 2000 or dir > 9999):
            self.memory.globalVars[dir] = value
        elif(dir < 6000):
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
            if(type(self.quads[i].op1) == str):
                opLeft = self.quads[i].op1
            else:
                try:
                    opLeft = self.getValue(self.quads[i].op1)
                except:
                    pass
            if(self.quads[i].res == None):
                pass
            elif(type(self.quads[i].res) == str):
                if(self.quads[i].res[0] == '$'):
                    result = self.quads[i].res[1:]
                else:
                    result = self.quads[i].res
            #Arithmetics
            if(operator == Conversion['=']):       
                if(type(self.quads[i].res) == str):
                    if(self.quads[i+1].operator == Conversion['Return']):
                        self.memory.memory[-1][self.quads[i].op1] = self.memory.popGlobal()[1]
                elif(self.quads[i-1].operator == Conversion['ARREGLO']):
                    key = 0
                    for keys in self.funcDir[-1].tablaDeVariables.keys():
                        if(self.funcDir[-1].tablaDeVariables[keys]['dir'] == self.quads[i-1].res):
                            key = keys
                    if(self.quads[i-1].res + self.getValue(self.quads[i].res) < self.funcDir[-1].tablaDeVariables[key]['dir'] + self.funcDir[-1].tablaDeVariables[key]['xAxis'] * self.funcDir[-1].tablaDeVariables[key]['yAxis']):
                        self.memory.memory[-1][self.quads[i-1].res + self.getValue(self.quads[i].res)] = opLeft
                    else:
                        print('ERROR: Se esta indexando fuera del rango de la variable')
                        exit()
                else:
                    self.memory.memory[-1][self.quads[i].res] = opLeft
            elif(operator == Conversion['+']):
                value = self.getValue(self.quads[i].op1) + self.getValue(self.quads[i].op2)
                self.setValue(self.quads[i].res,value)
            elif(operator == Conversion['-']):
                value = self.getValue(self.quads[i].op1) - self.getValue(self.quads[i].op2)
                self.setValue(self.quads[i].res,value)
            elif(operator == Conversion['*']):
                value = self.getValue(self.quads[i].op1) * self.getValue(self.quads[i].op2)
                self.setValue(self.quads[i].res,value)
            elif(operator == Conversion['/']):
                value = self.getValue(self.quads[i].op1) / self.getValue(self.quads[i].op2)
                self.setValue(self.quads[i].res,value)
            
            #Relational
            if(operator == Conversion['<']):
                if(self.getValue(self.quads[i].op1) < self.getValue(self.quads[i].op2)):
                    #print(opLeft,'<',opRight)
                    self.setValue(self.quads[i].res,1)
                else:
                    self.setValue(self.quads[i].res,0)
            elif(operator == Conversion['>']):
                if(self.getValue(self.quads[i].op1) > self.getValue(self.quads[i].op2)):
                    self.setValue(self.quads[i].res,1)
                else:
                    self.setValue(self.quads[i].res,0)
            elif(operator == Conversion['<=']):
                if(self.getValue(self.quads[i].op1) <= self.getValue(self.quads[i].op2)):
                    self.setValue(self.quads[i].res,1)
                else:
                    self.setValue(self.quads[i].res,0)
            elif(operator == Conversion['>=']):
                if(self.getValue(self.quads[i].op1) >= self.getValue(self.quads[i].op2)):
                    self.setValue(self.quads[i].res,1)
                else:
                    self.setValue(self.quads[i].res,0)
            elif(operator == Conversion['!=']):
                if(not(self.getValue(self.quads[i].op1) == self.getValue(self.quads[i].op2))):
                    self.setValue(self.quads[i].res,1)
                else:
                    self.setValue(self.quads[i].res,0)
            elif(operator == Conversion['==']):
                if(self.getValue(self.quads[i].op1) == self.getValue(self.quads[i].op2)):
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

            #Read
            if(operator == Conversion['Read']):
                value = input()
                if(self.quads[i].res < 500):
                        value = int(value)
                        self.memory.globalVars[self.quads[i].res] = int(value)
                elif(self.quads[i].res < 1000):
                        self.memory.globalVars[self.quads[i].res] = float(value)
                elif(self.quads[i].res < 1500):
                        self.memory.globalVars[self.quads[i].res] = str(value)
                elif(self.quads[i].res < 3000):
                        self.memory.memory[-1][self.quads[i].res] = int(value)
                elif(self.quads[i].res < 4000):
                        self.memory.memory[-1][self.quads[i].res] = float(value)
                elif(self.quads[i].res < 5000):
                        self.memory.memory[-1][self.quads[i].res] = str(value)

            #ERA
            if(operator == Conversion['ERA']):
                size = len(self.funcDir)-1
                for j in range(size):
                    if(self.funcDir[j].id == result):
                        for key in ((self.funcDir[j].tablaDeVariables.keys())):
                            xAxis = self.funcDir[j].tablaDeVariables[key]['xAxis']
                            yAxis = self.funcDir[j].tablaDeVariables[key]['yAxis']
                            for k in range(xAxis*yAxis):
                                self.memory.addVar(self.funcDir[j].tablaDeVariables[key]['dir']+k)
                        for key in ((self.funcDir[j].temps.keys())):
                            self.memory.addVar(key)
                        funcionIdTemp = result

            #Param
            if(operator == Conversion['Param']):
                size = len(self.funcDir)-1
                for j in range(size):
                    if(self.funcDir[j].id == funcionIdTemp):
                        key = list(self.funcDir[j].param.keys())[contParam]
                        self.memory.addVar(self.funcDir[j].param[key]['dirV'])
                        self.memory.localVars[self.funcDir[j].param[key]['dirV']] = self.getValue(self.quads[i].res)
                        temp = self.funcDir[j].ints + 2000 - 1
                        self.memory.addVar(temp)
                        self.memory.memory.append(self.memory.localVars)
                        self.memory.localVars = {}
                        contParam += 1
                                 
            #GoSub
            if(operator == Conversion['GoSub']):
                contParam = 0
                jumpEndProc.append(i)
                i = int(result) -1

            #Return
            if(operator == Conversion['Return']):
                if(self.quads[i-1].operator == Conversion['=']):
                    for j in range(len(self.funcDir)):
                        if(self.funcDir[j].id == self.quads[i].res):
                            self.memory.addVarGlobalType(self.funcDir[j].type)
                    key = list(self.memory.globalVars)[-1]
                    self.memory.globalVars[key] = self.getValue(self.quads[i-1].op1)
                else:
                    for j in range(len(self.funcDir)):
                        if(self.funcDir[j].id == funcionIdTemp):
                            self.memory.addVarGlobalType(self.funcDir[j].type)
                            key = list(self.memory.globalVars)[-1]
                        self.memory.globalVars[key] = self.getValue(self.quads[i].op1)
                i = int(jumpEndProc.pop())

            #MEAN
            if(operator == Conversion['MEAN']):
                df = pd.read_csv(self.quads[i].res.replace('"',''))
                mean_value = df.mean()
                # Print the mean value
                print('Mean: ',mean_value)

            #MEDIAN
            if(operator == Conversion['MEDIAN']):
                df = pd.read_csv(self.quads[i].res.replace('"',''))
                median_value = df.median()
                # Print the mean value
                print('Median: ',median_value)

            #MODE
            if(operator == Conversion['MODE']):
                df = pd.read_csv(self.quads[i].res.replace('"',''))
                mode_value = df.mode()
                # Print the mean value
                print('Mode: ',mode_value)

            #VARIANCE
            if(operator == Conversion['VARIANCE']):
                df = pd.read_csv(self.quads[i].res.replace('"',''))
                var_value = df.var()
                # Print the mean value
                print('Variance: ',var_value)

            #VARIANCE
            if(operator == Conversion['STDDEV']):
                df = pd.read_csv(self.quads[i].res.replace('"',''))
                std_value = df.std()
                # Print the mean value
                print('Standard Deviation: ',std_value)

            #HISTOGRAM
            if(operator == Conversion['HISTOGRAM']):
                df = pd.read_csv(self.quads[i].res.replace('"',''))
                df[self.quads[i].op2].plot.hist(bins=self.quads[i].op1)  # Adjust the number of bins as desired
                # Set labels and title
                plt.xlabel(self.quads[i].op2)
                # Display the histogram
                plt.show()
                                    
            
            #EndFunc
            if(operator == Conversion['EndFunc']):
                i = int(jumpEndProc.pop())
                        
            
            if(operator == Conversion['END']):
                print('Se acabo ejecucion')  
                self.memory.eraseAll()
                self.memory.printMem()
                exit()
            i += 1