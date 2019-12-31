import datetime

from utils.db_data_util import SecurityData
from .abs_data import AbsDataHandler
from ..future_event import MarketEvent


class FutureHistoricDatabaseDataHandler(AbsDataHandler):
    """
    读取数据库数据
    """

    def __init__(self, symbol_list):
        """
        Parameters:
        event_queue - The Event Queue. 事件队列, 存放事件
        symbol_list - A list of symbol strings.  # csv文件名称, list, 可指定多个名称
        """
        self.symbol_list = symbol_list

        self.symbol_data = {}  # 存放初始化的所有数据
        self.latest_symbol_data = {}  # 存放最新数据
        self.bar_index_generator = {}  # 下一个bar的索引

    def register_event_queue(self, event_queue):
        self.event_queue = event_queue

    def init_data(self, start_date, end_date):
        self._get_database_data(start_date, end_date)
        self._set_bar_generator()

    def _get_database_data(self, start_date=datetime.datetime(1990, 1, 1), end_date=datetime.datetime(2199, 12, 31)):
        comb_index = None
        for symbol_now in self.symbol_list:
            # 数据是 'datetime', 'open', 'low', 'high', 'close', 'turnover_rate', 'pct_chg'  # turnover_rate 是换手率
            security_point_data = SecurityData().get_future_security_point_data(symbol_now, start_date, end_date)
            security_point_data["turnover_rate"] = None
            security_point_data["pct_chg"] = None
            security_point_data.drop(['ts_code', 'vol'], axis=1, inplace=True)

            self.symbol_data[symbol_now] = security_point_data

            # Combine the index to ffill forward values
            if comb_index is None:
                comb_index = self.symbol_data[symbol_now].index
            else:
                comb_index.union(self.symbol_data[symbol_now].index)

            # Set the latest symbol_data to None
            self.latest_symbol_data[symbol_now] = None

        # Reindex the dataframes
        for symbol_now in self.symbol_list:
            self.symbol_data[symbol_now] = self.symbol_data[symbol_now].reindex(index=comb_index, method='ffill')

        self.min_index_date = min(comb_index)

    def _set_bar_generator(self):
        for symbol_now in self.symbol_list:
            self.bar_index_generator[symbol_now] = iter(range(len(self.symbol_data[symbol_now].index)))

    def get_latest_bars(self, symbol, N=0):
        """
        Returns the last N bars from the latest_symbol list,
        or N-k if less available.
        """
        try:
            bars_data = self.latest_symbol_data[symbol]
        except KeyError:
            print("That symbol is not available in the historical data set.")
        else:
            bars_frame = bars_data.iloc[-N:]
            return bars_frame

    def update_bars(self):
        """
        Pushes the latest bar to the latest_symbol_data structure
        for all symbols in the symbol list.
        """
        for symbol_now in self.symbol_list:
            try:
                bar_index = next(self.bar_index_generator[symbol_now])
            except StopIteration:
                raise StopIteration("数据已遍历完成")
            else:
                self.latest_symbol_data[symbol_now] = self.symbol_data[symbol_now].iloc[:bar_index + 1]

        self.event_queue.put(MarketEvent())
