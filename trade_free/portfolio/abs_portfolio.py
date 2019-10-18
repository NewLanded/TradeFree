from abc import ABC, abstractmethod


class AbsPortfolio(ABC):
    """
    The Portfolio class 处理持仓和市场价值

    每次从DataHandler对象请求新的市场数据时，投资组合必须更新所有持仓的当前市场价值。在实时交易场景中，可以直接从经纪商处下载和解析此信息，但对于回测实施，有必要手动计算这些值
    """

    @abstractmethod
    def update_signal(self, event):
        """
        接收SignalEvent产生订单
        """

    @abstractmethod
    def update_fill(self, event):
        """
        接收FillEvent信号更新持仓.
        """
