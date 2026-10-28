import input.tsv_organizer as tsv_organizer
from input.tsv_organizer import FILE_CSV

file = open(FILE_CSV, encoding='UTF-8')

file.readline()
stages = {}
counters = {}

for row in file:
    row = row.strip().split(',')
    if row[0] not in stages:
        if row[0]=='':
            pass
        stages[row[0]] = [float(parameters) for parameters in row[1:] if parameters!='']
        counters[row[0]] = 1
    else:
        counters[row[0]] += 1
        counter = str(counters[row[0]])
        new_row = row[0] + '(' + counter + ')'
        stages[new_row] = [float(parameters) for parameters in row[1:] if parameters!='']

keys = stages.keys()
for key in keys:
    stages[key].append(None)

