from abc import ABCMeta, abstractmethod


class AbsDataHandler(metaclass=ABCMeta):
    """
    提供数据的抽象类
    """

    @abstractmethod
    def get_latest_bars(self, symbol, N=1):
        """
        获取最新的N条数据
        """
        raise NotImplementedError("Should implement get_latest_bars()")

    @abstractmethod
    def update_bars(self):
        """
        维护数据, 更新新的数据到结构里面
        """
        raise NotImplementedError("Should implement update_bars()")

    @abstractmethod
    def register_event_queue(self, event_queue):
        """
        注册事件队列
        """
        raise NotImplementedError("Should implement register_event_queue(event_queue)")

    @abstractmethod
    def init_data(self, start_date, end_date):
        """
        初始化数据
        """
        raise NotImplementedError("Should implement init_data(start_date, end_date)")
