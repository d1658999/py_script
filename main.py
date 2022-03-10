import pathlib
import pandas as pd
import numpy as np

from ltemch import mchs


def Mch_judge(ch, mch):
    if ch < mch:
        return 'L'
    elif ch> mch:
        return 'H'
    else:
        return 'M'

def csv2pivot_table():
    path = pathlib.Path("./")
    usecols = ['Band', 'Test Item', 'Ch', 'Result']

    for file in path.iterdir():
        if file.match('*.csv'):  # to find *csv file
            # print(file)
            df = pd.read_csv(file, on_bad_lines='skip', skiprows=[0],
                             usecols=usecols)  # load the csv and skip the first row and the second row is the colums
            df[['Test Item', 'BW', 'Modulation']] = df['Test Item'].str.split(';',
                                                                              expand=True)  # split the Test Item by ';'
            # df['BW'] = df['Test Item'].str.split(';').str[1]

            # add the channel judgement to L/M/H
            df['channel'] = np.nan

            for b in set(df.Band):
                df.loc[df.Band==b, 'channel'] = df.loc[df.Band==b, 'Ch'].apply(Mch_judge, args=(mchs[b],))


            # this begins to transfer to pivot table

            prb_pwr_condition = (df['Test Item'].str.contains('Adjacent Channel Power') &
                         df['Modulation'].str.contains('QPSK-PRB@0'))  # filter what we want, and this can be modified
            frb_pwr_condition = (df['Test Item'].str.contains('Adjacent Channel Power') &
                                 df['Modulation'].str.contains('QPSK-FRB'))  # filter what we want, and this can be modified

            df_prb_pwr = df[prb_pwr_condition]
            df_frb_pwr = df[frb_pwr_condition]

            pt_prb_pwr = df_prb_pwr.pivot_table(index='Band', columns=['BW', 'channel'], values='Result', aggfunc='max')
            pt_frb_pwr = df_frb_pwr.pivot_table(index='Band', columns=['BW', 'channel'], values='Result', aggfunc='max')
            #print(df_frb_pwr[['Ch', 'Result']].head(20))
            print(pt_frb_pwr)

def main():
    csv2pivot_table()


if __name__ == '__main__':
    main()
