import os

import pandas as pd

from .abs_data import AbsDataHandler
from ..event import MarketEvent


class HistoricCSVDataHandler(AbsDataHandler):
    """
    读取CSV数据
    """

    def __init__(self, csv_dir, symbol_list):
        """
        Parameters:
        event_queue - The Event Queue. 事件队列, 存放事件
        csv_dir - Absolute directory path to the CSV files.  # csv文件所在目录
        symbol_list - A list of symbol strings.  # csv文件名称, list, 可指定多个名称
        """
        self.csv_dir = csv_dir
        self.symbol_list = symbol_list

        self.symbol_data = {}  # 存放初始化的所有数据
        self.latest_symbol_data = {}  # 存放最新数据
        self.bar_generator = {}  # 设计使用生成器获取下一个bar, 这里存放生成器

        # self.continue_backtest = True  # 用来控制回测是否终止

    def init_data(self, start_date, end_date):
        self._open_convert_csv_files(start_date, end_date)
        self._set_bar_generator()

    def register_event_queue(self, event_queue):
        self.event_queue = event_queue

    def _open_convert_csv_files(self, start_date, end_date):
        """
        Opens the CSV files from the data directory, converting
        them into pandas DataFrames within a symbol dictionary.
        """
        comb_index = None
        for symbol_now in self.symbol_list:
            # CSV中的数据结构应该是 没有表头的, 数据顺序是 'datetime', 'open', 'low', 'high', 'close', 'turnover_rate', 'pct_chg'  # turnover_rate 是换手率
            csv_data = pd.read_csv(
                os.path.join(self.csv_dir, '{0}.csv'.format(symbol_now)),
                header=None, index_col=0, parse_dates=[0],
                names=['datetime', 'open', 'low', 'high', 'close', 'turnover_rate', 'pct_chg'])

            self.symbol_data[symbol_now] = csv_data[start_date: end_date]

            # Combine the index to ffill forward values
            if comb_index is None:
                comb_index = self.symbol_data[symbol_now].index
            else:
                comb_index.union(self.symbol_data[symbol_now].index)

            # Set the latest symbol_data to None
            self.latest_symbol_data[symbol_now] = []

        # Reindex the dataframes
        for symbol_now in self.symbol_list:
            self.symbol_data[symbol_now] = self.symbol_data[symbol_now].reindex(index=comb_index, method='ffill')

    def get_latest_bars(self, symbol, N=1, frame_flag=True):
        """
        Returns the last N bars from the latest_symbol list,
        or N-k if less available.
        """
        try:
            bars_list = self.latest_symbol_data[symbol]
        except KeyError:
            print("That symbol is not available in the historical data set.")
        else:
            if frame_flag is False:
                return bars_list[-N:]
            else:
                bars_list = bars_list[-N:]
                bars_frame = pd.DataFrame(bars_list, columns=['sybmbol', 'datetime', 'open', 'low', 'high', 'close', 'turnover_rate', 'pct_chg'])
                return bars_frame

    def _set_bar_generator(self):
        for symbol_now in self.symbol_list:
            self.bar_generator[symbol_now] = zip(self.symbol_data[symbol_now].index, self.symbol_data[symbol_now].values)

    def _get_new_bar(self, symbol):
        """
        Returns the latest bar from the data feed as a tuple of
        (sybmbol, datetime, 'open', 'low', 'high', 'close', 'turnover_rate', 'pct_chg').
        """
        bar = next(self.bar_generator[symbol])
        return tuple([symbol, bar[0], bar[1][0], bar[1][1], bar[1][2], bar[1][3], bar[1][4], bar[1][5]])

    def update_bars(self):
        """
        Pushes the latest bar to the latest_symbol_data structure
        for all symbols in the symbol list.
        """
        for symbol_now in self.symbol_list:
            try:
                bar = self._get_new_bar(symbol_now)
            except StopIteration:
                raise StopIteration("数据已遍历完成")
                # self.continue_backtest = False
                # break
            else:
                if bar:
                    self.latest_symbol_data[symbol_now].append(bar)

        self.event_queue.put(MarketEvent())
