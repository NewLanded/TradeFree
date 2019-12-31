from utils.constant_util import CASH_DEPOSIT, CLONG, CSHORT
from utils.exception_util import SymbolNotFoundError
from .abs_execution import ExecutionHandler
from ..future_event import FillEvent


class FutureExecutionHandler(ExecutionHandler):
    """
    回测用, 简单实现
    """

    def __init__(self, event_queue, bars, portfolio):
        """
        Parameters:
        events - The Queue of Event objects.
        """
        self.bars = bars
        self.event_queue = event_queue
        self.portfolio = portfolio

    def execute_order(self, event):
        """
        使用Order objects, 生成Fill objects

        Parameters:
        event - Contains an Event object with order information.
        """
        bar_now = self.bars.get_latest_bars(event.symbol, N=1)
        price = bar_now.iloc[-1]['open']
        order_date = bar_now.index[0].to_pydatetime()

        event_id = event.event_id
        symbol = event.symbol
        order_type = event.order_type
        quantity = event.quantity
        direction = event.direction

        if self.cash_enough_judge(price, symbol, quantity, order_type) is False:
            return

        #############
        # 此处真实下单
        pass
        #############

        fill_event = FillEvent(event_id, symbol, order_date, '', quantity, direction, order_type, price)
        self.event_queue.put(fill_event, put_left_flag=True)  # 将这个event加到队列的最左边, 下一次就一定会计算这个event, 就可以及时的更新持仓, 就可以通过持仓判断现金不足等事物

    def cash_enough_judge(self, price, symbol, quantity, order_type):
        """判断交易的现金是否足够"""
        symbol = symbol.split(".")[0][:-4]
        if order_type in (CLONG, CSHORT):
            return True

        if symbol not in CASH_DEPOSIT:
            raise SymbolNotFoundError

        trade_unit_num = CASH_DEPOSIT[symbol]['trade_unit_num']
        cash_deposit_percent = CASH_DEPOSIT[symbol]['cash_deposit_percent']
        cash_deposit_per = price * trade_unit_num * cash_deposit_percent
        cash_deposit = cash_deposit_per * quantity

        if self.portfolio.current_holdings['cash'] > cash_deposit:
            return True

        return False
