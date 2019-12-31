import talib as ta

from utils.constant_util import MKT, CLONG, CSHORT, LONG, SHORT
from .abs_strategy import AbsStrategy
from ..future_event import SignalEvent


class Future5Penetrate30Strategy(AbsStrategy):
    def __init__(self, bars, event_queue, position, holding, strategy_min_days):
        super().__init__(bars, event_queue, position, holding, strategy_min_days)

    def calc_bs_quantity(self, cash, point):
        return 1

    def buy(self, security_point_data):
        sma_data_5 = ta.MA(security_point_data["close"], timeperiod=5, matype=0)
        sma_data_30 = ta.MA(security_point_data["close"], timeperiod=30, matype=0)

        sma_5_t, sma_5_t_1, sma_5_t_2 = sma_data_5.iloc[-1], sma_data_5.iloc[-2], sma_data_5.iloc[-3]
        sma_30_t, sma_30_t_1, sma_30_t_2 = sma_data_30.iloc[-1], sma_data_30.iloc[-2], sma_data_30.iloc[-3]

        sma_5_slope_symbol_t = 0b100 if sma_5_t - sma_5_t_1 > 0 else 0b010 if sma_5_t - sma_5_t_1 < 0 else 0b001
        sma_30_slope_symbol_t = 0b100 if sma_30_t - sma_30_t_1 > 0 else 0b010 if sma_30_t - sma_30_t_1 < 0 else 0b001

        sma_5_slope_symbol_t_1 = 0b100 if sma_5_t_1 - sma_5_t_2 > 0 else 0b010 if sma_5_t_1 - sma_5_t_2 < 0 else 0b001
        sma_30_slope_symbol_t_1 = 0b100 if sma_30_t_1 - sma_30_t_2 > 0 else 0b010 if sma_30_t_1 - sma_30_t_2 < 0 else 0b001

        if sma_5_slope_symbol_t != 0b001 and sma_30_slope_symbol_t != 0b001:
            if not sma_5_slope_symbol_t_1 & sma_30_slope_symbol_t_1:  # 昨天的方向不同
                if sma_5_slope_symbol_t & sma_30_slope_symbol_t:  # 今天的方向相同
                    return True

        return False

    def sell(self, security_point_data):
        sma_data_5 = ta.MA(security_point_data["close"], timeperiod=5, matype=0)
        sma_data_30 = ta.MA(security_point_data["close"], timeperiod=30, matype=0)

        sma_5_t, sma_5_t_1, sma_5_t_2 = sma_data_5.iloc[-1], sma_data_5.iloc[-2], sma_data_5.iloc[-3]
        sma_30_t, sma_30_t_1, sma_30_t_2 = sma_data_30.iloc[-1], sma_data_30.iloc[-2], sma_data_30.iloc[-3]

        sma_5_slope_symbol_t = 0b100 if sma_5_t - sma_5_t_1 > 0 else 0b010 if sma_5_t - sma_5_t_1 < 0 else 0b001
        sma_30_slope_symbol_t = 0b100 if sma_30_t - sma_30_t_1 > 0 else 0b010 if sma_30_t - sma_30_t_1 < 0 else 0b001

        sma_5_slope_symbol_t_1 = 0b100 if sma_5_t_1 - sma_5_t_2 > 0 else 0b010 if sma_5_t_1 - sma_5_t_2 < 0 else 0b001
        sma_30_slope_symbol_t_1 = 0b100 if sma_30_t_1 - sma_30_t_2 > 0 else 0b010 if sma_30_t_1 - sma_30_t_2 < 0 else 0b001

        if sma_5_slope_symbol_t_1 & sma_30_slope_symbol_t_1:  # 昨天方向相同
            if not sma_5_slope_symbol_t & sma_30_slope_symbol_t:  # 今天方向不相同
                return True

        if not sma_5_slope_symbol_t & sma_5_slope_symbol_t_1:  # 5日线方向变化的时候, 平仓
            return True

        return False

    def calculate_signals(self, event):
        """
        实现策略, 买入并持有

        Parameters
        event - A MarketEvent object.
        """
        for symbol in self.symbol_list:
            bars = self.bars.get_latest_bars(symbol, N=self.strategy_min_days)
            if len(bars) >= self.strategy_min_days:
                close_position_flag = self.sell(bars)
                if close_position_flag is True:
                    if self.position[symbol] != 0:
                        if self.position[symbol] > 0:
                            bs_flag = CLONG
                        else:
                            bs_flag = CSHORT
                        signal = SignalEvent(event.event_id, symbol, bs_flag, MKT, 1, None, bars.iloc[-1]['trade_date'])
                        self.event_queue.put(signal)

                open_position_flag = self.buy(bars)
                if open_position_flag is True:
                    sma_data_30 = ta.MA(bars["close"], timeperiod=30, matype=0)
                    if sma_data_30.iloc[-1] > 0:
                        bs_flag = LONG
                    else:
                        bs_flag = SHORT
                    signal = SignalEvent(event.event_id, symbol, bs_flag, MKT, 1, None, bars.iloc[-1]['trade_date'])
                    self.event_queue.put(signal)
