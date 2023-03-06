import pandas as pd


numRows = 2
numCols = 4
colsName=list(map(chr, range(97, 97+numCols)))
print(colsName)
df = pd.DataFrame(index=range(numRows),columns=range(numCols))

