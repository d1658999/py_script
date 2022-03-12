import pathlib
import pandas as pd
import numpy as np

from ltemch import mchs
from test_items import pwr_items, aclr_items, evm_items

PATH = pathlib.Path("./")
USECOLS = ['Band', 'Test Item', 'Ch', 'Result']
ITEMS = [pwr_items, aclr_items, evm_items]
ITEMS_INDEX = {'pwr': 0, 'aclr': 1, 'evm': 2}
MODULATIONS = ['QPSK-PRB@0', 'QPSK-FRB', '16QAM-FRB']


class Csv2pt:
    def __init__(self, path, cols):
        self.path = path
        self.cols = cols

    def _mch_judge(self, ch, mch):
        if ch < mch:
            return '-1'
        elif ch > mch:
            return '1'
        else:
            return '0'

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
                        self._mch_judge, args=(mchs[b],))

    def conditions(self):
        # self.pwr_condition = {}
        # self.aclr_condition = {}
        self.condition = {}
        for items in ITEMS:
            for item in items:
                self.condition[item] = {}
                for mod in MODULATIONS:
                    self.condition[item][mod] = (self.df['Test Item'].str.contains(item) &
                                                 self.df['Modulation'].str.contains(mod))
                # self.pwr_condition[mod] = (self.df['Test Item'].str.contains('Adjacent Channel Power') &
                #                            self.df['Modulation'].str.contains(mod))
                # self.aclr_condition[mod] = (self.df['Test Item'].str.contains('-UTRA') &
                #                        self.df['Modulation'].str.contains(mod))

        # filter what we want, and this can be modified
        # self.prb_pwr_condition = (self.df['Test Item'].str.contains('Adjacent Channel Power') &
        #                           self.df['Modulation'].str.contains('QPSK-PRB@0')
        #                           )
        # self.frb_pwr_condition = (self.df['Test Item'].str.contains('Adjacent Channel Power') &
        #                           self.df['Modulation'].str.contains('QPSK-FRB')
        #                           )
        # self.frb_16qam_pwr_condition = (self.df['Test Item'].str.contains('Adjacent Channel Power') &
        #                           self.df['Modulation'].str.contains('16QAM-FRB')
        #                           )
        # self.prb_aclr_condition = (self.df['Test Item'].str.contains('UTRA') &
        #                           self.df['Modulation'].str.contains('QPSK-PRB@0')
        #                           )
        # self.frb_aclr_condition = (self.df['Test Item'].str.contains('UTRA') &
        #                           self.df['Modulation'].str.contains('QPSK-FRB')
        #                           )
        # self.frb_16qam_aclr_condition = (self.df['Test Item'].str.contains('UTRA') &
        #                           self.df['Modulation'].str.contains('16QAM-FRB')
        #                           )

    def pwr(self):
        # this begins to transfer to pivot table
        self.df_pwr, self.pt_pwr = self._csv2pt(self.df, self.condition, ITEMS_INDEX['pwr'])

        # self.df_pwr = {}
        # self.pt_pwr = {}
        # for pwr_type in ITEMS[0]:
        #     self.df_pwr[pwr_type] = {}
        #     self.pt_pwr[pwr_type] = {}
        #     for mod in MODULATIONS:
        #         self.df_pwr[mod] = self.df[self.condition[pwr_type][mod]]
        #         # self.df_pwr[mod] = self.df[self.condition[mod]]
        #         self.pt_pwr[mod] = self.df_pwr[mod].pivot_table(index='Band', columns=['BW', 'channel'],
        #                                                         values='Result',
        #                                                         aggfunc='max')

        # self.df_prb_pwr = self.df[self.prb_pwr_condition]
        # self.df_frb_pwr = self.df[self.frb_pwr_condition]
        # self.df_frb_16qam_pwr = self.df[self.frb_16qam_pwr_condition]
        #
        # self.pt_prb_pwr = self.df_prb_pwr.pivot_table(index='Band', columns=['BW', 'channel'], values='Result',
        #                                               aggfunc='max')
        # self.pt_frb_pwr = self.df_frb_pwr.pivot_table(index='Band', columns=['BW', 'channel'], values='Result',
        #                                               aggfunc='max')
        # self.pt_frb_16qam_pwr = self.df_frb_16qam_pwr.pivot_table(index='Band', columns=['BW', 'channel'], values='Result',
        #                                               aggfunc='max')
        # # print(df_frb_pwr[['Ch', 'Result']].head(20))
        # print(self.pt_prb_pwr)
        # print(self.pt_frb_pwr)
        # print(self.pt_frb_16qam_pwr)

    def aclr(self):
        self.df_aclr, self.pt_aclr = self._csv2pt(self.df, self.condition, ITEMS_INDEX['aclr'])

        # self.df_aclr = {}
        # self.pt_aclr = {}
        # for aclr_type in ITEMS[1]:
        #     self.df_aclr[aclr_type] = {}
        #     self.pt_aclr[aclr_type] = {}
        #     for mod in MODULATIONS:
        #         self.df_aclr[aclr_type][mod] = self.df[self.condition[aclr_type][mod]]
        #
        #         # self.df_aclr[mod] = self.df[self.aclr_condition[mod]]
        #         self.pt_aclr[aclr_type][mod] = self.df_aclr[aclr_type][mod].pivot_table(index='Band',
        #                                                                                 columns=['BW', 'channel'],
        #                                                                                 values='Result',
        #                                                                                 aggfunc='max')

        # self.df_prb_aclr = self.df[self.prb_aclr_condition]
        # self.df_frb_aclr = self.df[self.frb_aclr_condition]
        # self.df_frb_16qam_aclr = self.df[self.frb_16qam_aclr_condition]
        #
        # self.pt_prb_aclr = self.df_prb_aclr.pivot_table(index='Band', columns=['BW', 'channel'], values='Result',
        #                                               aggfunc='max')
        # self.pt_frb_aclr = self.df_frb_aclr.pivot_table(index='Band', columns=['BW', 'channel'], values='Result',
        #                                               aggfunc='max')
        # self.pt_frb_16qam_aclr = self.df_frb_16qam_aclr.pivot_table(index='Band', columns=['BW', 'channel'], values='Result',
        #                                               aggfunc='max')
        # # print(df_frb_pwr[['Ch', 'Result']].head(20))
        # print(self.pt_prb_aclr)
        # print(self.pt_frb_aclr)
        # print(self.pt_frb_16qam_aclr)

    def evm(self):
        self.df_evm, self.pt_evm = self._csv2pt(self.df, self.condition, ITEMS_INDEX['evm'])

        # self.df_evm = {}
        # self.pt_evm = {}
        # for evm_type in ITEMS[2]:
        #     self.df_evm[evm_type] = {}
        #     self.pt_evm[evm_type] = {}
        #     for mod in MODULATIONS:
        #         self.df_evm[evm_type][mod] = self.df[self.condition[evm_type][mod]]
        #         self.pt_evm[evm_type][mod] = self.df_evm[evm_type][mod].pivot_table(index='Band',
        #                                                                             columns=['BW', 'channel'],
        #                                                                             values='Result',
        #                                                                             aggfunc='max')

    def _csv2pt(self, df, condition, index):
        df_want = {}
        pt_want = {}
        for _type in ITEMS[index]:
            df_want[_type] = {}
            pt_want[_type] = {}
            for mod in MODULATIONS:
                df_want[_type][mod] = df[condition[_type][mod]]

                # self.df_aclr[mod] = self.df[self.aclr_condition[mod]]
                pt_want[_type][mod] = df_want[_type][mod].pivot_table(index='Band',
                                                                      columns=['BW', 'channel'],
                                                                      values='Result',
                                                                      aggfunc='max')
        return df_want, pt_want

    def linechart(self):
        pass

    def colorcode(self):
        pass


def main():
    csv2pt = Csv2pt(PATH, USECOLS)
    csv2pt.refresh()
    csv2pt.conditions()
    csv2pt.pwr()
    csv2pt.aclr()
    csv2pt.evm()


if __name__ == '__main__':
    main()
