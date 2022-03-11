import pathlib
import pandas as pd
import numpy as np

from ltemch import mchs

PATH = pathlib.Path("./")
USECOLS = ['Band', 'Test Item', 'Ch', 'Result']



class Csv2pt:
    def __init__(self, path, cols):
        self.path = path
        self.cols = cols

    def mch_judge(self, ch, mch):
        if ch < mch:
            return '-1'
        elif ch > mch:
            return '0'
        else:
            return '1'

    def refresh(self):
        for file in self.path.iterdir():
            if file.match('*.csv'):  # to find *csv file
                # load the csv and skip the first row and the second row is the colums
                self.df = pd.read_csv(file, on_bad_lines='skip', skiprows=[0], usecols=self.cols)
                # split the Test Item by ';'
                self.df[['Test Item', 'BW', 'Modulation']] = self.df['Test Item'].str.split(';', expand=True)
                # df['BW'] = df['Test Item'].str.split(';').str[1]

                # add the channel judgement to L/M/H
                self.df['channel'] = np.nan

                for b in set(self.df.Band):
                    self.df.loc[self.df.Band == b, 'channel'] = self.df.loc[self.df.Band == b, 'Ch'].apply(
                        self.mch_judge, args=(mchs[b],))

    def condtion(self):
        # filter what we want, and this can be modified
        self.prb_pwr_condition = (self.df['Test Item'].str.contains('Adjacent Channel Power') &
                                  self.df['Modulation'].str.contains('QPSK-PRB@0')
                                  )
        self.frb_pwr_condition = (self.df['Test Item'].str.contains('Adjacent Channel Power') &
                                  self.df['Modulation'].str.contains('QPSK-FRB')
                                  )
        self.frb_16qam_pwr_condition = (self.df['Test Item'].str.contains('Adjacent Channel Power') &
                                  self.df['Modulation'].str.contains('16QAM-FRB')
                                  )
        self.prb_aclr_condition = (self.df['Test Item'].str.contains('UTRA') &
                                  self.df['Modulation'].str.contains('QPSK-PRB@0')
                                  )
        self.frb_aclr_condition = (self.df['Test Item'].str.contains('UTRA') &
                                  self.df['Modulation'].str.contains('QPSK-FRB')
                                  )
        self.frb_16qam_aclr_condition = (self.df['Test Item'].str.contains('UTRA') &
                                  self.df['Modulation'].str.contains('16QAM-FRB')
                                  )

    def pwr(self):
        # this begins to transfer to pivot table
        self.df_prb_pwr = self.df[self.prb_pwr_condition]
        self.df_frb_pwr = self.df[self.frb_pwr_condition]
        self.df_frb_16qam_pwr = self.df[self.frb_16qam_pwr_condition]

        self.pt_prb_pwr = self.df_prb_pwr.pivot_table(index='Band', columns=['BW', 'channel'], values='Result',
                                                      aggfunc='max')
        self.pt_frb_pwr = self.df_frb_pwr.pivot_table(index='Band', columns=['BW', 'channel'], values='Result',
                                                      aggfunc='max')
        self.pt_frb_16qam_pwr = self.df_frb_16qam_pwr.pivot_table(index='Band', columns=['BW', 'channel'], values='Result',
                                                      aggfunc='max')
        # print(df_frb_pwr[['Ch', 'Result']].head(20))
        print(self.pt_prb_pwr)
        print(self.pt_frb_pwr)
        print(self.pt_frb_16qam_pwr)

    def aclr(self):
        self.df_prb_aclr = self.df[self.prb_aclr_condition]
        self.df_frb_aclr = self.df[self.frb_aclr_condition]
        self.df_frb_16qam_aclr = self.df[self.frb_16qam_aclr_condition]

        self.pt_prb_aclr = self.df_prb_aclr.pivot_table(index='Band', columns=['BW', 'channel'], values='Result',
                                                      aggfunc='max')
        self.pt_frb_aclr = self.df_frb_aclr.pivot_table(index='Band', columns=['BW', 'channel'], values='Result',
                                                      aggfunc='max')
        self.pt_frb_16qam_aclr = self.df_frb_16qam_aclr.pivot_table(index='Band', columns=['BW', 'channel'], values='Result',
                                                      aggfunc='max')
        # print(df_frb_pwr[['Ch', 'Result']].head(20))
        print(self.pt_prb_aclr)
        print(self.pt_frb_aclr)
        print(self.pt_frb_16qam_aclr)



def main():
    csv2pt = Csv2pt(PATH, USECOLS)
    csv2pt.refresh()
    csv2pt.condtion()
#    csv2pt.pwr()
    csv2pt.aclr()


if __name__ == '__main__':
    main()
