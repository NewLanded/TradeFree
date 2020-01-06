import datetime

from trade_free.brain import FutureBrain
from trade_free.data import FutureHistoricDatabaseDataHandler
from trade_free.strategy import Future5Penetrate30Strategy


def start(ts_code, ploy_flag=True):
    bars = FutureHistoricDatabaseDataHandler([ts_code])
    brain = FutureBrain()

    brain.add_bars(bars, datetime.datetime(2019, 1, 1), datetime.datetime(2019, 12, 31))
    brain.add_portfolio(100000)
    brain.add_execution_handler()
    brain.add_Strategy(Future5Penetrate30Strategy, strategy_min_days=33)

    brain.start()
    brain.output_summary_stats()

    if ploy_flag is True:
        brain.plot_one_symbol(ts_code)


def start_all_symbol():
    ts_code_list = ['AP2001.ZCE', 'C2001.DCE', 'CF2001.ZCE', 'FG2001.ZCE', 'HC2001.SHF', 'JD2001.DCE', 'L2001.DCE', 'M2001.DCE', 'OI2001.ZCE', 'P2001.DCE',
                    'RB2001.SHF', 'RM2001.ZCE', 'SR2001.ZCE', 'Y2001.DCE']
    for ts_code in ts_code_list:
        print(ts_code)
        start(ts_code, ploy_flag=False)


if __name__ == "__main__":
    # start('FG2001.ZCE')
    start_all_symbol()
