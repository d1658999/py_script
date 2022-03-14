import pathlib
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

from ltemch import mchs
from test_items import pwr_items, aclr_items, evm_items
from specs import aclr_usls, evm_usls

PATH = pathlib.Path("./")
USECOLS = ['Band', 'Test Item', 'Ch', 'Result']

# this _EN can be modified
PWR_EN = 1
ACLR_EN = 1
EVM_EN = 1
MODULATIONS = ['QPSK-PRB@0', 'QPSK-FRB', '16QAM-PRB@0', '16QAM-FRB', '64QAM-FRB']  # this is can be modified to we want

ITEMS = [pwr_items, aclr_items, evm_items]
ITEMS_INDEX = {'pwr': 0, 'aclr': 1, 'evm': 2}
ACLR_USLS = aclr_usls


class Csv2pt:
    def __init__(self, path, cols):
        self.path = path
        self.cols = cols

    @staticmethod
    def _mch_judge(ch, mch):
        if ch < mch:
            return 'L'
        elif ch > mch:
            return 'H'
        else:
            return 'M'

    @staticmethod
    def _select_items(df):
        # global cond
        # true_series = pd.Series([True for i in range(len(df.index))], name='Test Item')
        # flag = 0
        # for item in items:
        #     for i in item:
        #         print(item, i)
        #         if flag == 0:
        #             cond = df['Test Item'].str.contains(i) & true_series
        #             flag = 1
        #         else:
        #             cond = cond | df['Test Item'].str.contains(i)
        #
        # return df[cond]


        df = df[df['Test Item'].str.contains('6.6.2.3') |
                df['Test Item'].str.contains('6.5.2.1')]

        return df


    def refresh(self):
        for file in self.path.iterdir():
            if file.match('*.csv'):  # to find *csv file
                # load the csv and skip the first row and the second row is the colums
                self.df = pd.read_csv(file, on_bad_lines='skip', skiprows=[0], usecols=self.cols)
                # self.df = pd.read_csv(file, on_bad_lines='skip', usecols=self.cols)
                # split the Test Item by ';'
                self.df = self._select_items(self.df)
                print(self.df)
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

    def pwr(self):
        # this begins to transfer to pivot table
        self.df_pwr, self.pt_pwr = self._csv2pt(self.df, self.condition, ITEMS_INDEX['pwr'])

    def aclr(self):
        self.df_aclr, self.pt_aclr = self._csv2pt(self.df, self.condition, ITEMS_INDEX['aclr'])

    def evm(self):
        self.df_evm, self.pt_evm = self._csv2pt(self.df, self.condition, ITEMS_INDEX['evm'])

    def pwr_linechart(self):
        self._linechart_save(pwr_items, self.df_pwr)

    def evm_linechart(self):
        self._linechart_save(evm_items, self.df_evm)

    def aclr_linechart(self):
        self._linechart_save(aclr_items, self.df_aclr, ACLR_USLS)

    def _linechart_save(self, want_items, df_item, limit=None):
        global xmax_value, legend_label
        for item in want_items:
            for bw in set(self.df[self.df['Test Item'].str.contains(item)].BW):
                try:
                    legend_label = []
                    plt.figure(figsize=(20, 10))
                    xmax_value = None
                    for mod in MODULATIONS:
                        legend_label.append(bw + '_' + mod)
                        print(f'linechart is processing for {item}, {mod}, {bw}')
                        xmax_value = self._plotlines(df_item, item, mod, bw)
                except KeyError as err:
                    print(f'{err} is not in the raw data ')

                plt.title(item)
                if limit is not None:
                    print(limit[item])
                    plt.hlines(y=limit[item], xmin=0, xmax=xmax_value, linewidth=2, color='r', linestyles='--')
                    legend_label.append('USL')
                plt.legend(legend_label)
                plt.grid(True)
                plt.savefig(f'{item}_{bw}.png', dpi=300)

    @staticmethod
    def _plotlines(df, item, mod, bw):
        df_item_mod = df[item][mod]
        df_item_mod_bw = df_item_mod[df_item_mod.BW == bw]
        values = range(len(df_item_mod_bw.index))
        x = df_item_mod_bw.Band.astype(str).str.cat(df_item_mod_bw[['BW', 'channel']], sep='_')
        plt.plot(values, df_item_mod_bw.Result, '-o')
        plt.xticks(values, x, rotation=90)
        return len(x)

    def save2excel(self):
        with pd.ExcelWriter('pandas_to_excel.xlsx') as writer:
            self.df.to_excel(writer, sheet_name='raw data')
            if PWR_EN == 1:
                for item in pwr_items:
                    for mod in self.pt_pwr[item]:
                        self.pt_pwr[item][mod].to_excel(writer, sheet_name=f'Power_{mod}')
            if ACLR_EN == 1:
                for item in aclr_items:
                    for mod in self.pt_aclr[item]:
                        self.pt_aclr[item][mod].to_excel(writer, sheet_name=f'ACLR_{item}_{mod}')
            if EVM_EN == 1:
                for item in evm_items:
                    for mod in self.pt_evm[item]:
                        self.pt_evm[item][mod].to_excel(writer, sheet_name=f'EVM_{mod}')

    def colorcode(self):
        pass

    @staticmethod
    def _csv2pt(df, condition, index):
        df_want = {}
        pt_want = {}
        for _item in ITEMS[index]:
            df_want[_item] = {}
            pt_want[_item] = {}
            for mod in MODULATIONS:
                if mod in set(df[df['Test Item'].str.contains(_item)].Modulation):
                    df_want[_item][mod] = df[condition[_item][mod]]

                    # self.df_aclr[mod] = self.df[self.aclr_condition[mod]]
                    pt_want[_item][mod] = df_want[_item][mod].pivot_table(index='Band',
                                                                          columns=['BW', 'channel'],
                                                                          values='Result',
                                                                          aggfunc='max')
                else:
                    print(f'{_item}, {mod} is not in the data')
        return df_want, pt_want


def main():
    csv2pt = Csv2pt(PATH, USECOLS)
    csv2pt.refresh()
    csv2pt.conditions()
    if PWR_EN == 1:
        csv2pt.pwr()
        csv2pt.pwr_linechart()
    if ACLR_EN == 1:
        csv2pt.aclr()
        csv2pt.aclr_linechart()
    if EVM_EN == 1:
        csv2pt.evm()
        csv2pt.evm_linechart()
    csv2pt.save2excel()


if __name__ == '__main__':
    main()
