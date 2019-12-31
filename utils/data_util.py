from utils.constant_util import CASH_DEPOSIT
from utils.exception_util import SymbolNotFoundError


def get_future_trade_unit_num_and_cash_deposit_percent(symbol):
    symbol = symbol.split(".")[0][:-4]

    if symbol not in CASH_DEPOSIT:
        raise SymbolNotFoundError

    trade_unit_num = CASH_DEPOSIT[symbol]['trade_unit_num']
    cash_deposit_percent = CASH_DEPOSIT[symbol]['cash_deposit_percent']

    return trade_unit_num, cash_deposit_percent
