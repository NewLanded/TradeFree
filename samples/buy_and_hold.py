import datetime

from trade_free.brain import BaseBrain
from trade_free.data import HistoricCSVDataHandler
from trade_free.strategy import BuyAndHoldStrategy

if __name__ == "__main__":
    bars = HistoricCSVDataHandler(r"../test_data", ["000001.SZ", "000538.SZ"])
    brain = BaseBrain(bars, datetime.datetime(2017, 1, 1), datetime.datetime(2017, 12, 31), 10000)
    brain.add_Strategy(BuyAndHoldStrategy)
    brain.start()
    brain.output_summary_stats()
    brain.plot_one_symbol("000001.SZ")




