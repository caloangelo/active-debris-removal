from input.INPUTS import FILE_TSV,FILE_CSV



with open(FILE_TSV, encoding='UTF-8') as f:
   
    file = f.read()
    contenuto1 = file.replace(",",".")
    contenuto2 = contenuto1.replace('\t',',')

with open(FILE_CSV,"w") as f:
    f.write(contenuto2)



