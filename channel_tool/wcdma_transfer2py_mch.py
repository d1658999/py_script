import csv
import pathlib
import pandas as pd
import numpy as np
import json


path = pathlib.Path("./")
# d = {1:18300, 2:19300}
# print(type(d))
# for file in path.iterdir():
#     if file.match('*.csv'):
#         with open(file, 'r') as inputfile:
#             reader = csv.reader(inputfile)
#             next(reader)
#             mydict = {int(rows[0]): int(rows[1]) for rows in reader}
#             print(type(mydict))
#             with open('new.ini', 'w') as outfile:
#                 print(str(mydict).replace(',', ',\n'), file=outfile)



for file in path.iterdir():
    if file.match('*wcdma.csv'):
        with open(file, 'r') as inputfile:
            reader = csv.reader(inputfile)
            next(reader)
            mydict = {int(rows[0]): int(rows[1]) for rows in reader}
            with open('new_wcdma_mch.json', 'w') as outputfile:
                json.dump(mydict, outputfile, indent=4)
