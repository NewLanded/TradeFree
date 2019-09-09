from abc import ABCMeta, abstractmethod

from utils.queue_util import SimpleEventQueue


class AbsBrain(metaclass=ABCMeta):
    """
    初始化各组件, 执行回测或交易
    """

    def __init__(self, event_queue=None):
        """
        :param event_queue:  需要实现 put和pop方法, 先入先出
        """
        self.event_queue = event_queue if event_queue is not None else self._inti_event_queue()

    def _inti_event_queue(self):
        return SimpleEventQueue()

    @abstractmethod
    def add_Strategy(self, *args, **kwargs):
        """初始化Strategy"""
        pass

    @abstractmethod
    def start(self):
        """开始回测或交易"""
        pass
