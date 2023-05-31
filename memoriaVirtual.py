'''
global variables: (0 - 1999)
	int			: (0 - 499)
	float		: (500 - 999)
	char		: (1000 - 1499)
	bool 		: (1500 - 1999)

local variables	: (2000 - 5999)		# includes temporary variables
	int			: (2000 - 2999)
	float		: (3000 - 3999)
	char		: (4000 - 4999)
	bool 		: (5000 - 5999)

constants		: (6000 - 9999)		# are global
	int			: (6000 - 6999)
	float		: (7000 - 7999)
	char		: (8000 - 8999)
	bool 		: (9000 - 9999)
'''
from cuboSemantico import Conversion

CONSTMAXGLOBALINTS = 500
CONSTMAXGLOBALFLOATS = 500
CONSTMAXGLOBALCHARS = 500
CONSTMAXGLOBALBOOLS = 500
CONSTMAXINTS = 1000
CONSTMAXFLOATS = 1000
CONSTMAXCHARS = 1000
CONSTMAXBOOLS = 1000
CONSTMAXCTEI = 1000
CONSTMAXCTEF = 1000
CONSTMAXCTEC = 1000
CONSTMAXCTEB = 1000

class memoria:
    def __init__(self):
        self.memory = []
        self.localVars = {}
        self.globalVars = {}
        self.constants = {}
        self.counterCteI = 0
        self.counterCteF = 0
        self.counterCteC = 0
        self.counterCteB = 0
        self.counterInt = 0
        self.counterFloat = 0
        self.counterChar = 0
        self.counterBool = 0
        self.counterIntGlobal = 0
        self.counterFloatGlobal = 0
        self.counterCharGlobal = 0
        self.counterBoolGlobal = 0

    def printMem(self):
        print('Globales',self.globalVars)
        print('Locales',self.memory[len(self.localVars)-2])
        print('constants',self.constants)

    def addToMemory(self):
        self.memory.append(self.localVars)
        self.localVars = {}

    def updateMainMemV(self):
        self.memory[0] = {**self.memory[0],**self.localVars}
        self.localVars = {}

    def addVarGlobal(self,dir):
        if dir < 1999:
            if (dir > 0 and dir < 500): 
                if self.counterIntGlobal < CONSTMAXGLOBALINTS:
                    self.counterIntGlobal +=1
                else:
                    print(f"ERROR: ran out of memory for global Ints.")
                    exit()
            elif (dir > 499 and dir < 1000): 
                if self.counterFloatGlobal < CONSTMAXGLOBALFLOATS:
                    self.counterFloatGlobal +=1
                else:
                    print(f"ERROR: ran out of memory for global Floats.")
                    exit()
            elif (dir > 999 and dir < 1500):
                if self.counterCharGlobal < CONSTMAXGLOBALCHARS:
                    self.counterCharGlobal +=1
                else:
                    print(f"ERROR: ran out of memory for global Chars.")
                    exit()
            else:
                if self.counterBoolGlobal < CONSTMAXGLOBALBOOLS:
                    self.counterBoolGlobal += 1
                else:
                    print(f"ERROR: ran out of memory for global Bools.")
                    exit()
            self.globalVars.update({dir : 0})

    def addVar(self,dir):
        if dir < 5999:
            if (dir > 1999 and dir < 3000): 
                if self.counterIntGlobal < CONSTMAXINTS:
                    self.counterIntGlobal +=1
                else:
                    print(f"ERROR: ran out of memory for Local Ints.")
                    exit()
            elif (dir > 2999 and dir < 4000): 
                if self.counterFloatGlobal < CONSTMAXFLOATS:
                    self.counterFloatGlobal +=1
                else:
                    print(f"ERROR: ran out of memory for Local Floats.")
                    exit()
            elif (dir > 3999 and dir < 5000):
                if self.counterCharGlobal < CONSTMAXCHARS:
                    self.counterCharGlobal +=1
                else:
                    print(f"ERROR: ran out of memory for Local Chars.")
                    exit()
            else:
                if self.counterBoolGlobal < CONSTMAXBOOLS:
                    self.counterBoolGlobal += 1
                else:
                    print(f"ERROR: ran out of memory for Local Bools.")
                    exit()
            self.localVars.update({dir : 0})
            
    def addConst(self,type,value):
        tempDir = 0
        if (Conversion['int'] == type): 
            if self.counterCteI < CONSTMAXCTEI:
                tempDir = self.counterCteI + 6000
                self.counterCteI +=1
            else:
                print(f"ERROR: ran out of memory for Constant Ints.")
                exit()
        elif (Conversion['float'] == type): 
            if self.counterCteF < CONSTMAXCTEF:
                tempDir = self.counterCteF + 7000
                self.counterCteF +=1
            else:
                print(f"ERROR: ran out of memory for Constant Floats.")
                exit()
        elif (Conversion['char'] == type):
            if self.counterCteC < CONSTMAXCTEC:
                tempDir = self.counterCteC + 8000
                self.counterCteC +=1
            else:
                print(f"ERROR: ran out of memory for Constant Chars.")
                exit()
        else:
            if self.counterCteB < CONSTMAXCTEB:
                tempDir = self.counterCteB + 9000
                self.counterCteB += 1
            else:
                print(f"ERROR: ran out of memory for Constant Bools.")
                exit()
        self.constants.update({tempDir : value})

    def searchDirGlobal(self,id):
        try:
            if dir < 1999:
                for value in self.globalVars.values():
                    if self.globalVars[value] == id:
                        return self.globalVars[value]
        except:
            print(f"ERROR: there is no variable in virtual memory at {dir}.")
            exit()

    def searchDirGlobal(self,id):
        try:
            if dir < 1999:
                for value in self.globalVars.values():
                    if self.globalVars[value] == id:
                        return self.globalVars[value]
        except:
            print(f"ERROR: there is no variable in virtual memory at {dir}.")
            exit()

    def searchDirConstantes(self,id):
        for key, val in self.constants.items():
            if val == id:
                return key
        return 0
    
    def eraseAll(self):
        self.memory = []
        self.globalVars = {}
        self.constants = {}
        self.counterCteI = 0
        self.counterCteF = 0
        self.counterCteC = 0
        self.counterCteB = 0
        self.counterInt = 0
        self.counterFloat = 0
        self.counterChar = 0
        self.counterBool = 0
        self.counterIntGlobal = 0
        self.counterFloatGlobal = 0
        self.counterCharGlobal = 0
        self.counterBoolGlobal = 0
