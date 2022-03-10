import pathlib
import pandas as pd


def csv2pivot_table():
    path = pathlib.Path("./")
    usecols = ['Band', 'Test Item', 'Ch', 'Result']

    for file in path.iterdir():
        if file.match('*.csv'):  # to find *csv file
            df = pd.read_csv(file, on_bad_lines='skip', skiprows=[0],
                             usecols=usecols)  # load the csv and skip the first row and the second row is the colums
            df[['Test Item', 'BW', 'Modulation']] = df['Test Item'].str.split(';',
                                                                              expand=True)  # split the Test Item by ';'
            # df['BW'] = df['Test Item'].str.split(';').str[1]

            condition = (df['Test Item'].str.contains('Adjacent Channel Power') &
                         df['Modulation'].str.contains('QPSK-PRB@0'))  # filter what we want, and this can be modified

            # add the channel judgement to L/M/H

            # this begins to transfer to pivot table
            # pt = df.pivot_table(df[condition], index='Band', columns=['BW', 'Ch'], values=['Result'])

            print(df[condition].head(50))


def main():
    csv2pivot_table()


if __name__ == '__main__':
    main()

