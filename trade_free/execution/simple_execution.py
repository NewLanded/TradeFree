from .abs_execution import ExecutionHandler
from ..event import FillEvent


class SimulatedExecutionHandler(ExecutionHandler):
    """
    此实现不考虑延迟, 滑点等问题
    """

    def __init__(self, event_queue):
        """
        Parameters:
        events - The Queue of Event objects.
        """
        self.event_queue = event_queue

    def execute_order(self, event):
        """
        使用Order objects, 生成Fill objects

        Parameters:
        event - Contains an Event object with order information.
        """
        event_id = event.event_id
        symbol = event.symbol
        order_type = event.order_type
        quantity = event.quantity
        direction = event.direction
        price = event.price
        order_date = event.order_date

        fill_event = FillEvent(event_id, symbol, order_date, 'SH/SZ', quantity, direction, order_type, price)
        self.event_queue.put(fill_event)
