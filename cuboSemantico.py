#Este diccionario sirvira para poder convertir a un valor que acepta el cubo semantico para poder ver que tipo es la operacion
Conversion = {
'int' : 1,
'float' : 2,
'char' : 3,
'bool' : 4,
'+' : 5,
'-' : 6,
'*' : 7,
'/' : 8,
'=' : 9,
'>' : 10,
'>=' : 11,
'<' : 12,
'<=' : 13,
'==' : 14,
'!=' : 15,
'||' : 16,
'&' : 17,
'(' : 18,
'GoTo' : 19,
'GoToV' : 20,
'GoToF' : 21,
'GoSub' : 22,
'Print' : 23,
'void'	: 24,
'Return' : 25,
'EndFunc' : 26,
'Param' : 27,
'ERA' : 28,
'(' : 29
}

cuboSemantico = {
        1: { # Se definen las operaciones para INT
            1 : {
                5:  1, #+
                6:  1, #-
                7:  1, #*
                8:  1, #/
                9:  1, #=
                10: 4, #>
                11: 4, #>=
                12: 4, #<
                13: 4, #<=
                14: 4, #==
                15: 4, #!=
            }, 

            2: {
                5:  2,  #+
                6:  2,  #-
                7:  2,  #*
                8:  2,  #/
                9:  2,  #=
                10: 4,  #>
                11: 4,  #>=
                12: 4,  #<
                13: 4,  #<=
                14: 4,  #==
                15: 4,  #!=
                  },

            3: {
                5:  3,  #+
                6:  3,  #-
                7:  3,  #*
                8:  3,  #/
                9:  3,  #=
                10: 4,  #>
                11: 4,  #>=
                12: 4,  #<
                13: 4,  #<=
                14: 4,  #==
                15: 4,  #!=
            }
        }, 

        2: { # Se definen las operaciones para FLOAT
            1 : {
                5:  2,  #+
                6:  2,  #-
                7:  2,  #*
                8:  2,  #/
                9:  2,  #=
                10: 4,  #>
                11: 4,  #>=
                12: 4,  #<
                13: 4,  #<=
                14: 4,  #==
                15: 4,  #!=
            },

            2: {
                5:  2,  #+
                6:  2,  #-
                7:  2,  #*
                8:  2,  #/
                9:  2,  #=
                10: 4,  #>
                11: 4,  #>=
                12: 4,  #<
                13: 4,  #<=
                14: 4,  #==
                15: 4,  #!=
            },

            3: {
                5:  3,  #+
                6:  3,  #-
                7:  3,  #*
                8:  3,  #/
                9:  3,  #=
                10: 4,  #>
                11: 4,  #>=
                12: 4,  #<
                13: 4,  #<=
                14: 4,  #==
                15: 4,  #!=
            },

       }, 

        3 : { # Se definen las operaciones para CHAR
            1 : {
                5:  3,  #+
                6:  3,  #-
                7:  3,  #*
                8:  3,  #/
                9:  3,  #=
                10: 4,  #>
                11: 4,  #>=
                12: 4,  #<
                13: 4,  #<=
                14: 4,  #==
                15: 4,  #!=
            },

            2: { 
                5:  3,  #+
                6:  3,  #-
                7:  3,  #*
                8:  3,  #/
                9:  3,  #=
                10: 4,  #>
                11: 4,  #>=
                12: 4,  #<
                13: 4,  #<=
                14: 4,  #==
                15: 4,  #!=
            },

            3: {
                5:  3,  #+
                6:  3,  #-
                7:  3,  #*
                8:  3,  #/
                9:  3,  #=
                10: 4,  #>
                11: 4,  #>=
                12: 4,  #<
                13: 4,  #<=
                14: 4,  #==
                15: 4,  #!=
            }

       } 

} 

#1 int
#2 float
#3 char
#4 bool
#5 +
#6 -
#7 *
#8 /
#9 =
#10 >
#11 >=
#12 <
#13 <=
#14 ==
#15 !=
