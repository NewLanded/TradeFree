import datetime
import math

from utils.constant_util import LONG, CSHORT, SHORT, CLONG, CASH_DEPOSIT
from utils.data_util import get_future_trade_unit_num_and_cash_deposit_percent
from utils.exception_util import SymbolNotFoundError
from .abs_portfolio import AbsPortfolio
from ..future_event import OrderEvent


class FuturePortfolio(AbsPortfolio):
    """
    期货Portfolio
    """

    def __init__(self, start_date, event_queue, bars, initial_capital):
        """
        Parameters:
        bars - The DataHandler object with current market data. # DataHandler对象, 当前市场数据
        events - The Event Queue object.  # 事件队列
        start_date - The start date (bar) of the portfolio.
        initial_capital - The starting capital.  # 初始现金
        """
        self.bars = bars
        self.event_queue = event_queue
        self.symbol_list = self.bars.symbol_list
        self.start_date_previous_day = start_date - datetime.timedelta(days=1)
        self.initial_capital = initial_capital

        self.all_positions = self._construct_all_positions()
        self.current_positions = dict((k, v) for k, v in [(s, 0) for s in self.symbol_list])  # 空头头寸被视为负值

        self.all_holdings = self._construct_all_holdings()
        self.current_holdings = self._construct_current_holdings()

        self.bs_data = []

    def _construct_all_positions(self):
        """
        使用start_date构造all_positions，以确定时间索引何时开始
        """
        all_positions = dict((k, v) for k, v in [(s, 0) for s in self.symbol_list])
        all_positions['datetime'] = self.start_date_previous_day
        return [all_positions]

    def _construct_all_holdings(self):
        """
        使用start_date构造all_holdings，以确定时间索引何时开始
        """
        all_holdings = dict((k, v) for k, v in [(s, 0.0) for s in self.symbol_list])
        all_holdings['datetime'] = self.start_date_previous_day
        all_holdings['cash'] = self.initial_capital  # 现金
        all_holdings['commission'] = 0.0  # 累计佣金
        all_holdings['total'] = self.initial_capital  # 包括现金和任何未平仓头寸在内的总账户资产
        return [all_holdings]

    def _construct_current_holdings(self):
        """
        和construct_all_holdings类似, 但是只作用于当前时刻
        """
        current_holdings = dict((k, v) for k, v in [(s, 0.0) for s in self.symbol_list])  # 空头头寸是正值
        current_holdings['cash'] = self.initial_capital
        current_holdings['commission'] = 0.0
        current_holdings['total'] = self.initial_capital
        return current_holdings

    def update_signal(self, event):
        """
        接收SignalEvent, 生成订单Event
        """
        # if event.type == 'SIGNAL':
        order_event = self.generate_naive_order(event)
        self.event_queue.put(order_event)

    def generate_naive_order(self, signal):
        """
        简单的生成OrderEvent, 不考虑风控等
        Parameters:
        signal - The SignalEvent signal information.
        """
        order = None

        symbol = signal.symbol
        event_id = signal.event_id
        direction = signal.direction
        order_type = signal.order_type
        mkt_quantity = signal.quantity
        mkt_price = signal.price
        single_date = signal.single_date

        """
        # 此处执行风控
        """

        if mkt_quantity:
            order = OrderEvent(event_id, symbol, order_type, mkt_quantity, mkt_price, direction, single_date)

        return order

    def update_fill(self, event):
        """
        使用FillEvent更新持仓
        """
        # if event.type == 'FILL':
        self.update_positions_from_fill(event)
        self.update_holdings_from_fill(event)
        self.update_bs_data_from_fill(event)

    def update_positions_from_fill(self, fill):
        """
        使用FilltEvent对象并更新 position
        Parameters:
        fill - The FillEvent object to update the positions with.
        """
        # Check whether the fill is a buy or sell
        fill_dir = 0
        if fill.direction in (LONG, CSHORT):
            fill_dir = 1
        if fill.direction in (SHORT, CLONG):
            fill_dir = -1

        # Update positions list with new quantities
        self.current_positions[fill.symbol] += fill_dir * fill.quantity

    def update_bs_data_from_fill(self, fill):
        """记录buy sell 数据"""
        open_point = self.bars.get_latest_bars(fill.symbol).iloc[-1]['open']
        bs_data = {"bs_date": fill.fill_date, "direction": fill.direction, "quantity": fill.quantity, "price": open_point, "symbol": fill.symbol}

        self.bs_data.append(bs_data)

    def update_holdings_from_fill(self, fill):
        """
        使用FilltEvent对象并更新 holding
        Parameters:
        fill - The FillEvent object to update the holdings with.
        """
        # Update holdings list with new quantities
        symbol = fill.symbol
        trade_unit_num, cash_deposit_percent = get_future_trade_unit_num_and_cash_deposit_percent(symbol)

        fill_cost = self.bars.get_latest_bars(fill.symbol).iloc[-1]['open']  # Open price
        cash_deposit = fill_cost * fill.quantity * trade_unit_num * cash_deposit_percent

        if fill.direction in (LONG, SHORT):
            cash_deposit = abs(cash_deposit)
        else:
            cash_deposit = -abs(cash_deposit)

        self.current_holdings[fill.symbol] += cash_deposit
        self.current_holdings['commission'] += fill.commission
        self.current_holdings['cash'] -= (cash_deposit + fill.commission)
        self.current_holdings['total'] -= fill.commission

    def update_timeindex(self):
        """
        添加新纪录到positions, 使用队列中的 MarketEvent
        """
        bars = {}
        for symbol in self.symbol_list:
            bars[symbol] = self.bars.get_latest_bars(symbol, N=1)

        # Update positions
        data_position = dict((k, v) for k, v in [(s, 0) for s in self.symbol_list])
        data_position['datetime'] = bars[self.symbol_list[0]].iloc[-1]['trade_date']

        for symbol in self.symbol_list:
            data_position[symbol] = self.current_positions[symbol]

        # Append the current positions
        self.all_positions.append(data_position)

        # Update holdings
        data_holding = {}
        data_holding['datetime'] = bars[self.symbol_list[0]].iloc[-1]['trade_date']
        data_holding['commission'] = self.current_holdings['commission']

        for symbol in self.symbol_list:
            # Approximation to the real value
            data_holding[symbol + "_close"] = bars[symbol].iloc[-1]['close']

            trade_unit_num, cash_deposit_percent = get_future_trade_unit_num_and_cash_deposit_percent(symbol)
            ori_cash_deposit = self.current_holdings[symbol]
            now_cash_deposit = abs(self.current_positions[symbol]) * bars[symbol].iloc[-1]['close'] * trade_unit_num * cash_deposit_percent
            cash_deposit_diff = now_cash_deposit - ori_cash_deposit

            self.current_holdings[symbol] = now_cash_deposit
            self.current_holdings['cash'] -= cash_deposit_diff
            self.current_holdings['total'] -= cash_deposit_diff

            profit = cash_deposit_diff / cash_deposit_percent
            if self.current_positions[symbol] < 0:
                profit = -profit
            self.current_holdings['cash'] += profit
            self.current_holdings['total'] += profit

            data_holding[symbol] = now_cash_deposit

        data_holding['cash'] = self.current_holdings['cash']
        data_holding['total'] = self.current_holdings['total']

        self.all_holdings.append(data_holding)
