from collections import defaultdict

#T composition table
T=defaultdict(dict)

U={'DC','EC','EQ','TPP','NTPP','TPPi','NTPPi','PO'}
O={'EQ','TPP','NTPP','TPPi','NTTPi','PO'}


T['DC']={'DC':U, 'EC':{'DC','EC','PO','TPP','NTPP'},'PO':{'DC','EC','PO','TPP','NTPP'},'TPP':{'DC','EC','PO','TPP','NTPP'},'NTPP':{'DC','EC','PO','TPP','NTPP'},'TPPi':{'DC'},'NTPPi':{'DC'},'EQ':{'DC'}}
T['EC']={'DC':{'DC','EC','PO','PPi'},'EC':{'DC','EC','PO','TPP','TPi'},'PO':U,'TPP':{'EC','PO','TPP','NTPP'},'NTPP':{'PO','TPP','NTPP'},'TPPi':{'DC','EC','PO','PPi'},'EQ':{'PO'}}
T['PO']={'DC':{'DC','EC','PO','PPi'},'EC':{'DC','EC','PO','PPi'},'PO':U,'TPP':{'PO','TPP','NTPP'},'NTPP':{'PO','TPP','NTPP'},'TPPi':{'DC','EC','PO','PPi'},'NTPPi':{'DC','EC','PO','PPi'},'EQ':{'PO'}}
T['TPP']={'DC':'DC','EC':{'DC','EC'},'PO':{'DC','EC','PO','TPP','NTPP'},'TPP':{'TPP','NTPP'},'NTPP':{'NTPP'},'TPPi':{'DC','EC','PO','TPP','TPi'},'NTPPi':{'DC','EC','PO','PPi'},'EQ':{'TPP'}}
T['NTPP']={'DC':{'DC'},'EC':{'DC'},'PO':{'DC','EC','PO','TPP','NTPP'},'TPP':{'NTPP'},'NTPP':{'NTPP'},'TPPi':{'DC','EC','PO','TPP','NTPP'},'NTPPi':U,'EQ':'NTPP'}
T['TPPi']={'DC':{'DC','EC','PO','PPi'},'EC':{'EC','PO,PPi'},'PO':{'PO','TPP','TPi'},'TPP':{'PO','TPP','TPi'},'NTPP':{'PO','TPP','NTPP'},'TPPi':{'PPi'},'NTPPi':{'NTPPi'},'EQ':{'NTPPi'}}
T['NTPPi']={'DC':{'DC','EC','PO','PPi'},'EC':{'PO','PPi'},'PO':{'PO','PPi'},'TPP':{'PO','PPi'},'NTPP':O,'TPPi':{'NTPPi'},'NTTPi':{'NTPPi'},'EQ':{'NTPPi'}}
T['EQ']={'DC':{'DC'},'EC':{'EC'},'PO':{'PO'},'TPP':{'TPP'},'NTPP':{'NTPP'},'TPPi':{'TPPi'},'NTPPi':{'NTPPi'},'EQ':{'EQ'}}

OperatoriDiretti=['EQ','TPP','NTPP','PO','EC','DC']
OperatoriInversi=['EQ','TPPI','NTPPI','PO','EC','DC']

#OperatoriDiretti=['DC','EC','EQ','TPP','NTPP','PO']
#OperatoriInversi=['EQ','TPPI','NTPPI','PO','EC','DC']
