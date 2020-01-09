# 买卖方向
BUY = "B"
SELL = "S"

LONG = "Long"  # 买多
SHORT = "Short"  # 卖空
CLONG = "CLong"  # 平多
CSHORT = "CShort "  # 平空

# 下单方式
MKT = "MKT"  # 市价下单
LMT = "LMT"  # 限价下单

# 保证金
CASH_DEPOSIT = {
    #        交易手数              保证金率
    'AP': {"trade_unit_num": 10, "cash_deposit_percent": 0.11},
    'C': {"trade_unit_num": 10, "cash_deposit_percent": 0.08},
    'CF': {"trade_unit_num": 5, "cash_deposit_percent": 0.08},
    'CY': {"trade_unit_num": 5, "cash_deposit_percent": 0.08},
    'FG': {"trade_unit_num": 20, "cash_deposit_percent": 0.08},
    'HC': {"trade_unit_num": 10, "cash_deposit_percent": 0.11},
    'JD': {"trade_unit_num": 10, "cash_deposit_percent": 0.1},
    'L': {"trade_unit_num": 5, "cash_deposit_percent": 0.08},
    'M': {"trade_unit_num": 10, "cash_deposit_percent": 0.08},
    'OI': {"trade_unit_num": 10, "cash_deposit_percent": 0.08},
    'P': {"trade_unit_num": 10, "cash_deposit_percent": 0.08},
    'RB': {"trade_unit_num": 10, "cash_deposit_percent": 0.11},
    'RM': {"trade_unit_num": 10, "cash_deposit_percent": 0.09},
    'SR': {"trade_unit_num": 10, "cash_deposit_percent": 0.08},
    'Y': {"trade_unit_num": 10, "cash_deposit_percent": 0.08},
    'MA': {"trade_unit_num": 10, "cash_deposit_percent": 0.1},
    'EG': {"trade_unit_num": 10, "cash_deposit_percent": 0.09},
    'AG': {"trade_unit_num": 15, "cash_deposit_percent": 0.1},
    'PP': {"trade_unit_num": 5, "cash_deposit_percent": 0.08},
    'AU': {"trade_unit_num": 1000, "cash_deposit_percent": 0.09},
    'A': {"trade_unit_num": 10, "cash_deposit_percent": 0.08},
    'CS': {"trade_unit_num": 10, "cash_deposit_percent": 0.08},
    'SP': {"trade_unit_num": 10, "cash_deposit_percent": 0.1},
    'CJ': {"trade_unit_num": 5, "cash_deposit_percent": 0.1},
    'ZC': {"trade_unit_num": 100, "cash_deposit_percent": 0.09},
    'AI': {"trade_unit_num": 5, "cash_deposit_percent": 0.1},
    'V': {"trade_unit_num": 5, "cash_deposit_percent": 0.08},
    'BU': {"trade_unit_num": 10, "cash_deposit_percent": 0.12},
}
