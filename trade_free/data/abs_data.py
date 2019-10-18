from abc import ABC, abstractmethod


class AbsDataHandler(ABC):
    """
    提供数据的抽象类
    """

    @abstractmethod
    def get_latest_bars(self, symbol, N=1):
        """
        获取最新的N条数据
        """

    @abstractmethod
    def update_bars(self):
        """
        维护数据, 更新新的数据到结构里面
        """

    @abstractmethod
    def register_event_queue(self, event_queue):
        """
        注册事件队列
        """

    @abstractmethod
    def init_data(self, start_date, end_date):
        """
        初始化数据
        """
