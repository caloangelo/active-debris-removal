velocities = []

file = open("output/iterator_output_dv.txt","r",encoding="UTF-8")
line = file.readline()
while line != '':
    dv = float(line[0:5])
    velocities.append(dv)
    line = file.readline()

minimum_DV = min(velocities)
index = velocities.index(minimum_DV)
print("index: ",index, "DV: ",minimum_DV )

