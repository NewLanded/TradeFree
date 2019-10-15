from abc import ABC, abstractmethod


class ExecutionHandler(ABC):
    """
    将Portfolio产生的下单对象转换为市场上的交易, 也可用户回测
    """

    @abstractmethod
    def execute_order(self, event):
        """
        执行Order event , 生成Fill event

        Parameters:
        event - Contains an Event object with order information.
        """
        raise NotImplementedError("Should implement execute_order()")
