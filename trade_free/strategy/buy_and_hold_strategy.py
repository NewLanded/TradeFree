from utils.constant_util import BUY, LMT
from .abs_strategy import AbsStrategy
from ..event import SignalEvent


class BuyAndHoldStrategy(AbsStrategy):
    """
    策略示例: 买入并持有, 可以作为判断其他策略结果的基准
    """

    def __init__(self, bars, event_queue, position, holding):
        super().__init__(bars, event_queue, position, holding)
        self.bought = self._calculate_initial_bought()

    def _calculate_initial_bought(self):
        """
        Adds keys to the bought dictionary for all symbols
        and sets them to False.
        """
        bought = {}
        for symbol in self.symbol_list:
            if symbol not in bought:
                bought[symbol] = False
        return bought

    def calculate_signals(self, event):
        """
        实现策略, 买入并持有

        Parameters
        event - A MarketEvent object.
        """

        for symbol in self.symbol_list:
            if self.position[symbol] != 0:
                self.bought[symbol] = True

            bars = self.bars.get_latest_bars(symbol, N=1)
            if bars:
                if self.bought[symbol] is False:
                    per_symbol_cash = self.holding["cash"] / len(self.symbol_list)
                    quantity = per_symbol_cash // bars[-1][5] // 100 * 100
                    price = bars[-1][5]

                    signal = SignalEvent(event.event_id, symbol, BUY, LMT, quantity, price, bars[-1][1])
                    self.event_queue.put(signal)
