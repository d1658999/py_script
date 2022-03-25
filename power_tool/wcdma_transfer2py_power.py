import csv
import pathlib
import json


path = pathlib.Path("./")

for file in path.iterdir():
    if file.match('*wcdma.csv'):
        with open(file, 'r') as inputfile:
            reader = csv.reader(inputfile)
            next(reader)
            mydict = {int(rows[0]): float(rows[1]) for rows in reader}
            with open('new_wcdma_power_target.json', 'w') as outputfile:
                json.dump(mydict, outputfile, indent=4)
