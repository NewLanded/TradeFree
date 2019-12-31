from abc import ABC, abstractmethod


class AbsStrategy(ABC):
    """
    策略抽象类, 用于生成 Signal
    """

    def __init__(self, bars, event_queue, position, holding, strategy_min_days=1):
        """
        Initialises the buy and hold strategy.

        Parameters:
        bars - The DataHandler object that provides bar information  OLHC数据
        events - The Event Queue object.  事件队列, 存放事件
        position - 当前持仓数量, dict  {"000001": 100, "000002": 200}
        holding - 当前持仓概况, dict {"cash": 现金剩余, "total": 组合总资产, "commission": 当前一笔交易手续费, "000001": 当前个券成本, "000002": 当前个券成本 ......}
        strategy_min_days - 策略需要的最少的前置数据天数
        """
        self.bars = bars
        self.symbol_list = self.bars.symbol_list
        self.event_queue = event_queue
        self.position = position
        self.holding = holding
        self.strategy_min_days = strategy_min_days

    @abstractmethod
    def calculate_signals(self, event):
        """
        Provides the mechanisms to calculate the list of signals.
        应该产生SignalEvent并加入到event_queue
        """

    def calc_bs_quantity(self, cash, point):
        return cash // point // 100 * 100
