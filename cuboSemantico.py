cuboSemantico = {
        'int': { # Se definen las operaciones para INT
            'int' : {
                '+':    'int',
                '-':    'int',
                '*':    'int',
                '/':    'int',
                '=':    'int',
                '>':  'bool',
                'GTEQ':  'bool',
                '<':  'bool',
                'LTEQ':  'bool',
                'EQ':  'bool',
                'NE':  'bool',
            }, 

            'float': {
                '+':    'float',
                '-':    'float',
                '*':    'float',
                '/':    'float',
                '=':    'float',
                '>':  'bool',
                'GTEQ':  'bool',
                '<':  'bool',
                'LTEQ':  'bool',
                'EQ':  'bool',
                'NE':  'bool',
                  },

            'char': {
                '+':    'char',
                '-':    'char',
                '*':    'char',
                '/':    'char',
                '=':    'char',
                '>':  'bool',
                'GTEQ':  'bool',
                '<':  'bool',
                'LTEQ':  'bool',
                'EQ':  'bool',
                'NE':  'bool',
            }
        }, 

        'float': { # Se definen las operaciones para FLOAT
            'int' : {
                '+':    'float',
                '-':    'float',
                '*':    'float',
                '/':    'float',
                '=':    'float',
                '>':  'bool',
                'GTEQ':  'bool',
                '<':  'bool',
                'LTEQ':  'bool',
                'EQ':  'bool',
                'NE':  'bool',
            },

            'float': {
                '+':    'float',
                '-':    'float',
                '*':    'float',
                '/':    'float',
                '=':    'float',
                '>':  'bool',
                'GTEQ':  'bool',
                '<':  'bool',
                'LTEQ':  'bool',
                'EQ':  'bool',
                'NE':  'bool',
            },

            'char': {
                '+':    'char',
                '-':    'char',
                '*':    'char',
                '/':    'char',
                '=':    'char',
                '>':  'bool',
                'GTEQ':  'bool',
                '<':  'bool',
                'LTEQ':  'bool',
                'EQ':  'bool',
                'NE':  'bool',
            },

       }, 

        'char' : { # Se definen las operaciones para CHAR
            'int' : {
                '+':    'char',
                '-':    'char',
                '*':    'char',
                '/':    'char',
                '=':    'char',
                '>':  'bool',
                'GTEQ':  'bool',
                '<':  'bool',
                'LTEQ':  'bool',
                'EQ':  'bool',
                'NE':  'bool',
            },

            'float': { 
                '+':    'char',
                '-':    'char',
                '*':    'char',
                '/':    'char',
                '=':    'char',
                '>':  'bool',
                'GTEQ':  'bool',
                '<':  'bool',
                'LTEQ':  'bool',
                'EQ':  'bool',
                'NE':  'bool',
            },

            'char': {
                '+':    'char',
                '-':    'char',
                '*':    'char',
                '/':    'char',
                '=':    'char',
                '>':  'bool',
                'GTEQ':  'bool',
                '<':  'bool',
                'LTEQ':  'bool',
                'EQ':  'bool',
                'NE':  'bool',
            }

       } 

} 
