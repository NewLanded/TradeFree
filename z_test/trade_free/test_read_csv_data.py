from trade_free.data import HistoricCSVDataHandler
from queue import Queue


class Test:
    def test_0(self):
        data_handler = HistoricCSVDataHandler(r"../../test_data", ["000001.SZ", "000538.SZ"])
        data_handler.register_event_queue(Queue())

        print(data_handler.get_latest_bars("000001.SZ"))
        data_handler.update_bars()
        print(data_handler.get_latest_bars("000001.SZ"))
        data_handler.get_latest_bars("000001.SZ")
        data_handler.update_bars()
        print(data_handler.get_latest_bars("000001.SZ", 2))


if __name__ == "__main__":
    import os
    import pytest

    pytest.main([os.path.join(os.path.curdir, __file__), "-s", "--tb=short"])
