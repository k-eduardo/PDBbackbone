'''
Quick python3 plugin to retrive the protein backbone from a PDB file.

Developed by Eduardo Ocampo L E
On December 1st 2019
MIT Licensed
'''

from e import array2csv,files2array
from pathlib import Path

datadir = 'data/'
files = files2array(datadir)

print('\n This program will load all PDB files on the folder data, catch the\n \
backbone of the protein and write it on the out folder with the format:\n \
type, sequence id, atom, x coord, y coord, z coord\n \
if you wish another outcome format, contact the developer\n\n')

cbackbone = []
backbone = []
n = False
for file in files:
    try:
        print('loading file '+file)
        f = open(file,'r')
        for line in f:
            try:
                words = line.split('  ')
                atom = words[2]
                newline = [words[0],words[1],words[2],words[6],words[7],words[8]]
                if atom == 'N':
                    cbackbone.append(newline)
                elif atom == 'CA' and len(cbackbone) > 0:
                    cbackbone.append(newline)
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
        outname = 'out/' + Path(file).stem + '.csv'
        array2csv(outname,backbone)
        print('file '+file+' processed correctly and outcome saved to: '+outname+'\n')
    except Exception as e:
        if str(e) != 'list index out of range':
            print("error on file " + file)
            print(e)
        else:
            pass
