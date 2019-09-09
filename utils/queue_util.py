from collections import deque


class SimpleEventQueue:
    def __init__(self):
        self.event_queue = deque()

    def put(self, value):
        self.event_queue.append(value)

    def pop(self):
        return self.event_queue.popleft()
