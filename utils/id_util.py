class AutoIncrementMetaclass(type):
    def __call__(cls, *args, **kwargs):
        raise TypeError("Can't instantiate directly")


class EventId(metaclass=AutoIncrementMetaclass):
    id = 0

    @classmethod
    def get_next_id(cls):
        id_str = str(cls.id).rjust(16, "0")
        cls.id += 1
        return id_str
