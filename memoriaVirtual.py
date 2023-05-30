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

class memoria:
    def __init__(self):
        self.localVars = {}
        self.globalVars = {}
        self.constatnts = {}
        self.counterInt = 0
        self.counterFloat = 0
        self.counterChar = 0
        self.counterBool = 0
        self.counterIntGlobal = 0
        self.counterFloatGlobal = 0
        self.counterCharGlobal = 0
        self.counterBoolGlobal = 0

    def addVar(self,scope,type):
        if type == Conversion['int']:#Int
            if scope == 0:#Globales
                self.globalVars.update({self.counterIntGlobal:0})
                self.counterIntGlobal += 1
            else:#Locales
                self.localVars.update({2000+self.counterInt:0})
                self.counterInt += 1
        elif type == Conversion['float']:#Float
            if scope == 0:#Globales
                self.globalVars.update({500+self.counterFloatGlobal:0})
                self.counterFloatGlobal += 1
            else:#Locales
                self.localVars.update({3000+self.counterFloat:0})
                self.counterFloat += 1
        elif type == Conversion['char'] :#Char
            if scope == 0:#Globales
                self.globalVars.update({1000+self.counterCharGlobal:0})
                self.counterCharGlobal += 1
            else:#Locales
                self.localVars.update({4000+self.counterChar:0})
                self.counterChar += 1
        else:#Bool
            if scope == 0:#Globales
                self.globalVars.update({1500+self.counterBoolGlobal:0})
                self.counterBoolGlobal += 1
            else:#Locales
                self.localVars.update({5000+self.counterBool:0})
                self.counterBool += 1