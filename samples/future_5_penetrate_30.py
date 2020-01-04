import datetime

from trade_free.brain import FutureBrain
from trade_free.data import FutureHistoricDatabaseDataHandler
from trade_free.strategy import Future5Penetrate30Strategy

if __name__ == "__main__":
    bars = FutureHistoricDatabaseDataHandler(['AP2001.ZCE'])
    brain = FutureBrain()

    brain.add_bars(bars, datetime.datetime(2019, 1, 1), datetime.datetime(2019, 12, 31))
    brain.add_portfolio(100000)
    brain.add_execution_handler()
    brain.add_Strategy(Future5Penetrate30Strategy, strategy_min_days=33)

    brain.start()
    brain.output_summary_stats()
    brain.plot_one_symbol("AP2001.ZCE")
