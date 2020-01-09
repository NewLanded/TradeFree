from collections import deque


class SimpleEventQueue:
    def __init__(self):
        self.event_queue = deque()

    def put(self, value, put_left_flag=False):
        if put_left_flag is True:
            self.event_queue.appendleft(value)
        else:
            self.event_queue.append(value)

    def pop(self):
        return self.event_queue.popleft()
