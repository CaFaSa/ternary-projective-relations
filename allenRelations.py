from collections import defaultdict

#T composition table
T=defaultdict(dict)

U={'<','>','d','di','o','oi','m','mi','s','si','f','fi','='}
dur={'d','s','f'}
con={'di','si','fi'}
O={'d','s','f','di','si','fi','o','oi','='} #big overlap
T['<']={'<':{'<'},'>':U,'d':{'<','o','m','d','s'},
        'di':{'<'},'o':{'<'},'oi':{'<','o','m','d','s'},
        'm':{'<'},'mi':{'<','o','m','d','s'},'s':{'<'},
        'si':{'<'},'f':{'<','o','m','d','s'},'fi':{'<'},'=':{'<'}}
T['>']={'<':U,'>':{'>'},'d':{'>','oi','mi','d','f'},
        'di':{'>'},'o':{'>','oi','mi','d','f'},'oi':{'>'},
        'm':{'>','oi','mi','d','f'},'mi':{'>'},
        's':{'>','oi','mi','d','f'},'si':{'>'},'f':{'>'},
        'fi':{'>'},'=':{'>'}}
T['d']={'<':{'<'},'>':{'>'},'d':{'d'},'di':U,
        'o':{'<','o','m','d','s'},'oi':{'>','oi','mi','d','f'},
        'm':{'<'},'mi':{'>'},'s':{'d'},'si':{'>','oi','mi','d','f'},
        'f':{'d'},'fi':{'<','o','m','d','s'},'=':{'d'}}
T['di']={'<':{'<','o','m','di','fi'},'>':{'>','oi','di','mi','si'},
         'd':O,'di':{'di'},'o':{'o','di','fi'},'oi':{'oi','di','si'},
         'm':{'o','di','fi'},'mi':{'oi','di','si'},
         's':{'di','fi','o'},'si':{'di'},'f':{'di','si','oi'},
         'fi':{'di'},'=':{'di'}}
T['o']={'<':{'<'},'>':{'>','oi','di','mi','si'},'d':{'o','d','s'},
        'di':{'<','o','m','di','fi'},'o':{'<','o','m'},'oi':O,
        'm':{'<'},'mi':{'oi','di','si'},'s':{'o'},
        'si':{'di','fi','o'},'f':{'d','s','o'},'fi':{'<','o','m'},
        '=':{'o'}}
T['oi']={'<':{'<','o','m','di','fi'},'>':{'>'},'d':{'oi','d','f'},
        'di':{'>','oi','di','mi','si'},'o':O,'oi':{'>','oi','mi'},
        'm':{'di','fi','o'},'mi':{'>'},'s':{'oi','d','f'},
        'si':{'oi','>','mi'},'f':{'oi'},'fi':{'oi','di','si'},
        '=':{'oi'}}
T['m']={'<':{'<'},'>':{'>','oi','di','mi','si'},'d':{'o','d','s'},
        'di':{'<'},'o':{'<'},'oi':{'o','d','s'},'m':{'<'},
        'mi':{'f','fi','='},'s':{'m'},'si':{'m'},'f':{'o','d','s'},
        'fi':{'<'},'=':{'m'}}
T['mi']={'<':{'<','o','m','di','fi'},'>':{'>'},'d':{'oi','d','f'},
        'di':{'>'},'o':{'oi','d','f'},'oi':{'>'},'m':{'s','si','='},
        'mi':{'>'},'s':{'oi','d','f'},'si':{'>'},'f':{'mi'},
        'fi':{'mi'},'=':{'mi'}}
T['s']={'<':{'<'},'>':{'>'},'d':{'d'},'di':{'<','o','m','di','fi'},
        'o':{'<','o','m'},'oi':{'oi','d','f'},'m':{'<'},'mi':{'mi'},
        's':{'s'},'si':{'s','si','='},'f':{'d'},'fi':{'<','o','m'},
        '=':{'s'}}
T['si']={'<':{'<','o','m','di','fi'},'>':{'>'},'d':{'oi','d','f'},
         'di':{'di'},'o':{'o','di','fi'},'oi':{'oi'},
         'm':{'o','di','fi'},'mi':{'mi'},'s':{'s','si','='},
         'si':{'si'},'f':{'oi'},'fi':{'di'},'=':{'si'}}
T['f']={'<':{'<'},'>':{'>'},'d':{'d'},'di':{'>','oi','mi','di','si'},
        'o':{'o','d','s'},'oi':{'>','oi','mi'},'m':{'m'},'mi':{'>'},
        's':{'d'},'si':{'>','oi','mi'},'f':{'f'},'fi':{'f','fi','='},
        '=':{'f'}}
T['fi']={'<':{'<'},'>':{'>','oi','di','mi','si'},'d':{'o','d','s'},
         'di':{'di'},'o':{'o'},'oi':{'oi','di','si'},'m':{'m'},
         'mi':{'si','oi','di'},'s':{'o'},'si':{'di'},
         'f':{'f','fi','='},'fi':{'fi'},'=':{'fi'}}
T['=']={'<':{'<'},'>':{'>'},'d':{'d'},'di':{'di'},'o':{'o'},
        'oi':{'oi'},'m':{'m'},'mi':{'mi'},'s':{'s'},'si':{'si'},
         'f':{'f'},'fi':{'fi'},'=':{'='}}

L1=['<','d','o','m','s','f','=']
L2=['>','di','oi','mi','si','fi','=']
