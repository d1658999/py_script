import pathlib
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

from ltemch import mchs
from test_items import pwr_items, aclr_items, evm_items

PATH = pathlib.Path("./")
USECOLS = ['Band', 'Test Item', 'Ch', 'Result']
ITEMS = [pwr_items, aclr_items, evm_items]
ITEMS_INDEX = {'pwr': 0, 'aclr': 1, 'evm': 2}
MODULATIONS = ['QPSK-PRB@0', 'QPSK-FRB', '16QAM-FRB']
ACLR_LIMITS = {'-UTRA': -32.2, '-EUTRA': -29.2}


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

    def pwr(self):
        # this begins to transfer to pivot table
        self.df_pwr, self.pt_pwr = self._csv2pt(self.df, self.condition, ITEMS_INDEX['pwr'])

    def aclr(self):
        self.df_aclr, self.pt_aclr = self._csv2pt(self.df, self.condition, ITEMS_INDEX['aclr'])

    def evm(self):
        self.df_evm, self.pt_evm = self._csv2pt(self.df, self.condition, ITEMS_INDEX['evm'])

    def pwr_linechart(self):
        self._linechart(pwr_items, self.df_pwr)

    def evm_linechart(self):
        self._linechart(evm_items, self.df_evm)

    def aclr_linechart(self):
        self._linechart(aclr_items, self.df_aclr, ACLR_LIMITS, hline_bool=True)
        # for item in aclr_items:
        #     for bw in set(self.df[self.df['Test Item'].str.contains(item)].BW):
        #         legend_label = []
        #         plt.figure(figsize=(20, 10))
        #         for mod in MODULATIONS:
        #             legend_label.append(bw+'_'+mod)
        #             print(item, mod, bw)
        #             self._plotlines(self.df_aclr, item, mod, bw, ACLR_LIMITS[item])
        #
        #         plt.title(item)
        #         plt.legend(legend_label)
        #         plt.grid(True)
        #
        #         plt.savefig(f'{item}_{bw}.png', dpi=300)
        #         #plt.show()

    def _linechart(self, want_items, df_item, limit=None, hline_bool=False):
        for item in want_items:
            for bw in set(self.df[self.df['Test Item'].str.contains(item)].BW):
                legend_label = []
                plt.figure(figsize=(20, 10))
                for mod in MODULATIONS:
                    legend_label.append(bw+'_'+mod)
                    print(item, mod, bw)
                    if limit != None:
                        self._plotlines(df_item, item, mod, bw, limit=limit[item], hlines=hline_bool)
                    else:
                        self._plotlines(df_item, item, mod, bw)


                plt.title(item)
                plt.legend(legend_label)
                plt.grid(True)
                plt.savefig(f'{item}_{bw}.png', dpi=300)

        # for item in self.df_pwr:
        #     for mod in self.df_pwr[item]:
        #         for bw in set(self.df_pwr[item][mod].BW):
        #             df_pwr_item_mod = self.df_pwr[item][mod]
        #             df_pwr_item_mod_bw = df_pwr_item_mod[df_pwr_item_mod.BW == bw]
        #             values = range(len(df_pwr_item_mod_bw.index))
        #             x = df_pwr_item_mod_bw.Band.astype(str).str.cat(df_pwr_item_mod_bw[['BW', 'channel']], sep='_')
        #             plt.plot(x, df_pwr_item_mod_bw.Result, '-o')
        #             plt.xticks(values, x, rotation=90)
        #             plt.grid(True)
        #             plt.show()
        #             print(mod, bw)
    @staticmethod
    def _plotlines(df, item, mod, bw, limit=None, hlines=False):
        df_item_mod = df[item][mod]
        df_item_mod_bw = df_item_mod[df_item_mod.BW == bw]
        values = range(len(df_item_mod_bw.index))
        x = df_item_mod_bw.Band.astype(str).str.cat(df_item_mod_bw[['BW', 'channel']], sep='_')
        plt.plot(values, df_item_mod_bw.Result, '-o')
        if hlines == True:
            plt.hlines(y=limit, xmin=0, xmax=len(df_item_mod_bw.index), linewidth=2, color='r', linestyles='--')
        plt.xticks(values, x, rotation=90)







                    # df_pwr_mod_bw = self.df_pwr[self.df_pwr[item][mod].BW == bw]
                    # values = range(len(df_pwr_mod_bw.index))
                    # x = df_pwr_mod_bw.astype(str).str.cat(df_pwr_mod_bw.channel, sep='_')
                    # plt.plot(values, df_pwr_mod_bw, '-o')
                    # plt.xticks(values, x, rotation=90)
                    # plt.show()




        # self.df_prb = self.df_pwr['Adjacent Channel Power']['QPSK-PRB@0']
        # self.df_prb_5M = self.df_prb[self.df_prb.BW == '5MHZ']
        # self.df_prb_20M = self.df_prb[self.df_prb.BW == '20MHZ']
        # x1 = self.df_prb_5M.Band.astype(str).str.cat(self.df_prb_5M.channel, sep='_')
        #
        #
        # values1 = range(len(self.df_prb_5M.index))  #use. index is faster slightly
        # values2 = range(len(self.df_prb_20M.index))
        # plt.plot(values1, self.df_prb_5M['Result'], '-o')
        # plt.plot(values2, self.df_prb_20M['Result'], '-o')

        # plt.xticks(values1, x1, rotation=90)
        # plt.show()

    def colorcode(self):
        pass

    def save_fig(self):
        pass

    def savefiles(self):
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
    csv2pt.pwr()
    csv2pt.aclr()
    csv2pt.evm()
    csv2pt.pwr_linechart()
    csv2pt.aclr_linechart()
    csv2pt.evm_linechart()


if __name__ == '__main__':
    main()
