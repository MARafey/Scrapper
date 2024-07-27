# reading the json file
import json

# reading the json file
with open('data.json') as f:
    data = json.load(f)

# printing the data

data2 = []
for i in range(len(data['Balochistan'])):
    # merging the data into one
    data2.append(data['Balochistan'][i])

# converting the data into 1 d array
data = []
for i in range(len(data2)):
    for j in range(len(data2[i])):
        data.append(data2[i][j])

# converting the data into float
for i in range(len(data)):
    data[i] = float(data[i])

# writing the data into a file
with open('data.txt', 'w') as f:
    for i in range(len(data)):
        f.write(str(data[i]) + ' ')