import csv , os

def files2array(location):
    '''Returns all files on a dir in an array'''
    out = []
    for file in os.listdir(location):
        if not file.startswith('.') and not file.startswith("~"):
            out.append(location+file)
    return out

def array2csv(filename,arraytowrite):
    '''This function recieves a name and an array of arrays and writes a comma separated
    value entry on the file for all '''
    with open(filename, 'w') as file:
        writer = csv.writer(file)
        for element in arraytowrite:
            writer.writerow(element)
