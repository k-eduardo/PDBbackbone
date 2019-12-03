'''

Quick python3 plugin to retrive the protein backbone from a PDB file.

Developed by Eduardo Ocampo L E
On December 1st 2019
MIT Licensed

'''

from e import array2csv,files2array
from pathlib import Path
import numpy as np
from numpy import linalg as LA

datadir = 'data/'
files = files2array(datadir)

print('\n This program will load all PDB files on the folder data, catch the\n \
backbone of the protein and write it on the out folder with the format:\n \
type, sequence id, atom, x coord, y coord, z coord\n \
if you wish another outcome format, contact the developer\n\n')

ei = eim1 = eim2 = []
boundangle = 0.
dihedricangle = 0.

cbackbone = []
backbone = []
n = False
trigger = False

for file in files:
    try:
        print('loading file '+file)
        f = open(file,'r')
        ei = eim1 = eim2 = []
        boundangle = 0.
        dihedricangle = 0.
        cbackbone = []
        backbone = []
        trigger = False
        for line in f:
            try:
                line = line.replace('  ',' ')
                words = line.split(' ')
                words = list(filter(lambda a: a!= ' ',words))
                words = list(filter(lambda a: a!= '\n',words))
                words = list(filter(None,words))
                if words[0] == 'ATOM':
                    atom = words[2]
                    eim2 = eim1
                    eim1 = ei
                    ei = [float(words[6]),float(words[7]),float(words[8])]
                    if trigger:
                        try:
                            boundangle = np.arccos(np.dot(eim1,eim2)/(LA.norm(eim1)*LA.norm(eim2)))
                        except Exception as e:
                            print(e)
                        try:
                            t1 = np.cross(ei,eim1)
                            t2 = np.cross(eim1,eim2)
                            dihedricangle = np.arccos(np.dot(t1,t2)/(LA.norm(t1)*LA.norm(t2)))
                        except Exception as e:
                            print(e)
                    newline = [words[0],words[1],words[2],words[6],words[7],words[8],boundangle,dihedricangle]
                    if atom == 'N':
                        cbackbone.append(newline)
                    elif atom == 'CA' and len(cbackbone) > 0:
                        cbackbone.append(newline)
                        trigger = True
                    elif atom == 'C' and len(cbackbone) > 1:
                        cbackbone.append(newline)
                        for element in cbackbone:
                            backbone.append(element)
                        cbackbone = []
                    else:
                        cbackbone = []
            except Exception as e:
                if str(e) != 'list index out of range':
                    print('error al insertar línea')
                    print(e)
                else:
                    pass
        print('Outing file '+file)
        outname = 'out/' + Path(file).stem + '.csv'
        array2csv(outname,backbone)
        print('done outing')
        print('file '+file+' processed correctly and outcome saved to: '+outname+'\n')
    except Exception as e:
        if str(e) != 'list index out of range':
            print("error on file " + file)
            print(e)
        else:
            pass
